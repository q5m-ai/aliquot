from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit

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

    def test_point_card_is_an_overlay_inside_the_chart(self):
        self.assertRegex(read("site/index.html"),
                         r'<div id="chart" class="chart">\s*<canvas[^>]+></canvas>\s*<section id="point-details"')
        css = read("site/site.css")
        self.assertIn(".chart{position:relative}", css)
        overlay = css.split(".point-details{", 1)[1].split("}", 1)[0]
        for expected in ["position:absolute", "max-width:calc(100% - 16px)",
                         "overflow:visible", "pointer-events:none"]:
            self.assertIn(expected, overlay)
        self.assertNotIn("max-height", overlay)
        self.assertNotIn("overflow:auto", overlay)
        divisors = css.split("#point-divisors{", 1)[1].split("}", 1)[0]
        self.assertEqual(divisors, "overflow:visible")
        self.assertNotIn("overflow-y:auto", css)
        self.assertIn(".point-details[data-pinned=true]{pointer-events:auto}", css)

    def test_seed_shortcuts_and_adjustment_controls_are_above_the_chart(self):
        html = read("site/index.html")
        form = re.search(r'<form class="controls" id="form">(.*?)</form>', html, re.S).group(1)
        self.assertEqual(re.findall(r'<button type="button" data-n="(\d+)"', form),
                         ["12", "30", "28", "95", "790", "220", "1184", "1264460", "12496", "276"])
        self.assertIn('id="preset-info"', form)
        self.assertEqual(html.count('class="presets"'), 1)
        self.assertLess(html.index('class="presets"'), html.index('id="graph"'))
        self.assertIn('id="seed-decrement" aria-label="Decrease starting number by 1"', form)
        self.assertIn('id="seed-increment" aria-label="Increase starting number by 1"', form)
        self.assertIn('id="speed" min="1" max="20" value="8"', form)
        self.assertIn('id="speed-readout"', form)
        self.assertIn('<option value="linear" selected>linear y</option>', form)

    def test_site_dependencies_are_self_hosted_and_ordered(self):
        html = read("site/index.html")
        scripts = [urlsplit(url).path for url in re.findall(r'<script src="([^"]+)" defer></script>', html)]
        self.assertEqual(scripts, ["/vendor/katex/katex.min.js", "/latex.js", "/math.js", "/explorer.js"])
        for script in scripts:
            self.assertTrue((ROOT / "site" / script.lstrip("/")).is_file())
        self.assertEqual(read("favicon.svg"), read("site/favicon.svg"))
