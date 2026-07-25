from http.server import BaseHTTPRequestHandler
import json
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
    if os.path.exists(os.path.join(candidate, 'app.py')) or os.path.exists(os.path.join(candidate, 'data', 'raw_skills.csv')):
        project_dir = candidate
        break

if project_dir is None:
    project_dir = candidate_dirs[0]

if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

service = None
init_error = None

try:
    from app import TechStackRecommenderService
    data_path = os.path.join(project_dir, 'data', 'raw_skills.csv')
    model_dir = os.path.join(project_dir, 'models')
    service = TechStackRecommenderService(data_path, model_dir)
    service.initialize()
except Exception as e:
    init_error = str(e)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        self.send_header('Access-Control-Allow-Origin', '*')
        
        try:
            req_json = json.loads(post_data.decode('utf-8'))
            query = req_json.get('query', '')
            top_n = int(req_json.get('top_n', 5))

            if not query.strip():
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Query string cannot be empty'}).encode('utf-8'))
                return

            if service is None:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': f'Failed to initialize recommender: {init_error}'}).encode('utf-8'))
                return

            result = service.recommend_for_query(query, top_n=top_n)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success', 'data': result}).encode('utf-8'))
        except Exception as err:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(err)}).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
