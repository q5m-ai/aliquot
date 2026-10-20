import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
const read = path => readFileSync(new URL('../' + path, import.meta.url), 'utf8');

test('native contract has exact identity, allocated ingress, and release health', () => {
  assert.equal(read('q5m/app.env'), 'Q5M_APP=aliquot\nQ5M_INGRESS_PORTS=20001/tcp\n');
  const compose = read('q5m/compose.yaml');
  for (const expected of ['published: "20001"', 'target: 8080', 'host_ip: 0.0.0.0', 'read_only: true', 'user: "1000:1000"', 'cap_drop: [ALL]', 'no-new-privileges:true', 'mem_limit: 128m', 'pids_limit: 128', '/.q5m-release']) assert.ok(compose.includes(expected), expected);
  assert.ok(!compose.includes('published: "0"'));
  const declaration = read('q5m.yaml');
  for (const expected of ['name: aliquot', 'node: q5m-n01', 'hostname: aliquot.q5m.ai', 'health: /.q5m-release']) assert.ok(declaration.includes(expected), expected);
});

test('container build copies only public site and retains a pinned base image', () => {
  const dockerfile = read('q5m/Dockerfile');
  assert.match(dockerfile, /FROM .*@sha256:[0-9a-f]{64}\n/);
  assert.match(dockerfile, /COPY site\//);
  assert.ok(!dockerfile.includes('COPY . '));
  assert.match(dockerfile, /USER 1000:1000/);
  assert.match(dockerfile, /\.q5m-release/);
  assert.equal(read('.dockerignore'), '**\n!site/\n!site/**\n!q5m/\n!q5m/Dockerfile\n!q5m/nginx.conf\n');
  const nginx = read('q5m/nginx.conf');
  for (const expected of ['autoindex off', 'disable_symlinks on', 'nosniff', 'Content-Security-Policy', 'location ~ /\\. { deny all; }', 'try_files $uri $uri/ =404']) assert.ok(nginx.includes(expected), expected);
});
