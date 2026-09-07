import React, { useState } from 'react';
import axios from 'axios';
import { 
  FlaskConical, Sparkles, AlertOctagon, CheckCircle2, 
  HelpCircle, BarChart3, FileSpreadsheet, ShieldCheck, ArrowRight, Layers
} from 'lucide-react';
import { SynergyResult } from '../types';

const POPULAR_HERBS = [
  'Ashwagandha', 'Curcumin', 'Brahmi', 'Tulsi', 'Guduchi', 
  'Shatavari', 'Triphala', 'Neem', 'Pippali', 'Kalmegh'
];

export const SynergyAnalyzer: React.FC = () => {
  const [selectedHerbs, setSelectedHerbs] = useState<string[]>(['Ashwagandha', 'Curcumin', 'Pippali']);
  const [extractionMethod, setExtractionMethod] = useState<string>('Hydroalcoholic Standardized Extract (95% Purity)');
  const [claim, setClaim] = useState<string>('Enhanced Bioavailability & Synergistic Anti-inflammatory Response');
  const [hasData, setHasData] = useState<boolean>(true);
  const [ciValue, setCiValue] = useState<number>(0.68);
  const [result, setResult] = useState<SynergyResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const runEvaluation = async () => {
    setLoading(true);
    try {
      const res = await axios.post('/api/knowledge-graph/synergy-check', {
        herbs: selectedHerbs,
        extraction_method: extractionMethod,
        therapeutic_claim: claim,
        has_experimental_data: hasData,
        combination_index: hasData ? ciValue : null
      });
      setResult(res.data);
    } catch (err) {
      console.error('Synergy evaluation error:', err);
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    runEvaluation();
  }, []);

  const toggleHerb = (herb: string) => {
    if (selectedHerbs.includes(herb)) {
      setSelectedHerbs(selectedHerbs.filter(h => h !== herb));
    } else {
      setSelectedHerbs([...selectedHerbs, herb]);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-blue-950/80 via-slate-900 to-indigo-950/80 border border-blue-500/30 rounded-2xl p-6 shadow-2xl backdrop-blur-md">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 text-xs font-semibold border border-blue-500/30">
              <FlaskConical className="w-3.5 h-3.5" />
              <span>Section 3(e) Synergism & Non-Obviousness Assistant</span>
            </div>
            <h1 className="text-2xl font-bold text-white flex items-center gap-2">
              Ayurvedic Synergy & Patentability Analyzer
            </h1>
            <p className="text-slate-300 text-sm max-w-3xl">
              Under Section 3(e) of the Indian Patents Act 1970, combining known Ayurvedic substances is barred as a <em>"mere admixture"</em> unless you prove non-obvious synergistic efficacy ($CI &lt; 1.0$).
            </p>
          </div>

          <button
            onClick={runEvaluation}
            disabled={loading || selectedHerbs.length === 0}
            className="inline-flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 text-white font-medium rounded-xl text-sm shadow-lg shadow-blue-900/30 transition-all cursor-pointer"
          >
            <Sparkles className="w-4 h-4" />
            <span>{loading ? 'Evaluating...' : 'Run Synergy Evaluation'}</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Input Formulation Form */}
        <div className="lg:col-span-5 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-5">
          <h2 className="text-sm font-semibold text-slate-200 flex items-center gap-2 pb-2 border-b border-slate-800">
            <Layers className="w-4 h-4 text-blue-400" />
            <span>Formulation Parameters</span>
          </h2>

          {/* Herb Chips */}
          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-400 block">
              Active Botanical Combination ({selectedHerbs.length} selected):
            </label>
            <div className="flex flex-wrap gap-2">
              {POPULAR_HERBS.map((h) => {
                const isSel = selectedHerbs.includes(h);
                return (
                  <button
                    key={h}
                    onClick={() => toggleHerb(h)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all cursor-pointer ${
                      isSel
                        ? 'bg-blue-500/30 text-blue-200 border-blue-400 shadow-sm'
                        : 'bg-slate-800/80 text-slate-400 border-slate-700 hover:border-slate-500'
                    }`}
                  >
                    {h}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Extraction Process */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-400 block">Extraction / Processing Method:</label>
            <select
              value={extractionMethod}
              onChange={(e) => setExtractionMethod(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-xs focus:border-blue-500 outline-none"
            >
              <option value="Hydroalcoholic Standardized Extract (95% Purity)">Hydroalcoholic Standardized Fraction (Enriched)</option>
              <option value="Supercritical Fluid CO2 Fractionation">Supercritical Fluid CO2 Selective Fractionation</option>
              <option value="Liposomal Nanocarrier Delivery Complex">Liposomal / Phospholipid Nanocarrier Complex</option>
              <option value="Traditional Aqueous Decoction (Kwatha / Churna)">Traditional Aqueous Decoction (Kwatha / Churna)</option>
            </select>
          </div>

          {/* Therapeutic Claim */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-400 block">Target Therapeutic Claim:</label>
            <input
              type="text"
              value={claim}
              onChange={(e) => setClaim(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-xs focus:border-blue-500 outline-none"
              placeholder="e.g. Cognitive enhancement & stress reduction"
            />
          </div>

          {/* Experimental Data Toggle */}
          <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800/80 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-300">Have Quantitative Bioassay Data?</span>
              <input
                type="checkbox"
                checked={hasData}
                onChange={(e) => setHasData(e.target.checked)}
                className="w-4 h-4 accent-blue-500 cursor-pointer"
              />
            </div>

            {hasData && (
              <div className="space-y-2 pt-2 border-t border-slate-800">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Chou-Talalay Combination Index ($CI$):</span>
                  <span className={`font-bold font-mono ${ciValue < 1 ? 'text-emerald-400' : 'text-red-400'}`}>
                    CI = {ciValue} ({ciValue < 0.9 ? 'Synergistic' : ciValue > 1.1 ? 'Antagonistic' : 'Additive'})
                  </span>
                </div>
                <input
                  type="range"
                  min="0.3"
                  max="1.8"
                  step="0.05"
                  value={ciValue}
                  onChange={(e) => setCiValue(parseFloat(e.target.value))}
                  className="w-full accent-blue-500 cursor-pointer"
                />
                <div className="flex justify-between text-[10px] text-slate-400 font-mono">
                  <span>0.3 (Strong Synergy)</span>
                  <span>1.0 (Additive Barred)</span>
                  <span>1.8 (Antagonistic)</span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Results & Statutory Risk Radar */}
        <div className="lg:col-span-7 space-y-4">
          {result ? (
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5">
              {/* Verdict Banner */}
              <div className={`p-4 rounded-xl border flex items-center gap-3 ${
                result.verdict_color === 'emerald'
                  ? 'bg-emerald-950/40 border-emerald-500/40 text-emerald-200'
                  : result.verdict_color === 'red'
                  ? 'bg-red-950/40 border-red-500/40 text-red-200'
                  : 'bg-amber-950/40 border-amber-500/40 text-amber-200'
              }`}>
                <ShieldCheck className="w-6 h-6 shrink-0" />
                <div>
                  <h3 className="font-bold text-sm">Patentability & Synergy Verdict:</h3>
                  <p className="text-xs font-semibold">{result.patentability_verdict}</p>
                </div>
              </div>

              {/* Risk Radar Bars */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                  Statutory Patentability Risk Radar:
                </h4>
                
                <div className="space-y-2 text-xs">
                  <div>
                    <div className="flex justify-between mb-1 text-slate-400">
                      <span>Section 3(p) Traditional Knowledge Bar:</span>
                      <span className="font-bold text-slate-200">{result.risk_radar.sec_3p_traditional_knowledge_risk}% Risk</span>
                    </div>
                    <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
                      <div className="h-full bg-red-500 rounded-full" style={{ width: `${result.risk_radar.sec_3p_traditional_knowledge_risk}%` }} />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between mb-1 text-slate-400">
                      <span>Section 3(e) Mere Admixture Bar:</span>
                      <span className="font-bold text-slate-200">{result.risk_radar.sec_3e_mere_admixture_risk}% Risk</span>
                    </div>
                    <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
                      <div className="h-full bg-blue-500 rounded-full" style={{ width: `${result.risk_radar.sec_3e_mere_admixture_risk}%` }} />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between mb-1 text-slate-400">
                      <span>NBA Biological Diversity Clearance Mandate:</span>
                      <span className="font-bold text-slate-200">{result.risk_radar.nba_abs_clearance_mandate}% Trigger</span>
                    </div>
                    <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
                      <div className="h-full bg-orange-500 rounded-full" style={{ width: `${result.risk_radar.nba_abs_clearance_mandate}%` }} />
                    </div>
                  </div>
                </div>
              </div>

              {/* Recommended Route */}
              <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 text-xs space-y-1.5">
                <span className="font-bold text-emerald-400 block">Recommended Commercial IP Filing Strategy:</span>
                <p className="text-slate-300 leading-relaxed">{result.recommended_ip_filing_route}</p>
              </div>

              {/* Experimental Protocol Checklist */}
              <div className="space-y-2">
                <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                  <FileSpreadsheet className="w-4 h-4 text-blue-400" />
                  <span>Mandatory Experimental Evidentiary Protocol for Patent Examination:</span>
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                  {result.protocol_steps.map((step, idx) => (
                    <div key={idx} className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 text-xs space-y-1">
                      <span className="font-bold text-slate-200 text-[11px] block">{step.step}</span>
                      <p className="text-slate-400 text-[11px] leading-relaxed">{step.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
};
