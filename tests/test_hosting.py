from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text()


class HostingTests(unittest.TestCase):
    def test_native_contract_and_allocated_ingress(self):
        self.assertEqual(read("q5m/app.env"), "Q5M_APP=aliquot\nQ5M_INGRESS_PORTS=20001/tcp\n")
        compose = read("q5m/compose.yaml")
        for expected in ['published: "20001"', 'target: 8080', 'host_ip: 0.0.0.0',
                         'read_only: true', 'user: "1000:1000"', 'cap_drop: [ALL]',
                         'no-new-privileges:true', 'mem_limit: 128m', 'pids_limit: 128', '/.q5m-release']:
            self.assertIn(expected, compose)
        self.assertNotIn('published: "0"', compose)
        for expected in ['name: aliquot', 'node: q5m-n01', 'hostname: aliquot.q5m.ai', 'health: /.q5m-release']:
            self.assertIn(expected, read("q5m.yaml"))

    def test_static_artifact_boundary_and_security(self):
        dockerfile = read("q5m/Dockerfile")
        self.assertRegex(dockerfile, r"FROM .*@sha256:[0-9a-f]{64}\n")
        self.assertIn("COPY site/", dockerfile)
        self.assertNotIn("COPY . ", dockerfile)
        self.assertIn("USER 1000:1000", dockerfile)
        self.assertIn(".q5m-release", dockerfile)
        self.assertEqual(read(".dockerignore"), "**\n!site/\n!site/**\n!q5m/\n!q5m/Dockerfile\n!q5m/nginx.conf\n")
        for expected in ['autoindex off', 'disable_symlinks on', 'nosniff', 'Content-Security-Policy',
                         'location ~ /\\. { deny all; }', 'try_files $uri $uri/ =404']:
            self.assertIn(expected, read("q5m/nginx.conf"))

    def test_site_dependencies_are_self_hosted_and_ordered(self):
        html = read("site/index.html")
        scripts = re.findall(r'<script src="([^"]+)" defer></script>', html)
        self.assertEqual(scripts, ["/math.js", "/explorer.js"])
        for script in scripts:
            self.assertTrue((ROOT / "site" / script.lstrip("/")).is_file())
        self.assertEqual(read("favicon.svg"), read("site/favicon.svg"))
