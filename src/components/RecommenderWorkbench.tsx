import React, { useState } from 'react';
import { RecommendationApiResponse, RecommendationResult } from '../types';
import { Search, Sparkles, Layers, Database, Server, Cpu, CheckCircle2, ArrowRight, RefreshCw, BarChart2, Tag } from 'lucide-react';

interface RecommenderWorkbenchProps {
  onRecommend: (query: string, topN: number) => Promise<RecommendationApiResponse | null>;
  isLoading: boolean;
  recommendationData: RecommendationApiResponse | null;
}

const PRESET_QUERIES = [
  {
    title: 'Python AI & Machine Learning',
    query: 'Building an end-to-end AI platform using Python, PyTorch, Scikit-Learn, FastAPI microservices, CUDA, and Vector Database for NLP models',
    badge: 'AI / ML'
  },
  {
    title: 'Modern Full-Stack Web App',
    query: 'Full-stack web developer building React Next.js application with TypeScript, Node.js Express REST APIs, PostgreSQL, Tailwind CSS, and Docker',
    badge: 'Web'
  },
  {
    title: 'DevOps & Cloud Orchestration',
    query: 'Kubernetes container orchestration, Terraform infrastructure as code, Go language, CI/CD pipelines, Prometheus and Grafana monitoring',
    badge: 'DevOps'
  },
  {
    title: 'High-Throughput Microservices',
    query: 'Distributed backend architecture in Go, gRPC microservices, Apache Kafka event streaming, Redis caching, PostgreSQL, Envoy proxy',
    badge: 'Backend'
  },
  {
    title: 'Cross-Platform Mobile App',
    query: 'Mobile app development for iOS and Android using Flutter, Dart, SQLite offline storage, Firebase authentication, and fastlane automation',
    badge: 'Mobile'
  },
  {
    title: 'Enterprise Java Services',
    query: 'Enterprise backend system using Java, Spring Boot, Spring Cloud microservices, Hibernate ORM, Oracle DB, PostgreSQL, and Jenkins CI/CD',
    badge: 'Enterprise'
  }
];

