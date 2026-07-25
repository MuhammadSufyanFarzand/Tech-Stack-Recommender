import React, { useState, useEffect } from 'react';
import { RecommendationApiResponse, ProjectFile } from './types';
import { Header } from './components/Header';
import { RecommenderWorkbench } from './components/RecommenderWorkbench';
import { MathExplainer } from './components/MathExplainer';
import { CodeExplorer } from './components/CodeExplorer';
import { ExportDeploy } from './components/ExportDeploy';

export default function App() {
  const [activeTab, setActiveTab] = useState<string>('workbench');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [recommendationData, setRecommendationData] = useState<RecommendationApiResponse | null>(null);
  const [files, setFiles] = useState<ProjectFile[]>([]);
  const [isDownloadingZip, setIsDownloadingZip] = useState<boolean>(false);

  // Fetch project files on load
  const fetchFiles = async () => {
    try {
      const res = await fetch('/api/files');
      const data = await res.json();
      if (data.status === 'success') {
        setFiles(data.files || []);
      }
    } catch (err) {
      console.error('Failed to fetch files:', err);
    }
  };

  useEffect(() => {
    fetchFiles();
    // Run initial recommendation query on load
    handleRecommend(
      'Building an AI microservices backend with Python, FastAPI, PyTorch, PostgreSQL, and Docker containerization',
      3
    );
  }, []);

  const handleRecommend = async (query: string, topN: number = 3): Promise<RecommendationApiResponse | null> => {
    setIsLoading(true);
    try {
      const res = await fetch('/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, top_n: topN })
      });

      const json = await res.json();
      if (json.status === 'success' && json.data) {
        setRecommendationData(json.data);
        setIsLoading(false);
        return json.data;
      }
    } catch (err) {
      console.error('Recommendation API error:', err);
    }
    setIsLoading(false);
    return null;
  };

  const handleSaveFile = async (relativePath: string, content: string): Promise<boolean> => {
    try {
      const res = await fetch('/api/files/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ relativePath, content })
      });
      const data = await res.json();
      if (data.status === 'success') {
        await fetchFiles();
        // Re-run current recommendation to retrain
        if (recommendationData?.query_raw) {
          handleRecommend(recommendationData.query_raw, recommendationData.top_n);
        }
        return true;
      }
    } catch (err) {
      console.error('Save file error:', err);
    }
    return false;
  };

  const handleDownloadZip = async () => {
    setIsDownloadingZip(true);
    try {
      const windowRef = window.open('/api/download-zip', '_blank');
      if (!windowRef) {
        window.location.href = '/api/download-zip';
      }
    } catch (err) {
      console.error('Download error:', err);
    }
    setTimeout(() => setIsDownloadingZip(false), 2000);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans antialiased selection:bg-indigo-500 selection:text-white">
      
      {/* Top Header & Navigation */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onDownloadZip={handleDownloadZip}
        isDownloadingZip={isDownloadingZip}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'workbench' && (
          <RecommenderWorkbench
            onRecommend={handleRecommend}
            isLoading={isLoading}
            recommendationData={recommendationData}
          />
        )}

        {activeTab === 'math' && <MathExplainer />}

        {activeTab === 'code' && (
          <CodeExplorer
            files={files}
            onRefreshFiles={fetchFiles}
            onSaveFile={handleSaveFile}
          />
        )}

        {activeTab === 'deploy' && (
          <ExportDeploy
            onDownloadZip={handleDownloadZip}
            isDownloadingZip={isDownloadingZip}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 py-6 bg-slate-950">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-400 gap-4">
          <div>
            Project 3: Tech Stack Recommender • Powered by Python, TF-IDF Vectorization & Cosine Similarity
          </div>
          <div className="flex items-center space-x-4 font-mono">
            <span>Algorithm: Content-Based Filtering</span>
            <span>•</span>
            <span>Matrix: L2 Cosine Norm</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
