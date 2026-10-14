
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import {
  mkdtemp,
  mkdir,
  writeFile,
  rm,
} from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';

const tempDir = await mkdtemp(
  path.join(os.tmpdir(), 'resqspace-test-')
);

process.env.NODE_ENV = 'test';
process.env.RESQSPACE_DATA_DIR = tempDir;

const { app } = await import('../server.js');

let server;
let baseUrl;

before(async () => {
  server = app.listen(0);

  await new Promise((resolve, reject) => {
    server.once('listening', resolve);
    server.once('error', reject);
  });

  const address = server.address();
  baseUrl = `http://127.0.0.1:${address.port}`;
});

after(async () => {
  if (server) {
    await new Promise((resolve, reject) => {
      server.close((error) => {
        if (error) reject(error);
        else resolve();
      });
    });
  }

  await rm(tempDir, { recursive: true, force: true });
});

test('health endpoint responds successfully', async () => {
  const response = await fetch(`${baseUrl}/api/health`);

  assert.equal(response.status, 200);

  const body = await response.json();
  assert.equal(body.status, 'ok');
});

test('missing output files are unavailable, not zero', async () => {
  const response = await fetch(`${baseUrl}/api/results`);

  assert.equal(response.status, 200);

  const body = await response.json();

  assert.equal(body.schemaVersion, '0.1.0');
  assert.equal(body.integrationStatus, 'unavailable');
  assert.equal(body.warnings.length, 7);

  for (const item of Object.values(body.files)) {
    assert.equal(item.status, 'unavailable');
    assert.equal(item.data, null);
  }
});

test('malformed summary JSON is rejected', async () => {
  await writeFile(
    path.join(tempDir, 'flood_summary.json'),
    '{not valid JSON'
  );

  const response = await fetch(`${baseUrl}/api/results`);
  const body = await response.json();

  assert.equal(body.files.floodSummary.status, 'invalid');
  assert.equal(body.files.floodSummary.data, null);
  assert.equal(body.integrationStatus, 'invalid');
});

test('invalid GeoJSON structure is rejected', async () => {
  await writeFile(
    path.join(tempDir, 'flood_extent.geojson'),
    JSON.stringify({
      type: 'FeatureCollection',
      features: [{ type: 'NotAFeature' }],
    })
  );

  const response = await fetch(`${baseUrl}/api/results`);
  const body = await response.json();

  assert.equal(body.files.floodExtent.status, 'invalid');
  assert.equal(body.files.floodExtent.data, null);
  assert.equal(body.integrationStatus, 'invalid');
});