export const RecommenderWorkbench: React.FC<RecommenderWorkbenchProps> = ({
  onRecommend,
  isLoading,
  recommendationData
}) => {
  const [queryInput, setQueryInput] = useState<string>(
    'Building an AI microservices backend with Python, FastAPI, PyTorch, PostgreSQL, and Docker containerization'
  );
  const [topN, setTopN] = useState<number>(3);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (queryInput.trim()) {
      onRecommend(queryInput, topN);
    }
  };

  const handleSelectPreset = (presetQuery: string) => {
    setQueryInput(presetQuery);
    onRecommend(presetQuery, topN);
  };

  return (
    <div className="space-y-6">
      
      {/* Search & Query Input Panel */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-base font-semibold text-slate-100 flex items-center gap-2">
              <Search className="w-4 h-4 text-indigo-400" />
              <span>Skill & Project Requirement Prompt</span>
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Enter target job roles, developer skills, programming languages, or framework requirements to calculate TF-IDF Cosine Similarity angles.
            </p>
          </div>
          <span className="text-xs font-mono text-slate-400 bg-slate-800 px-2.5 py-1 rounded-md border border-slate-700">
            TF-IDF Engine Active
          </span>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative">
            <textarea
              rows={3}
              value={queryInput}
              onChange={(e) => setQueryInput(e.target.value)}
              placeholder="e.g. Looking for a high-performance backend using Go, gRPC, PostgreSQL, and Redis for distributed streaming..."
              className="w-full bg-slate-950 border border-slate-800 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 rounded-xl p-4 text-sm text-slate-100 placeholder-slate-500 resize-none outline-none transition-all"
            />
          </div>

          <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4">
            <div className="flex items-center space-x-3">
              <label className="text-xs font-medium text-slate-400">Recommendations Count:</label>
              <select
                value={topN}
                onChange={(e) => setTopN(Number(e.target.value))}
                className="bg-slate-950 border border-slate-800 text-xs text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500"
              >
                <option value={3}>Top 3 Matches</option>
                <option value={5}>Top 5 Matches</option>
                <option value={10}>Top 10 Matches</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={isLoading || !queryInput.trim()}
              className="inline-flex items-center justify-center space-x-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white text-xs font-semibold shadow-lg shadow-indigo-600/25 transition-all disabled:opacity-50"
            >
              {isLoading ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Calculating TF-IDF...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>Compute Tech Recommendations</span>
                </>
              )}
            </button>
          </div>
        </form>

        {/* Preset Query Chips */}
        <div className="mt-5 pt-4 border-t border-slate-800/80">
          <p className="text-xs font-medium text-slate-400 mb-2.5 flex items-center gap-1.5">
            <Tag className="w-3.5 h-3.5 text-indigo-400" />
            <span>Quick Sample Prompts:</span>
          </p>
          <div className="flex flex-wrap gap-2">
            {PRESET_QUERIES.map((preset, idx) => (
              <button
                key={idx}
                onClick={() => handleSelectPreset(preset.query)}
                className="group flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-950 hover:bg-slate-800/80 border border-slate-800 hover:border-slate-700 text-xs text-slate-300 hover:text-white transition-all text-left"
              >
                <span className="px-1.5 py-0.5 text-[10px] font-semibold rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                  {preset.badge}
                </span>
                <span className="font-medium">{preset.title}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Results Display Section */}
      {recommendationData && (
        <div className="space-y-6">
          
          {/* Summary Banner */}
          <div className="bg-slate-900/80 border border-indigo-500/20 rounded-xl p-4 flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 rounded-lg bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
                <BarChart2 className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-xs font-semibold text-slate-200">
                  Calculated TF-IDF Vector Space Analysis
                </h3>
                <p className="text-xs text-slate-400">
                  Processed query cleaned tokens: <code className="bg-slate-950 px-1.5 py-0.5 rounded text-indigo-300 font-mono text-[11px]">{recommendationData.query_cleaned}</code>
                </p>
              </div>
            </div>
            <div className="text-right text-xs text-slate-400">
              Analyzed <span className="text-indigo-400 font-semibold">{recommendationData.total_stacks_analyzed}</span> candidate tech stacks
            </div>
          </div>

          {/* Recommendation Cards Grid */}
          <div className="space-y-4">
            {recommendationData.recommendations.map((item: RecommendationResult) => {
              const isTopRank = item.rank === 1;
              return (
                <div
                  key={item.stack_id}
                  className={`bg-slate-900 border rounded-2xl p-6 transition-all ${
                    isTopRank
                      ? 'border-indigo-500/50 shadow-xl shadow-indigo-500/10 ring-1 ring-indigo-500/20'
                      : 'border-slate-800 hover:border-slate-700'
                  }`}
                >
                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
                    
                    {/* Rank Badge & Title */}
                    <div className="flex items-start space-x-4">
                      <div className={`w-10 h-10 rounded-xl flex items-center justify-center font-bold text-sm ${
                        isTopRank
                          ? 'bg-gradient-to-tr from-indigo-600 to-violet-500 text-white shadow-lg shadow-indigo-500/25'
                          : 'bg-slate-800 text-slate-300 border border-slate-700'
                      }`}>
                        #{item.rank}
                      </div>

                      <div>
                        <div className="flex items-center space-x-2 flex-wrap gap-y-1">
                          <h3 className="text-base font-bold text-slate-100">
                            {item.stack_name}
                          </h3>
                          <span className="px-2.5 py-0.5 text-xs font-medium rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                            {item.category}
                          </span>
                          {isTopRank && (
                            <span className="px-2.5 py-0.5 text-xs font-semibold rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1">
                              <CheckCircle2 className="w-3 h-3" /> Top Match
                            </span>
                          )}
                        </div>
                        <p className="text-xs text-slate-400 mt-1">
                          Roles: <span className="text-slate-300">{item.roles}</span>
                        </p>
                      </div>
                    </div>

                    {/* Similarity Score Percentage */}
                    <div className="flex flex-col items-start md:items-end">
                      <div className="text-xs text-slate-400 mb-1">Cosine Similarity</div>
                      <div className="flex items-baseline space-x-2">
                        <span className={`text-2xl font-black tracking-tight ${
                          isTopRank ? 'text-indigo-400' : 'text-slate-200'
                        }`}>
                          {item.match_percentage}%
                        </span>
                        <span className="text-xs text-slate-400 font-mono">
                          (score: {item.similarity_score})
                        </span>
                      </div>
                      
                      {/* Score Progress Bar */}
                      <div className="w-36 h-2 bg-slate-950 rounded-full overflow-hidden border border-slate-800 mt-1.5">
                        <div
                          className={`h-full rounded-full ${
                            isTopRank
                              ? 'bg-gradient-to-r from-indigo-500 to-violet-400'
                              : 'bg-slate-600'
                          }`}
                          style={{ width: `${Math.min(100, Math.max(5, item.match_percentage))}%` }}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Detailed Spec Grid */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-4 pt-2">
                    
                    {/* Primary Language */}
                    <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800/80">
                      <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1 flex items-center gap-1">
                        <Cpu className="w-3.5 h-3.5 text-indigo-400" /> Primary Lang
                      </div>
                      <div className="text-xs font-semibold text-slate-200">
                        {item.primary_language}
                      </div>
                    </div>

                    {/* Frameworks & Libraries */}
                    <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800/80">
                      <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1 flex items-center gap-1">
                        <Layers className="w-3.5 h-3.5 text-violet-400" /> Frameworks & Libs
                      </div>
                      <div className="text-xs text-slate-200 line-clamp-2">
                        {item.frameworks_libraries}
                      </div>
                    </div>

                    {/* Database & Storage */}
                    <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800/80">
                      <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1 flex items-center gap-1">
                        <Database className="w-3.5 h-3.5 text-cyan-400" /> Database & Storage
                      </div>
                      <div className="text-xs text-slate-200">
                        {item.database_storage}
                      </div>
                    </div>

                    {/* Infrastructure & Tools */}
                    <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800/80">
                      <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1 flex items-center gap-1">
                        <Server className="w-3.5 h-3.5 text-amber-400" /> Infrastructure & Tools
                      </div>
                      <div className="text-xs text-slate-200 line-clamp-2">
                        {item.infrastructure_tools}
                      </div>
                    </div>
                  </div>

                  {/* Skills Description & Matching Terms */}
                  <div className="mt-4 pt-4 border-t border-slate-800/60 space-y-3">
                    <p className="text-xs text-slate-300 leading-relaxed">
                      {item.skills_description}
                    </p>

                    {item.matching_terms && item.matching_terms.length > 0 && (
                      <div className="flex items-center gap-2 flex-wrap pt-1">
                        <span className="text-[11px] font-medium text-slate-400">TF-IDF Overlap Terms:</span>
                        {item.matching_terms.map((t, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-0.5 text-[11px] font-mono rounded bg-indigo-500/10 text-indigo-300 border border-indigo-500/20"
                            title={`Query wt: ${t.query_weight}, Doc wt: ${t.doc_weight}, Contribution: ${t.contribution}`}
                          >
                            {t.term}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
