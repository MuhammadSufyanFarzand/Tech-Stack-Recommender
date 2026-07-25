from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {
            'status': 'ok',
            'project': 'Tech Stack Recommender',
            'platform': 'Vercel Serverless Python',
            'algorithm': 'TF-IDF Vectorization & Cosine Similarity'
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))
