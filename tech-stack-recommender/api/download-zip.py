from http.server import BaseHTTPRequestHandler
import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))

candidate_dirs = [
    os.path.abspath(os.path.join(base_dir, '..')),
    os.path.abspath(os.path.join(base_dir, '..', 'tech-stack-recommender')),
    os.path.abspath(os.path.join(base_dir, 'tech-stack-recommender')),
]

project_dir = None
for candidate in candidate_dirs:
    if os.path.exists(os.path.join(candidate, 'create_zip.py')):
        project_dir = candidate
        break

if project_dir is None:
    project_dir = candidate_dirs[0]

if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            from create_zip import create_project_zip
            zip_path = create_project_zip()

            if os.path.exists(zip_path):
                with open(zip_path, 'rb') as f:
                    zip_bytes = f.read()

                self.send_response(200)
                self.send_header('Content-Type', 'application/zip')
                self.send_header('Content-Disposition', 'attachment; filename="tech-stack-recommender.zip"')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(zip_bytes)
            else:
                self.send_response(500)
                self.end_headers()
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))
