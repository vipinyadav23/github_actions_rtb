from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"status": "healthy", "service": "genai-cicd-demo", "version": APP_VERSION})
            return
        if self.path == "/":
            self._send(200, {"message": "GitHub Actions + GenAI CI/CD demo", "version": APP_VERSION})
            return
        self._send(404, {"error": "not found"})

    def log_message(self, format, *args):
        return

def create_server(port: int = 8080):
    return HTTPServer(("0.0.0.0", port), Handler)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    server = create_server(port)
    print(f"Listening on :{port}")
    server.serve_forever()
