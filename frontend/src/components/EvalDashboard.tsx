import React, { useState, useEffect } from 'react';
import { BarChart3, Play, CheckCircle2, XCircle, AlertTriangle, ShieldCheck, Database, RefreshCw, FileText } from 'lucide-react';
import axios from 'axios';
import { EvalRun, QueryLog } from '../types';

export const EvalDashboard: React.FC = () => {
  const [runs, setRuns] = useState<EvalRun[]>([]);
  const [selectedRun, setSelectedRun] = useState<EvalRun | null>(null);
  const [recentLogs, setRecentLogs] = useState<QueryLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [runningBenchmark, setRunningBenchmark] = useState(false);
  const [activeSubTab, setActiveSubTab] = useState<'benchmark' | 'audit'>('benchmark');

  const fetchMetrics = async () => {
    setLoading(true);
    try {
      const res = await axios.get('/api/metrics');
      setRuns(res.data.eval_runs || []);
      setRecentLogs(res.data.recent_logs || []);
      if (res.data.eval_runs && res.data.eval_runs.length > 0) {
        setSelectedRun(res.data.eval_runs[0]);
      }
    } catch (err) {
      console.error("Failed to fetch evaluation metrics:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
  }, []);

  const handleRunBenchmark = async () => {
    setRunningBenchmark(true);
    try {
      const res = await axios.post('/api/metrics/run', { run_name: `Benchmark Run ${new Date().toLocaleTimeString()}` });
      await fetchMetrics();
    } catch (err) {
      console.error("Benchmark run failed:", err);
    } finally {
      setRunningBenchmark(false);
    }
  };

  return (
    <div className="flex-1 max-w-7xl mx-auto w-full p-6 space-y-6 overflow-y-auto">
      
      {/* Dashboard Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 glass-panel p-5 rounded-2xl border border-slate-800">
        <div>
          <div className="flex items-center space-x-2">
            <BarChart3 className="w-5 h-5 text-emerald-400" />
            <h2 className="text-base font-bold text-slate-100">Retrieval & Citation Quality Dashboard</h2>
            <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-semibold border border-emerald-500/30">
              Dev Metric Tools
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Track Precision@k, MRR, Citation Validity, and Safe Abstention Rates across benchmark queries.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={fetchMetrics}
            disabled={loading}
            className="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold border border-slate-700 transition-all"
            title="Refresh metrics"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>

          <button
            id="btn-run-benchmark"
            onClick={handleRunBenchmark}
            disabled={runningBenchmark}
            className="flex items-center space-x-2 px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shadow-lg shadow-emerald-950/50 transition-all disabled:opacity-50"
          >
            <Play className="w-4 h-4" />
            <span>{runningBenchmark ? 'Executing Benchmark...' : 'Run Benchmark Evaluation'}</span>
          </button>
        </div>
      </div>

      {/* Metric Cards Overview */}
      {selectedRun ? (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
          <div className="glass-card p-4 rounded-2xl border border-slate-800 space-y-1">
            <div className="text-[11px] font-semibold text-slate-400">Precision@k (k=5)</div>
            <div className="text-2xl font-extrabold text-emerald-400">
              {(selectedRun.precision_at_k * 100).toFixed(1)}%
            </div>
            <div className="text-[10px] text-slate-500">Correct chunk in top 5</div>
          </div>

          <div className="glass-card p-4 rounded-2xl border border-slate-800 space-y-1">
            <div className="text-[11px] font-semibold text-slate-400">Recall@k (k=5)</div>
            <div className="text-2xl font-extrabold text-emerald-400">
              {(selectedRun.recall_at_k * 100).toFixed(1)}%
            </div>
            <div className="text-[10px] text-slate-500">Target corpus recall</div>
          </div>

          <div className="glass-card p-4 rounded-2xl border border-slate-800 space-y-1">
            <div className="text-[11px] font-semibold text-slate-400">Mean Reciprocal Rank</div>
            <div className="text-2xl font-extrabold text-amber-400">
              {selectedRun.mrr.toFixed(3)}
            </div>
            <div className="text-[10px] text-slate-500">Average reciprocal rank</div>
          </div>

          <div className="glass-card p-4 rounded-2xl border border-slate-800 space-y-1">
            <div className="text-[11px] font-semibold text-slate-400">Citation Validity Rate</div>
            <div className="text-2xl font-extrabold text-emerald-400">
              {(selectedRun.citation_validity_rate * 100).toFixed(1)}%
            </div>
            <div className="text-[10px] text-slate-500">Grounded claims passed</div>
          </div>

          <div className="glass-card p-4 rounded-2xl border border-slate-800 space-y-1">
            <div className="text-[11px] font-semibold text-slate-400">Abstention Accuracy</div>
            <div className="text-2xl font-extrabold text-emerald-400">
              {(selectedRun.abstention_rate * 100).toFixed(1)}%
            </div>
            <div className="text-[10px] text-slate-500">Out-of-corpus blocked</div>
          </div>
        </div>
      ) : (
        <div className="text-center py-6 text-xs text-slate-500">
          No benchmark runs available yet. Click 'Run Benchmark Evaluation' above.
        </div>
      )}

      {/* Sub Tab Navigation */}
      <div className="flex items-center space-x-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveSubTab('benchmark')}
          className={`flex items-center space-x-1.5 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
            activeSubTab === 'benchmark'
              ? 'bg-slate-800 text-emerald-400 border border-emerald-500/30'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <FileText className="w-4 h-4" />
          <span>Benchmark Query Breakdown</span>
        </button>
        <button
          onClick={() => setActiveSubTab('audit')}
          className={`flex items-center space-x-1.5 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
            activeSubTab === 'audit'
              ? 'bg-slate-800 text-emerald-400 border border-emerald-500/30'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Database className="w-4 h-4" />
          <span>Live Query Audit Trail ({recentLogs.length})</span>
        </button>
      </div>

      {/* Tab 1: Benchmark Breakdown Table */}
      {activeSubTab === 'benchmark' && selectedRun && (
        <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden shadow-xl">
          <div className="p-4 border-b border-slate-800 flex items-center justify-between">
            <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">
              {selectedRun.run_name} — {new Date(selectedRun.timestamp).toLocaleString()}
            </h3>
            <span className="text-xs text-slate-400 font-semibold">
              Total Benchmark Queries: {selectedRun.total_queries}
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-900/80 text-slate-400 uppercase text-[10px] font-bold border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">Query</th>
                  <th className="py-3 px-4">Jurisdiction</th>
                  <th className="py-3 px-4">Expected Target</th>
                  <th className="py-3 px-4 text-center">Retrieval Hit</th>
                  <th className="py-3 px-4 text-center">Top Similarity</th>
                  <th className="py-3 px-4 text-center">Citation Gate</th>
                  <th className="py-3 px-4 text-center">Overall Result</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {selectedRun.details.map((item, idx) => (
                  <tr key={idx} className="hover:bg-slate-900/40 transition-colors">
                    <td className="py-3 px-4 font-medium text-slate-100 max-w-xs truncate">
                      {item.query}
                    </td>
                    <td className="py-3 px-4 capitalize">
                      {item.jurisdiction === 'india' ? '🇮🇳 India' : '🌐 Intl'}
                    </td>
                    <td className="py-3 px-4 text-[11px] text-slate-400">
                      {item.expected_source ? `${item.expected_source} (${item.expected_section})` : 'Out-of-Corpus (Abstain)'}
                    </td>
                    <td className="py-3 px-4 text-center">
                      {item.expected_source ? (
                        item.hit_found ? (
                          <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-400 font-bold border border-emerald-500/30">
                            HIT (Rank #{item.rank})
                          </span>
                        ) : (
                          <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] bg-rose-500/20 text-rose-400 font-bold border border-rose-500/30">
                            MISS
                          </span>
                        )
                      ) : (
                        <span className="text-[10px] text-slate-500">N/A</span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-center font-semibold text-slate-200">
                      {(item.top_score * 100).toFixed(0)}%
                    </td>
                    <td className="py-3 px-4 text-center">
                      {item.is_valid_citation ? (
                        <span className="text-emerald-400 font-semibold">Valid</span>
                      ) : (
                        <span className="text-amber-400 font-semibold">Abstained</span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-center">
                      {item.correct_behavior ? (
                        <span className="inline-flex items-center space-x-1 text-emerald-400 font-bold text-[11px]">
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          <span>PASS</span>
                        </span>
                      ) : (
                        <span className="inline-flex items-center space-x-1 text-rose-400 font-bold text-[11px]">
                          <XCircle className="w-3.5 h-3.5" />
                          <span>FAIL</span>
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab 2: Live Query Audit Trail */}
      {activeSubTab === 'audit' && (
        <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden shadow-xl">
          <div className="p-4 border-b border-slate-800">
            <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">
              Recent Live Query Audit Trail (SQLite)
            </h3>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-900/80 text-slate-400 uppercase text-[10px] font-bold border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">Timestamp</th>
                  <th className="py-3 px-4">User Query</th>
                  <th className="py-3 px-4">Jurisdiction</th>
                  <th className="py-3 px-4">Product Category</th>
                  <th className="py-3 px-4 text-center">Confidence</th>
                  <th className="py-3 px-4 text-center">Hard Block Gate</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {recentLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-900/40 transition-colors">
                    <td className="py-3 px-4 text-[11px] text-slate-400">
                      {new Date(log.timestamp).toLocaleTimeString()}
                    </td>
                    <td className="py-3 px-4 font-medium text-slate-100 max-w-xs truncate">
                      {log.user_query}
                    </td>
                    <td className="py-3 px-4 capitalize">
                      {log.jurisdiction === 'india' ? '🇮🇳 India' : '🌐 Intl'}
                    </td>
                    <td className="py-3 px-4 text-[11px] text-slate-400">
                      {log.classification || 'Unspecified'}
                    </td>
                    <td className="py-3 px-4 text-center">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        log.confidence === 'High' ? 'badge-high' : log.confidence === 'Medium' ? 'badge-medium' : 'badge-low'
                      }`}>
                        {log.confidence}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-center">
                      {log.is_blocked ? (
                        <span className="text-rose-400 font-bold text-[11px] inline-flex items-center space-x-1">
                          <XCircle className="w-3.5 h-3.5" />
                          <span>BLOCKED</span>
                        </span>
                      ) : (
                        <span className="text-emerald-400 font-bold text-[11px] inline-flex items-center space-x-1">
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          <span>PASSED</span>
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

    </div>
  );
};
