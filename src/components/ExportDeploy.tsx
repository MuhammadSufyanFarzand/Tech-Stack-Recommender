import React from 'react';
import { Download, Terminal, CheckCircle2, Server, Package, Copy, Check } from 'lucide-react';

interface ExportDeployProps {
  onDownloadZip: () => void;
  isDownloadingZip: boolean;
}

export const ExportDeploy: React.FC<ExportDeployProps> = ({
  onDownloadZip,
  isDownloadingZip
}) => {
  const [copiedCmd, setCopiedCmd] = React.useState<string | null>(null);

  const copyToClipboard = (cmd: string, key: string) => {
    navigator.clipboard.writeText(cmd);
    setCopiedCmd(key);
    setTimeout(() => setCopiedCmd(null), 2000);
  };

  const cliSetupCode = `git clone <your-repository-url>
cd tech-stack-recommender
pip install -r requirements.txt
python app.py --cli`;

  const flaskSetupCode = `python app.py`;

  const dockerCode = `docker build -t tech-stack-recommender .
docker run -p 5000:5000 tech-stack-recommender`;

  return (
    <div className="space-y-6">
      
      {/* Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="flex items-center space-x-2">
            <Package className="w-5 h-5 text-indigo-400" />
            <h2 className="text-base font-bold text-slate-100">
              Download Complete Project ZIP Archive
            </h2>
          </div>
          <p className="text-xs text-slate-400 max-w-xl">
            Contains all Python modules (<code className="text-indigo-300">ingestion.py</code>, <code className="text-indigo-300">vectorizer.py</code>, <code className="text-indigo-300">similarity.py</code>), datasets (<code className="text-emerald-300">raw_skills.csv</code>), Flask API runner (<code className="text-indigo-300">app.py</code>), and automated <code className="text-amber-300">create_zip.py</code> script.
          </p>
        </div>

        <button
          onClick={onDownloadZip}
          disabled={isDownloadingZip}
          className="inline-flex items-center space-x-2 px-6 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white font-semibold text-xs shadow-lg shadow-indigo-600/30 transition-all shrink-0 disabled:opacity-50"
        >
          <Download className="w-4 h-4" />
          <span>{isDownloadingZip ? 'Creating ZIP...' : 'Download tech-stack-recommender.zip'}</span>
        </button>
      </div>

      {/* Terminal Setup Guides */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Local CLI Setup */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
              <Terminal className="w-4 h-4 text-indigo-400" />
              <span>1. Run Interactive CLI Mode</span>
            </h3>
            <button
              onClick={() => copyToClipboard(cliSetupCode, 'cli')}
              className="p-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs flex items-center space-x-1"
            >
              {copiedCmd === 'cli' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            </button>
          </div>
          <pre className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs font-mono text-indigo-300 overflow-x-auto">
            {cliSetupCode}
          </pre>
        </div>

        {/* Flask API Server */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
              <Server className="w-4 h-4 text-violet-400" />
              <span>2. Run Flask REST API Server</span>
            </h3>
            <button
              onClick={() => copyToClipboard(flaskSetupCode, 'flask')}
              className="p-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs flex items-center space-x-1"
            >
              {copiedCmd === 'flask' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            </button>
          </div>
          <pre className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs font-mono text-violet-300 overflow-x-auto">
            {flaskSetupCode}
          </pre>
        </div>
      </div>

      {/* Docker Deployment */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
            <Package className="w-4 h-4 text-cyan-400" />
            <span>3. Docker Container Deployment</span>
          </h3>
          <button
            onClick={() => copyToClipboard(dockerCode, 'docker')}
            className="p-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs flex items-center space-x-1"
          >
            {copiedCmd === 'docker' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
          </button>
        </div>
        <pre className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs font-mono text-cyan-300 overflow-x-auto">
          {dockerCode}
        </pre>
      </div>
    </div>
  );
};
