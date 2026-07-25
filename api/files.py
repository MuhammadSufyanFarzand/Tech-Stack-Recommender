from http.server import BaseHTTPRequestHandler
import json
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

candidate_dirs = [
    os.path.abspath(os.path.join(base_dir, '..', 'tech-stack-recommender')),
    os.path.abspath(os.path.join(base_dir, '..')),
    os.path.abspath(os.path.join(base_dir, 'tech-stack-recommender')),
]

project_dir = None
for candidate in candidate_dirs:
    if os.path.exists(os.path.join(candidate, 'app.py')) or os.path.exists(os.path.join(candidate, 'data', 'raw_skills.csv')):
        project_dir = candidate
        break

if project_dir is None:
    project_dir = candidate_dirs[0]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        file_tree = []

        def scan_dir(dir_path):
            if not os.path.exists(dir_path):
                return
            for item in os.listdir(dir_path):
                if item in {'__pycache__', 'node_modules', '.git'} or item.endswith('.zip'):
                    continue
                
                full_path = os.path.join(dir_path, item)
                rel_path = os.path.relpath(full_path, project_dir)

                if os.path.isdir(full_path):
                    file_tree.append({'path': full_path, 'relativePath': rel_path, 'type': 'dir'})
                    scan_dir(full_path)
                elif os.path.isfile(full_path):
                    content = ""
                    try:
                        if not item.endswith('.pkl') and not item.endswith('.zip'):
                            with open(full_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                    except Exception:
                        content = "(Binary file)"

                    stat = os.stat(full_path)
                    file_tree.append({
                        'path': full_path,
                        'relativePath': rel_path,
                        'type': 'file',
                        'size': stat.st_size,
                        'content': content
                    })

        scan_dir(project_dir)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'success', 'files': file_tree}).encode('utf-8'))
