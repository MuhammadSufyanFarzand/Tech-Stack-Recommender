import React from 'react';
import { Cpu, Download, Sparkles, Terminal, Code2 } from 'lucide-react';

interface HeaderProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  onDownloadZip: () => void;
  isDownloadingZip: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  setActiveTab,
  onDownloadZip,
  isDownloadingZip
}) => {
  return (
    <header className="bg-slate-900 border-b border-slate-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo & Project Title */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center text-white shadow-lg shadow-indigo-500/20">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h1 className="text-lg font-bold text-slate-100 tracking-tight">
                  Tech Stack Recommender
                </h1>
                <span className="px-2 py-0.5 text-xs font-semibold rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                  Project 3
                </span>
              </div>
              <p className="text-xs text-slate-400 hidden sm:block">
                Content-Based Filtering • TF-IDF Vectorization & Cosine Similarity
              </p>
            </div>
          </div>

          {/* Download Zip CTA */}
          <div className="flex items-center space-x-3">
            <button
              onClick={onDownloadZip}
              disabled={isDownloadingZip}
              className="inline-flex items-center space-x-2 px-3.5 py-2 text-xs font-medium rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition-all shadow-md shadow-indigo-600/20 disabled:opacity-50"
            >
              <Download className={`w-4 h-4 ${isDownloadingZip ? 'animate-bounce' : ''}`} />
              <span>{isDownloadingZip ? 'Zipping...' : 'Download Project ZIP'}</span>
            </button>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex space-x-1 border-t border-slate-800/80 pt-2 pb-2 overflow-x-auto">
          <button
            onClick={() => setActiveTab('workbench')}
            className={`flex items-center space-x-2 px-4 py-2 text-xs font-medium rounded-lg transition-colors whitespace-nowrap ${
              activeTab === 'workbench'
                ? 'bg-indigo-600/15 text-indigo-400 border border-indigo-500/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <Sparkles className="w-4 h-4" />
            <span>Live Recommender</span>
          </button>

          <button
            onClick={() => setActiveTab('math')}
            className={`flex items-center space-x-2 px-4 py-2 text-xs font-medium rounded-lg transition-colors whitespace-nowrap ${
              activeTab === 'math'
                ? 'bg-indigo-600/15 text-indigo-400 border border-indigo-500/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <Cpu className="w-4 h-4" />
            <span>TF-IDF & Cosine Math</span>
          </button>

          <button
            onClick={() => setActiveTab('code')}
            className={`flex items-center space-x-2 px-4 py-2 text-xs font-medium rounded-lg transition-colors whitespace-nowrap ${
              activeTab === 'code'
                ? 'bg-indigo-600/15 text-indigo-400 border border-indigo-500/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <Code2 className="w-4 h-4" />
            <span>Code Workspace & CSV Editor</span>
          </button>

          <button
            onClick={() => setActiveTab('deploy')}
            className={`flex items-center space-x-2 px-4 py-2 text-xs font-medium rounded-lg transition-colors whitespace-nowrap ${
              activeTab === 'deploy'
                ? 'bg-indigo-600/15 text-indigo-400 border border-indigo-500/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <Terminal className="w-4 h-4" />
            <span>Deployment & Setup</span>
          </button>
        </div>
      </div>
    </header>
  );
};
