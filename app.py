#!/usr/bin/env python3
"""
Tech Stack Recommender - Main Application Entry Point
Content-Based Filtering using TF-IDF Vectorization & Cosine Similarity.
Ready for deployment on platforms like Vercel.
"""

import os
import sys
import json
from typing import List, Dict, Any
from flask import Flask, request, jsonify, render_template_string, send_from_directory

# Configure path resolution for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.ingestion import SkillIngestor
from src.vectorizer import TFIDFVectorizerModel
from src.similarity import CosineSimilarityEngine

# ==========================================
# 1. CORE RECOMMENDER SERVICE CLASS
# ==========================================
class TechStackRecommenderService:
    """
    Service orchestration layer connecting Ingestion, Vectorizer, and Similarity Engine.
    """

    def __init__(self, data_path: str = None, model_dir: str = None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_path = data_path or os.path.join(base_dir, "data", "raw_skills.csv")
        self.model_dir = model_dir or os.path.join(base_dir, "models")
        self.model_file = os.path.join(self.model_dir, "tfidf_vectorizer.pkl")

        self.ingestor = SkillIngestor(self.data_path)
        self.vectorizer = TFIDFVectorizerModel(max_features=500, ngram_range=(1, 2))
        self.processed_records: List[Dict[str, Any]] = []
        self.dataset_vectors: List[List[float]] = []
        self.is_initialized = False

    def initialize(self, force_retrain: bool = False):
        """Loads data, prepares combined feature documents, fits TF-IDF matrix, and saves model."""
        print("🔄 Loading dataset and preparing features...")
        self.processed_records = self.ingestor.prepare_features()

        corpus = [r['combined_features'] for r in self.processed_records]

        print("⚡ Fitting TF-IDF Vectorizer model on corpus...")
        self.dataset_vectors = self.vectorizer.fit_transform(corpus)

        # Attempt to save model, catching permission errors on read-only serverless filesystems
        try:
            if not os.path.exists(self.model_dir):
                os.makedirs(self.model_dir, exist_ok=True)
            self.vectorizer.save_model(self.model_file)
            print(f"📁 Model saved successfully to {self.model_file}")
        except Exception as e:
            print(f"⚠️ Warning: Could not write model file (likely read-only serverless filesystem): {e}")

        self.is_initialized = True
        print(f"✅ Initialized recommender with {len(self.processed_records)} tech stacks.")

    def recommend_for_query(self, query_text: str, top_n: int = 5, min_score: float = 0.0) -> Dict[str, Any]:
        """
        Processes query, transforms into TF-IDF vector space, and computes cosine similarity.
        """
        if not self.is_initialized:
            self.initialize()

        cleaned_query = SkillIngestor.clean_text(query_text)
        query_vector = self.vectorizer.transform(cleaned_query)[0]

        recommendations = CosineSimilarityEngine.recommend(
            query_vector=query_vector,
            dataset_vectors=self.dataset_vectors,
            dataset_records=self.processed_records,
            feature_names=self.vectorizer.get_feature_names(),
            top_n=top_n,
            min_score=min_score
        )

        return {
            'query_raw': query_text,
            'query_cleaned': cleaned_query,
            'total_stacks_analyzed': len(self.processed_records),
            'top_n': top_n,
            'recommendations': recommendations
        }

    def get_all_stacks(self) -> List[Dict[str, Any]]:
        if not self.is_initialized:
            self.initialize()
        return [
            {
                'stack_id': r['stack_id'],
                'stack_name': r['stack_name'],
                'category': r['category'],
                'roles': r['roles'],
                'primary_language': r['primary_language'],
                'frameworks_libraries': r['frameworks_libraries'],
                'database_storage': r['database_storage'],
                'infrastructure_tools': r['infrastructure_tools'],
                'skills_description': r['skills_description']
            }
            for r in self.processed_records
        ]


# Initialize service instance
recommender_service = TechStackRecommenderService()

# ==========================================
# 2. TOP-LEVEL GLOBAL FLASK INSTANCE FOR VERCEL
# ==========================================
app = Flask(__name__)


# ==========================================
# 3. WEBPAGE FRONTEND HTML TEMPLATE
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tech Stack Recommender</title>
    
    <!-- Tab image configuration pointing to your custom static/logo.png file -->
    <link rel="icon" type="image/png" href="/static/logo.png">
    <link rel="shortcut icon" type="image/png" href="/static/logo.png">

    <style>
        :root {
            --primary-color: #3b82f6;
            --background-color: #f3f4f6;
            --card-color: #ffffff;
            --text-color: #1f2937;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            margin: 0;
            background-color: var(--background-color);
            color: var(--text-color);
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        .main-container {
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            flex-grow: 1;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header img {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            object-fit: cover;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .header h1 {
            margin: 10px 0 5px;
            font-size: 2.2rem;
            font-weight: 800;
        }
        .header p {
            color: #4b5563;
            margin-top: 0;
        }
        .search-card {
            background-color: var(--card-color);
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 30px;
        }
        textarea {
            width: 100%;
            box-sizing: border-box;
            height: 100px;
            border-radius: 8px;
            border: 1px solid #d1d5db;
            padding: 12px;
            font-size: 1rem;
            font-family: inherit;
            resize: vertical;
            outline-color: var(--primary-color);
        }
        .controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 15px;
        }
        button {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            font-weight: 600;
            transition: opacity 0.2s;
        }
        button:hover {
            opacity: 0.9;
        }
        .results-container h2 {
            font-size: 1.4rem;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 8px;
            margin-bottom: 15px;
        }
        .stack-card {
            background-color: var(--card-color);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.05);
        }
        .stack-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #f3f4f6;
            padding-bottom: 10px;
            margin-bottom: 10px;
        }
        .stack-name {
            font-weight: 700;
            font-size: 1.2rem;
        }
        .badge {
            background-color: #eff6ff;
            color: #1e40af;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        .score {
            font-size: 0.9rem;
            color: #10b981;
            font-weight: 700;
        }
        .meta-line {
            font-size: 0.9rem;
            margin: 6px 0;
        }
        .meta-line strong {
            color: #4b5563;
        }
        footer {
            text-align: center;
            padding: 25px 10px;
            margin-top: auto;
            background-color: #ffffff;
            font-size: 0.95rem;
            font-weight: 500;
            color: #4b5563;
            border-top: 1px solid #e5e7eb;
        }
    </style>
</head>
<body>

    <div class="main-container">
        <div class="header">
            <!-- Tries to show the set logo icon, otherwise uses fallback image/placeholder -->
            <img src="/static/logo.png" onerror="this.src='https://placehold.co/100x100?text=Logo'" alt="App Logo">
            <h1>Tech Stack Recommender</h1>
            <p>Content-Based Filtering via TF-IDF Vectorization & Cosine Similarity</p>
        </div>

        <div class="search-card">
            <textarea id="queryInput" placeholder="Describe your project (e.g., 'Looking for a Python backend with FastAPI, PostgreSQL, and Docker...')"></textarea>
            <div class="controls">
                <label>
                    Top Results:
                    <select id="topNSelect" style="padding: 6px; border-radius: 4px; border: 1px solid #d1d5db;">
                        <option value="3" selected>3</option>
                        <option value="5">5</option>
                        <option value="10">10</option>
                    </select>
                </label>
                <button onclick="getRecommendations()">Analyze Stack</button>
            </div>
        </div>

        <div class="results-container" id="resultsSection" style="display: none;">
            <h2>Recommendations</h2>
            <div id="resultsList"></div>
        </div>
    </div>

    <!-- Attribution Footer displayed when scrolling to the end of the page -->
    <footer>
        This webapp is developed by Muhammad Sufiyan Farzad.
    </footer>

    <script>
        async function getRecommendations() {
            const query = document.getElementById('queryInput').value.trim();
            const topN = document.getElementById('topNSelect').value;
            if (!query) {
                alert('Please provide some skills or project descriptions first.');
                return;
            }

            const resultsSection = document.getElementById('resultsSection');
            const resultsList = document.getElementById('resultsList');
            
            resultsList.innerHTML = '<p style="text-align:center; color:#6b7280;">Computing similarities...</p>';
            resultsSection.style.display = 'block';

            try {
                const response = await fetch('/api/recommend', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query, top_n: parseInt(topN) })
                });
                
                const responseData = await response.json();
                
                if (responseData.status === 'success' && responseData.data.recommendations.length > 0) {
                    resultsList.innerHTML = '';
                    responseData.data.recommendations.forEach(r => {
                        const terms = r.matching_terms ? r.matching_terms.map(t => t.term).join(', ') : 'None';
                        
                        const card = document.createElement('div');
                        card.className = 'stack-card';
                        card.innerHTML = `
                            <div class="stack-header">
                                <span class="stack-name">${r.stack_name}</span>
                                <span class="badge">${r.category}</span>
                            </div>
                            <div class="meta-line"><span class="score">Match: ${r.match_percentage}%</span></div>
                            <div class="meta-line"><strong>Primary Language:</strong> ${r.primary_language || 'N/A'}</div>
                            <div class="meta-line"><strong>Frameworks:</strong> ${r.frameworks_libraries || 'N/A'}</div>
                            <div class="meta-line"><strong>Databases:</strong> ${r.database_storage || 'N/A'}</div>
                            <div class="meta-line"><strong>Matching Terms:</strong> ${terms || 'General alignment'}</div>
                        `;
                        resultsList.appendChild(card);
                    });
                } else {
                    resultsList.innerHTML = '<p style="text-align:center; color:#ef4444;">No highly similar matching stacks found.</p>';
                }
            } catch (error) {
                console.error(error);
                resultsList.innerHTML = '<p style="text-align:center; color:#ef4444;">Could not process the recommendation request.</p>';
            }
        }
    </script>
