import React, { useState, useEffect } from 'react';
import { ProjectFile } from '../types';
import { Folder, FileCode, Save, Copy, Check, RefreshCw, FileSpreadsheet, Code2 } from 'lucide-react';

interface CodeExplorerProps {
  files: ProjectFile[];
  onRefreshFiles: () => void;
  onSaveFile: (relativePath: string, content: string) => Promise<boolean>;
}

export const CodeExplorer: React.FC<CodeExplorerProps> = ({
  files,
  onRefreshFiles,
  onSaveFile
}) => {
  const [selectedFilePath, setSelectedFilePath] = useState<string>('');
  const [fileContent, setFileContent] = useState<string>('');
  const [isCopied, setIsCopied] = useState<boolean>(false);
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [saveSuccess, setSaveSuccess] = useState<boolean>(false);

  // Default select first Python or CSV file
  useEffect(() => {
    if (files.length > 0 && !selectedFilePath) {
      const csvOrPyFile = files.find(f => f.type === 'file' && (f.relativePath.endsWith('app.py') || f.relativePath.endsWith('raw_skills.csv')));
      const target = csvOrPyFile || files.find(f => f.type === 'file');
      if (target) {
        setSelectedFilePath(target.relativePath);
        setFileContent(target.content || '');
      }
    }
  }, [files, selectedFilePath]);

  const handleSelectFile = (file: ProjectFile) => {
    if (file.type === 'file') {
      setSelectedFilePath(file.relativePath);
      setFileContent(file.content || '');
      setSaveSuccess(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(fileContent);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  const handleSave = async () => {
    if (!selectedFilePath) return;
    setIsSaving(true);
    const ok = await onSaveFile(selectedFilePath, fileContent);
    setIsSaving(false);
    if (ok) {
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 2500);
    }
  };

  const activeFileObj = files.find(f => f.relativePath === selectedFilePath);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl grid grid-cols-1 lg:grid-cols-12 min-h-[600px]">
      
      {/* File Tree Sidebar */}
      <div className="lg:col-span-4 border-r border-slate-800 p-4 bg-slate-950/80 flex flex-col justify-between">
        <div>
          <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-800">
            <div className="flex items-center space-x-2">
              <Folder className="w-4 h-4 text-indigo-400" />
              <span className="text-xs font-bold text-slate-200">tech-stack-recommender/</span>
            </div>
            <button
              onClick={onRefreshFiles}
              className="p-1 rounded text-slate-400 hover:text-slate-200 hover:bg-slate-800"
              title="Refresh file tree"
            >
              <RefreshCw className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* File List */}
          <div className="space-y-1 overflow-y-auto max-h-[500px]">
            {files.map((file) => {
              const isSelected = file.relativePath === selectedFilePath;
              const isCsv = file.relativePath.endsWith('.csv');
              const isPy = file.relativePath.endsWith('.py');

              return (
                <button
                  key={file.relativePath}
                  onClick={() => handleSelectFile(file)}
                  className={`w-full flex items-center space-x-2.5 px-3 py-2 rounded-lg text-xs transition-all text-left font-mono ${
                    isSelected
                      ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/30 font-semibold'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`}
                >
                  {isCsv ? (
                    <FileSpreadsheet className="w-4 h-4 text-emerald-400 shrink-0" />
                  ) : isPy ? (
                    <FileCode className="w-4 h-4 text-amber-400 shrink-0" />
                  ) : (
                    <Code2 className="w-4 h-4 text-slate-400 shrink-0" />
                  )}
                  <span className="truncate">{file.relativePath}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Info footer */}
        <div className="pt-4 border-t border-slate-800 text-[11px] text-slate-500">
          Editable workspace. You can modify <code className="text-emerald-400">raw_skills.csv</code> or Python logic and click <span className="text-indigo-400 font-semibold">Save File</span> to retrain the recommender live.
        </div>
      </div>

      {/* Code Editor / Viewer */}
      <div className="lg:col-span-8 flex flex-col bg-slate-950">
        
        {/* Editor Toolbar */}
        <div className="flex items-center justify-between px-4 py-3 bg-slate-900 border-b border-slate-800">
          <div className="flex items-center space-x-2 font-mono text-xs text-slate-300">
            <span className="text-slate-500">path:</span>
            <span className="font-semibold text-indigo-300">{selectedFilePath || 'Select a file'}</span>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={handleCopy}
              className="inline-flex items-center space-x-1.5 px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
            >
              {isCopied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{isCopied ? 'Copied' : 'Copy'}</span>
            </button>

            <button
              onClick={handleSave}
              disabled={isSaving || !selectedFilePath}
              className="inline-flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition-colors disabled:opacity-50"
            >
              {isSaving ? (
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
              ) : saveSuccess ? (
                <Check className="w-3.5 h-3.5 text-emerald-300" />
              ) : (
                <Save className="w-3.5 h-3.5" />
              )}
              <span>{saveSuccess ? 'Saved & Retrained!' : 'Save File'}</span>
            </button>
          </div>
        </div>

        {/* Textarea Code Content */}
        <div className="flex-1 p-4 font-mono text-xs text-slate-200 leading-relaxed overflow-auto">
          <textarea
            value={fileContent}
            onChange={(e) => setFileContent(e.target.value)}
            spellCheck={false}
            className="w-full h-full min-h-[500px] bg-transparent text-slate-200 outline-none resize-none font-mono"
          />
        </div>
      </div>
    </div>
  );
};
