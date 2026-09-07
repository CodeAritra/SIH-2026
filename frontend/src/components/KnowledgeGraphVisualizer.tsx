import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Network, Sparkles, BookOpen, ShieldAlert, FileText, CheckCircle2, 
  Info, ArrowRight, Layers, Award, RefreshCw, AlertTriangle
} from 'lucide-react';
import { HerbInfo, GraphNode, GraphEdge, PathwayResponse } from '../types';

export const KnowledgeGraphVisualizer: React.FC = () => {
  const [availableHerbs, setAvailableHerbs] = useState<HerbInfo[]>([]);
  const [selectedHerbs, setSelectedHerbs] = useState<string[]>(['ashwagandha', 'curcumin']);
  const [pathwayData, setPathwayData] = useState<PathwayResponse | null>(null);
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchHerbs();
  }, []);

  useEffect(() => {
    if (selectedHerbs.length > 0) {
      fetchPathway(selectedHerbs);
    }
  }, []);

  const fetchHerbs = async () => {
    try {
      const res = await axios.get('/api/knowledge-graph/herbs');
      if (res.data?.herbs) {
        setAvailableHerbs(res.data.herbs);
      }
    } catch (err) {
      console.error('Error fetching herbs:', err);
    }
  };

  const fetchPathway = async (herbs: string[]) => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.post('/api/knowledge-graph/pathway', {
        herbs: herbs,
        target_ip: 'patent',
        jurisdiction: 'india'
      });
      setPathwayData(res.data);
      if (res.data.nodes?.length > 0) {
        setSelectedNode(res.data.nodes[0]);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to compute regulatory pathway.');
    } finally {
      setLoading(false);
    }
  };

  const toggleHerb = (herbId: string) => {
    const updated = selectedHerbs.includes(herbId)
      ? selectedHerbs.filter(id => id !== herbId)
      : [...selectedHerbs, herbId];
    setSelectedHerbs(updated);
    if (updated.length > 0) {
      fetchPathway(updated);
    }
  };

  // Compute 2D node layout positions
  const getLayoutPositions = (nodes: GraphNode[]) => {
    const herbs = nodes.filter(n => n.type === 'herb');
    const texts = nodes.filter(n => n.type === 'classical_text');
    const bios = nodes.filter(n => n.type === 'bioactive');
    const statutes = nodes.filter(n => n.type === 'statutory_bar' || n.type === 'regulatory_mandate');

    const positions: Record<string, { x: number; y: number }> = {};

    herbs.forEach((n, idx) => {
      const step = 450 / Math.max(herbs.length, 1);
      positions[n.id] = { x: 80, y: 70 + idx * step };
    });

    texts.forEach((n, idx) => {
      const step = 450 / Math.max(texts.length, 1);
      positions[n.id] = { x: 280, y: 60 + idx * step };
    });

    bios.forEach((n, idx) => {
      const step = 450 / Math.max(bios.length, 1);
      positions[n.id] = { x: 440, y: 80 + idx * step };
    });

    statutes.forEach((n, idx) => {
      const step = 450 / Math.max(statutes.length, 1);
      positions[n.id] = { x: 620, y: 90 + idx * step };
    });

    return positions;
  };

  const positions = pathwayData?.nodes ? getLayoutPositions(pathwayData.nodes) : {};

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-emerald-950/80 via-slate-900 to-indigo-950/80 border border-emerald-500/30 rounded-2xl p-6 shadow-2xl backdrop-blur-md">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-semibold border border-emerald-500/30">
              <Network className="w-3.5 h-3.5" />
              <span>Phase 2: GraphRAG Multi-Hop Regulatory Engine</span>
            </div>
            <h1 className="text-2xl font-bold text-white flex items-center gap-2">
              Ayurvedic Herb & Statutory Knowledge Graph
            </h1>
            <p className="text-slate-300 text-sm max-w-3xl">
              Dynamically maps canonical Ayurvedic herbs to First Schedule classical texts (<em>Charaka</em>, <em>Sushruta</em>, <em>API</em>), 
              calculates Indian Patents Act Section 3(p) TK risk, Section 3(e) Synergistic Admixture mandates, and NBA Section 6 ABS clearances.
            </p>
          </div>

          <button
            onClick={() => fetchPathway(selectedHerbs)}
            disabled={loading || selectedHerbs.length === 0}
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-700 text-white font-medium rounded-xl text-sm shadow-lg shadow-emerald-900/30 transition-all cursor-pointer"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            <span>Recompute Pathways</span>
          </button>
        </div>

        {/* Botanical Selector Chips */}
        <div className="mt-6 pt-5 border-t border-slate-800">
          <label className="text-xs font-semibold uppercase tracking-wider text-slate-400 block mb-2">
            Select Active Botanical Ingredients for Formulation Testing:
          </label>
          <div className="flex flex-wrap gap-2">
            {availableHerbs.map((h) => {
              const isSelected = selectedHerbs.includes(h.id);
              return (
                <button
                  key={h.id}
                  onClick={() => toggleHerb(h.id)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1.5 cursor-pointer border ${
                    isSelected
                      ? 'bg-emerald-500/30 text-emerald-200 border-emerald-400 shadow-sm'
                      : 'bg-slate-800/80 text-slate-400 border-slate-700 hover:border-slate-500 hover:text-slate-200'
                  }`}
                >
                  <span className={`w-2 h-2 rounded-full ${isSelected ? 'bg-emerald-400 animate-pulse' : 'bg-slate-600'}`} />
                  <span>{h.common_name}</span>
                  <span className="text-[10px] text-slate-400 italic">({h.botanical_name.split(' ')[0]})</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Main Visualizer & Decision Card Split */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Visual Graph Canvas */}
        <div className="lg:col-span-8 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div className="flex items-center gap-2">
              <Layers className="w-4 h-4 text-emerald-400" />
              <h2 className="text-sm font-semibold text-slate-200">Interactive Statutory Regulatory Path Canvas</h2>
            </div>
            {/* Legend */}
            <div className="hidden sm:flex items-center gap-3 text-[11px] text-slate-400">
              <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-emerald-500" /> Herb</span>
              <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-purple-500" /> Classical Text</span>
              <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-cyan-500" /> Bioactive</span>
              <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-red-500" /> Statutory Bar</span>
              <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-orange-500" /> NBA Mandate</span>
            </div>
          </div>

          <div className="relative w-full h-[480px] bg-slate-950/60 rounded-xl overflow-hidden mt-4 border border-slate-800/80">
            {loading ? (
              <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 text-slate-400 bg-slate-950/80">
                <RefreshCw className="w-8 h-8 animate-spin text-emerald-400" />
                <p className="text-sm">Calculating multi-hop statutory graph pathways...</p>
              </div>
            ) : error ? (
              <div className="absolute inset-0 flex items-center justify-center text-red-400 p-6 text-center">
                <AlertTriangle className="w-6 h-6 mr-2" />
                <span>{error}</span>
              </div>
            ) : pathwayData && pathwayData.nodes.length > 0 ? (
              <svg className="w-full h-full" viewBox="0 0 760 480">
                {/* Edges */}
                {pathwayData.edges.map((edge, idx) => {
                  const p1 = positions[edge.source];
                  const p2 = positions[edge.target];
                  if (!p1 || !p2) return null;
                  return (
                    <g key={idx}>
                      <line
                        x1={p1.x}
                        y1={p1.y}
                        x2={p2.x}
                        y2={p2.y}
                        stroke={edge.color || '#64748b'}
                        strokeWidth="1.8"
                        strokeDasharray={edge.label.includes('BAR') ? '4,4' : 'none'}
                        opacity="0.6"
                      />
                    </g>
                  );
                })}

                {/* Nodes */}
                {pathwayData.nodes.map((node) => {
                  const pos = positions[node.id];
                  if (!pos) return null;
                  const isSelected = selectedNode?.id === node.id;
                  return (
                    <g
                      key={node.id}
                      transform={`translate(${pos.x}, ${pos.y})`}
                      onClick={() => setSelectedNode(node)}
                      className="cursor-pointer group"
                    >
                      <circle
                        r={isSelected ? '22' : '18'}
                        fill={node.color}
                        className="transition-all duration-200 group-hover:scale-110 drop-shadow-md"
                        stroke={isSelected ? '#ffffff' : '#0f172a'}
                        strokeWidth={isSelected ? '3' : '2'}
                      />
                      <text
                        y="34"
                        textAnchor="middle"
                        fill="#e2e8f0"
                        fontSize="11"
                        fontWeight="600"
                        className="select-none pointer-events-none drop-shadow"
                      >
                        {node.label.length > 18 ? node.label.slice(0, 16) + '...' : node.label}
                      </text>
                    </g>
                  );
                })}
              </svg>
            ) : null}
          </div>

          {/* Node Quick Inspector */}
          {selectedNode && (
            <div className="mt-4 p-4 rounded-xl bg-slate-800/70 border border-slate-700/60 flex items-start gap-3">
              <Info className="w-5 h-5 text-emerald-400 mt-0.5 shrink-0" />
              <div className="text-xs space-y-1">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-slate-100 text-sm">{selectedNode.label}</span>
                  <span className="px-2 py-0.5 rounded bg-slate-700 text-slate-300 uppercase font-mono text-[10px]">
                    {selectedNode.type}
                  </span>
                </div>
                <p className="text-slate-300">{selectedNode.sublabel}</p>
                {selectedNode.details && (
                  <div className="text-slate-400 pt-1">
                    {Object.entries(selectedNode.details).map(([k, v]) => (
                      <span key={k} className="mr-3">
                        <strong className="text-slate-300 capitalize">{k}:</strong> {Array.isArray(v) ? v.join(', ') : String(v)}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Statutory Regulatory Strategy & Findings */}
        <div className="lg:col-span-4 space-y-4">
          {pathwayData?.pathway_summary ? (
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
              <div className="flex items-center gap-2 pb-2 border-b border-slate-800">
                <ShieldAlert className="w-5 h-5 text-emerald-400" />
                <h3 className="font-bold text-white text-base">Regulatory Decision Matrix</h3>
              </div>

              {/* Status Pills */}
              <div className="space-y-2.5 text-xs">
                <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/60 border border-slate-800">
                  <span className="text-slate-400">Section 3(p) TK Bar Risk:</span>
                  <span className={`font-bold px-2 py-0.5 rounded ${
                    pathwayData.pathway_summary.sec_3p_tk_risk === 'High'
                      ? 'bg-red-500/20 text-red-300 border border-red-500/30'
                      : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                  }`}>
                    {pathwayData.pathway_summary.sec_3p_tk_risk} Risk
                  </span>
                </div>

                <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/60 border border-slate-800">
                  <span className="text-slate-400">Section 3(e) Synergism:</span>
                  <span className="font-bold px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30">
                    {pathwayData.pathway_summary.sec_3e_synergy_mandate}
                  </span>
                </div>

                <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/60 border border-slate-800">
                  <span className="text-slate-400">NBA Section 6 ABS Form:</span>
                  <span className="font-bold px-2 py-0.5 rounded bg-orange-500/20 text-orange-300 border border-orange-500/30">
                    {pathwayData.pathway_summary.nba_approval_required ? 'Form III Required' : 'Not Required'}
                  </span>
                </div>
              </div>

              {/* GI Tagging Opportunities */}
              {pathwayData.pathway_summary.gi_opportunities.length > 0 && (
                <div className="p-3 rounded-xl bg-purple-950/30 border border-purple-800/40 text-xs space-y-1">
                  <div className="flex items-center gap-1.5 font-bold text-purple-300">
                    <Award className="w-4 h-4" />
                    <span>Geographical Indication (GI) Pointers</span>
                  </div>
                  {pathwayData.pathway_summary.gi_opportunities.map((g, i) => (
                    <p key={i} className="text-slate-300">
                      <strong>{g.herb}:</strong> {g.gi}
                    </p>
                  ))}
                </div>
              )}

              {/* Recommended Filing Roadmap */}
              <div className="p-3.5 rounded-xl bg-slate-950/80 border border-emerald-900/30 space-y-2 text-xs">
                <div className="flex items-center gap-1.5 font-bold text-emerald-400">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Statutory Filing Roadmap</span>
                </div>
                <div className="text-slate-300 whitespace-pre-line leading-relaxed">
                  {pathwayData.pathway_summary.recommended_path}
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 text-center text-slate-400 text-sm">
              Select botanical herbs and click Recompute to inspect statutory pathways.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
