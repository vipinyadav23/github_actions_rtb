import json
from app.main import Handler

class FakeWFile:
    def __init__(self): self.data = b""
    def write(self, data): self.data += data

class FakeHandler(Handler):
    def __init__(self, path):
        self.path = path; self.sent = None; self.headers = {}; self.wfile = FakeWFile()
    def send_response(self, status): self.sent = status
    def send_header(self, key, value): self.headers[key] = value
    def end_headers(self): pass

def test_health_endpoint():
    h = FakeHandler("/health"); h.do_GET()
    assert h.sent == 200
    assert json.loads(h.wfile.data)["status"] == "healthy"

def test_root_endpoint():
    h = FakeHandler("/"); h.do_GET()
    assert h.sent == 200
    assert "GitHub Actions" in json.loads(h.wfile.data)["message"]

def test_unknown_endpoint():
    h = FakeHandler("/missing"); h.do_GET()
    assert h.sent == 404
