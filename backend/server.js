import express from 'express';
import cors from 'cors';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);

const app = express();
const PORT = Number(process.env.PORT) || 3000;

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const DATA_DIR = process.env.RESQSPACE_DATA_DIR
  ? path.resolve(process.env.RESQSPACE_DATA_DIR)
  : path.join(__dirname, 'data', 'outputs');

const VALID_STATUSES = [
  'pending',
  'processing',
  'completed',
  'partial',
  'failed',
];


app.disable('x-powered-by');

app.use(cors({
  origin: [
    'http://localhost:5173',
    'http://localhost:5175',
    'https://res-q-space-6wjv9nmkc-nityajha54-6094s-projects.vercel.app',
    'https://res-q-space-git-main-nityajha54-6094s-projects.vercel.app',
  ],
}));

app.use(express.json({ limit: '1mb' }));

app.get('/api/health', (_req, res) => {
  res.status(200).json({
    status: 'ok',
    service: 'resqspace-backend',
  });
});

function isObject(value) {
  return (
    value !== null &&
    typeof value === 'object' &&
    !Array.isArray(value)
  );
}

function validateGeoJSON(value) {
  if (
    !isObject(value) ||
    value.type !== 'FeatureCollection' ||
    !Array.isArray(value.features)
  ) {
    return false;
  }

  return value.features.every(
    (feature) =>
      isObject(feature) &&
      feature.type === 'Feature' &&
      (feature.geometry === null ||
        isObject(feature.geometry)) &&
      (feature.properties === null ||
        isObject(feature.properties))
  );
}

function validateSummary(value) {
  if (!isObject(value)) {
    return false;
  }

  if (
    value.processing_status != null &&
    !VALID_STATUSES.includes(value.processing_status)
  ) {
    return false;
  }

  return true;
}

async function loadOutput(filename, validator) {
  let content;

  try {
    content = await readFile(
      path.join(DATA_DIR, filename),
      'utf8'
    );
  } catch (error) {
    if (error.code === 'ENOENT') {
      return {
        status: 'unavailable',
        data: null,
        message: 'Output file is not available yet.',
      };
    }

    console.error(`Could not read output: ${filename}`);

    return {
      status: 'error',
      data: null,
      message: 'Output file could not be read.',
    };
  }

  let data;

  try {
    data = JSON.parse(content);
  } catch {
    return {
      status: 'invalid',
      data: null,
      message: 'Output file contains invalid JSON.',
    };
  }

  if (!validator(data)) {
    return {
      status: 'invalid',
      data: null,
      message: 'Output does not match the expected structure.',
    };
  }

  return {
    status: 'available',
    data,
    message: null,
  };
}


let analysisRunning = false;

app.post('/api/analysis/run', async (_req, res) => {
  if (analysisRunning) {
    return res.status(409).json({
      status: 'processing',
      message: 'Satellite analysis is already running.',
    });
  }

  analysisRunning = true;

  try {
    const projectDir = path.resolve(__dirname, '..');
    const python = process.env.PYTHON_EXECUTABLE ||
      (process.platform === 'win32' ? 'python' : 'python3');

    const preEvent = path.join(
      projectDir, 'data', 'satellite_processed',
      'pre_event_sigma0_roi.tif'
    );
    const postEvent = path.join(
      projectDir, 'data', 'satellite_processed',
      'post_event_sigma0_roi.tif'
    );
    const script = `
import json
import sys
from src.satellite.run_pipeline import run_pipeline

result = run_pipeline(
    sys.argv[1],
    sys.argv[2],
    sys.argv[3],
    sys.argv[4]
)
print(json.dumps(result))
`;

    const { stdout } = await execFileAsync(
      python,
      [
        '-c', script, preEvent, postEvent,
        DATA_DIR, 'resqspace-demo',
      ],
      { cwd: projectDir, maxBuffer: 2 * 1024 * 1024 }
    );

    return res.status(200).json({
      status: 'completed',
      result: JSON.parse(stdout.trim()),
    });
  } catch (error) {
    console.error('Satellite analysis failed:', error.message);
    return res.status(500).json({
      status: 'failed',
      error: 'Satellite analysis failed. Check Python dependencies and input rasters.',
    });
  } finally {
    analysisRunning = false;
  }
});

app.get('/api/results', async (_req, res) => {
  const definitions = {
    floodExtent: [
      'flood_extent.geojson',
      validateGeoJSON,
    ],
    floodSummary: [
      'flood_summary.json',
      validateSummary,
    ],
    infrastructureExposure: [
      'infrastructure_exposure.geojson',
      validateGeoJSON,
    ],
    infrastructureSummary: [
      'infrastructure_summary.json',
      validateSummary,
    ],
    roadConnectivity: [
      'road_connectivity.geojson',
      validateGeoJSON,
    ],
    connectivitySummary: [
      'connectivity_summary.json',
      validateSummary,
    ],
    analysisMetadata: [
      'analysis_metadata.json',
      validateSummary,
    ],
  };

  try {
    const entries = await Promise.all(
      Object.entries(definitions).map(
        async ([key, [filename, validator]]) => [
          key,
          await loadOutput(filename, validator),
        ]
      )
    );

    const files = Object.fromEntries(entries);
    if (files.floodExtent?.status === 'available') {
  const geojson = files.floodExtent.data;
  const maxFeatures = 500;

  if (geojson.features.length > maxFeatures) {
    files.floodExtent.data = {
      ...geojson,
      features: geojson.features.slice(0, maxFeatures),
    };

    files.floodExtent.message =
      `Showing ${maxFeatures} of ${geojson.features.length} potential-change features for performance.`;
  }
}
    const results = Object.values(files);

    const availableCount = results.filter(
      (item) => item.status === 'available'
    ).length;

    const invalidCount = results.filter(
      (item) =>
        item.status === 'invalid' ||
        item.status === 'error'
    ).length;

    let integrationStatus;

    if (availableCount === results.length) {
      integrationStatus = 'ready';
    } else if (availableCount === 0 && invalidCount > 0) {
      integrationStatus = 'invalid';
    } else if (availableCount === 0) {
      integrationStatus = 'unavailable';
    } else {
      integrationStatus = 'partial';
    }

    const warnings = Object.entries(files)
      .filter(([, item]) => item.status !== 'available')
      .map(([key, item]) => ({
        output: key,
        status: item.status,
        message: item.message,
      }));

    return res.status(200).json({
      schemaVersion: '0.1.0',
      integrationStatus,
      files,
      warnings,
    });
  } catch {
    return res.status(500).json({
      error: 'Could not load analysis results.',
    });
  }
});

app.use((_req, res) => {
  res.status(404).json({
    error: 'Endpoint not found',
  });
});

export { app };

if (process.env.NODE_ENV !== 'test') {
  app.listen(PORT, () => {
    console.log(
      `ResQSpace backend listening on port ${PORT}`
    );
  });
}