</body>
</html>
"""

# ==========================================
# 4. HTTP FLASK ROUTING DEFINITIONS
# ==========================================

@app.route('/', methods=['GET'])
def index():
    """Serves the main interactive dashboard webpage."""
    return render_template_string(HTML_TEMPLATE)


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    """Serves the tab icon favicon from the static directory."""
    static_dir = os.path.join(app.root_path, 'static')
    if os.path.exists(os.path.join(static_dir, 'logo.png')):
        return send_from_directory(static_dir, 'logo.png', mimetype='image/png')
    elif os.path.exists(os.path.join(static_dir, 'favicon.ico')):
        return send_from_directory(static_dir, 'favicon.ico', mimetype='image/x-icon')
    return '', 204


@app.route('/api/stacks', methods=['GET'])
def get_stacks():
    """Retrieve dataset tech stacks."""
    return jsonify({'status': 'success', 'data': recommender_service.get_all_stacks()})


@app.route('/api/recommend', methods=['POST'])
def recommend():
    """Get TF-IDF Cosine Similarity recommendations based on query."""
    data = request.get_json(force=True) or {}
    query = data.get('query', '')
    top_n = int(data.get('top_n', 5))
    if not query:
        return jsonify({'status': 'error', 'message': 'Missing query parameter'}), 400

    result = recommender_service.recommend_for_query(query, top_n=top_n)
    return jsonify({'status': 'success', 'data': result})


@app.route('/api/retrain', methods=['POST'])
def retrain():
    """Reload dataset and retrain vectorizer."""
    recommender_service.initialize(force_retrain=True)
    return jsonify({'status': 'success', 'message': 'Model retrained successfully'})


# Helper function for local execution
def run_cli_interactive():
    """Runs interactive command-line interface for local recommendation testing."""
    print("=" * 65)
    print("🚀 TECH STACK RECOMMENDER - TF-IDF & COSINE SIMILARITY DEMO")
    print("=" * 65)
    recommender_service.initialize()

    while True:
        print("\nEnter target project requirements, job roles, or developer skills:")
        print("(e.g., 'Looking for a Python backend with FastAPI, PostgreSQL, Docker')")
        user_input = input("\n👉 Query (or 'q' to quit): ").strip()

        if not user_input or user_input.lower() in {'q', 'quit', 'exit'}:
            print("Goodbye!")
            break

        res = recommender_service.recommend_for_query(user_input, top_n=3)
        recs = res['recommendations']

        print(f"\n📊 TOP {len(recs)} RECOMMENDED TECH STACKS:")
        print("-" * 65)
        for r in recs:
            print(f"Rank {r['rank']} | {r['stack_name']} [{r['category']}]")
            print(f"  • Cosine Similarity Match: {r['match_percentage']}% (Score: {r['similarity_score']})")
            print(f"  • Primary Lang: {r['primary_language']}")
            print(f"  • Frameworks: {r['frameworks_libraries']}")
            print(f"  • Database: {r['database_storage']}")
            print(f"  • Matching Key Terms: {', '.join([t['term'] for t in r['matching_terms']]) or 'General alignment'}")
            print("-" * 65)


if __name__ == '__main__':
    # Initialize model locally before launching server
    recommender_service.initialize()
    
    if '--cli' in sys.argv:
        run_cli_interactive()
    else:
        # Run local debug server
        app.run(host='0.0.0.0', port=5000, debug=True)