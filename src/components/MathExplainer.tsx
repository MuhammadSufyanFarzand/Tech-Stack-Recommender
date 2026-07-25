import React from 'react';
import { Cpu, Calculator, CheckCircle2, FileText, ArrowRight, Activity, FunctionSquare } from 'lucide-react';

export const MathExplainer: React.FC = () => {
  return (
    <div className="space-y-6">
      
      {/* Title Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
            <Calculator className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-slate-100">
              Mathematical Pipeline: TF-IDF & Cosine Similarity
            </h2>
            <p className="text-xs text-slate-400">
              How Content-Based Filtering converts unstructured tech skill descriptions into numerical feature vectors.
            </p>
          </div>
        </div>
      </div>

      {/* Grid of Formulas */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* 1. Term Frequency (TF) */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              Step 1: Term Frequency
            </span>
            <FunctionSquare className="w-4 h-4 text-slate-500" />
          </div>
          <h3 className="text-sm font-semibold text-slate-200">
            Sublinear Term Frequency Scaling
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Raw term counts are normalized using sublinear logarithmic scaling to prevent high-frequency terms from overwhelming term weight.
          </p>

          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-center font-mono text-sm text-indigo-300">
            TF(t, d) = 1 + log(f_(t,d))
          </div>

          <p className="text-[11px] text-slate-400">
            Where <code className="text-slate-200">f_(t,d)</code> is the raw occurrence frequency of term <code className="text-slate-200">t</code> in tech stack document <code className="text-slate-200">d</code>.
          </p>
        </div>

        {/* 2. Inverse Document Frequency (IDF) */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono px-2 py-0.5 rounded bg-violet-500/10 text-violet-400 border border-violet-500/20">
              Step 2: Inverse Document Frequency
            </span>
            <Activity className="w-4 h-4 text-slate-500" />
          </div>
          <h3 className="text-sm font-semibold text-slate-200">
            Global Informational Weighting
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Measures how rare or specific a term is across the entire corpus. Common stop words receive near-zero weight.
          </p>

          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-center font-mono text-sm text-violet-300">
            IDF(t) = log((1 + N) / (1 + DF(t))) + 1
          </div>

          <p className="text-[11px] text-slate-400">
            Where <code className="text-slate-200">N</code> is total tech stack profiles and <code className="text-slate-200">DF(t)</code> is document frequency.
          </p>
        </div>

        {/* 3. TF-IDF Matrix */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              Step 3: Vector Space Construction
            </span>
            <Cpu className="w-4 h-4 text-slate-500" />
          </div>
          <h3 className="text-sm font-semibold text-slate-200">
            TF-IDF Feature Representation
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Combines TF and IDF weights into a unified continuous vector space representation.
          </p>

          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-center font-mono text-sm text-cyan-300">
            W(t, d) = TF(t, d) × IDF(t)
          </div>

          <p className="text-[11px] text-slate-400">
            Vectors are L2-normalized: <code className="text-slate-200">v_norm = v / ||v||_2</code>
          </p>
        </div>

        {/* 4. Cosine Similarity */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Step 4: Cosine Similarity Scoring
            </span>
            <CheckCircle2 className="w-4 h-4 text-slate-500" />
          </div>
          <h3 className="text-sm font-semibold text-slate-200">
            Geometric Vector Angle Calculation
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Calculates cosine angle between user prompt vector and tech stack candidate vectors.
          </p>

          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-center font-mono text-sm text-emerald-300">
            cos(θ) = (q · d) / (||q||_2 × ||d||_2)
          </div>

          <p className="text-[11px] text-slate-400">
            Bounded between <code className="text-slate-200">0.0</code> (no term overlap) and <code className="text-slate-200">1.0</code> (identical term weights).
          </p>
        </div>
      </div>

      {/* Execution Flow Steps */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
        <h3 className="text-sm font-bold text-slate-100 mb-2">
          End-to-End System Execution Flow
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800/80 space-y-2">
            <div className="text-xs font-mono font-bold text-indigo-400">01. Ingestion</div>
            <div className="text-xs text-slate-300 font-semibold">Data Parsing</div>
            <p className="text-[11px] text-slate-400">
              Loads <code className="text-indigo-300">raw_skills.csv</code>, cleans punctuation, converts language tokens, filters stop words.
            </p>
          </div>

          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800/80 space-y-2">
            <div className="text-xs font-mono font-bold text-violet-400">02. Vectorizer</div>
            <div className="text-xs text-slate-300 font-semibold">Feature Matrix</div>
            <p className="text-[11px] text-slate-400">
              Transforms text tokens into 500-dimensional TF-IDF feature space and computes IDF weights.
            </p>
          </div>

          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800/80 space-y-2">
            <div className="text-xs font-mono font-bold text-cyan-400">03. Similarity</div>
            <div className="text-xs text-slate-300 font-semibold">Dot Product Norm</div>
            <p className="text-[11px] text-slate-400">
              Computes dot products normalized by L2 norms against all tech stack profiles.
            </p>
          </div>

          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800/80 space-y-2">
            <div className="text-xs font-mono font-bold text-emerald-400">04. Recommendation</div>
            <div className="text-xs text-slate-300 font-semibold">Ranked Match %</div>
            <p className="text-[11px] text-slate-400">
              Sorts top candidates, extracts overlapping feature term weights, and generates spec breakdown.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
