import React from 'react';
import { Globe, Shield, Sparkles, BarChart3, MessageSquare, AlertCircle } from 'lucide-react';
import { Jurisdiction } from '../types';

interface HeaderProps {
  activeTab: 'chat' | 'metrics';
  setActiveTab: (tab: 'chat' | 'metrics') => void;
  jurisdiction: Jurisdiction;
  setJurisdiction: (j: Jurisdiction) => void;
  productCategory: string | null;
  onOpenEscalate: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  setActiveTab,
  jurisdiction,
  setJurisdiction,
  productCategory,
  onOpenEscalate,
}) => {
  return (
    <header className="sticky top-0 z-30 glass-panel border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand & Logo */}
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl ayush-gradient flex items-center justify-center shadow-lg shadow-emerald-900/30 border border-emerald-500/30">
            <Shield className="w-6 h-6 text-emerald-400" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-lg font-bold text-slate-100 tracking-tight">IP-SAKTI Sahayak</h1>
              <span className="text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                SIH 2026 • PS 26045
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">
              Ayurvedic IP & Regulatory Grounded Assistant • Ministry of Ayush
            </p>
          </div>
        </div>

        {/* Center Controls: Jurisdiction Toggle */}
        <div className="flex items-center space-x-2 bg-slate-900/80 p-1 rounded-xl border border-slate-800">
          <button
            id="toggle-jurisdiction-india"
            onClick={() => setJurisdiction('india')}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              jurisdiction === 'india'
                ? 'bg-emerald-600 text-white shadow-sm shadow-emerald-900/50'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <span>🇮🇳</span>
            <span>India Law</span>
          </button>
          <button
            id="toggle-jurisdiction-intl"
            onClick={() => setJurisdiction('international')}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              jurisdiction === 'international'
                ? 'bg-emerald-600 text-white shadow-sm shadow-emerald-900/50'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <Globe className="w-3.5 h-3.5" />
            <span>International Law</span>
          </button>
        </div>

        {/* Right Navigation & Category Badge */}
        <div className="flex items-center space-x-3">
          {productCategory && (
            <div className="hidden lg:flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-amber-500/10 text-amber-300 border border-amber-500/20 text-xs">
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              <span className="truncate max-w-[140px] font-medium">{productCategory}</span>
            </div>
          )}

          {/* Navigation Tabs */}
          <nav className="flex items-center bg-slate-900/80 p-1 rounded-xl border border-slate-800">
            <button
              id="tab-chat"
              onClick={() => setActiveTab('chat')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'chat'
                  ? 'bg-slate-800 text-emerald-400 border border-emerald-500/30'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <MessageSquare className="w-3.5 h-3.5" />
              <span>Assistant</span>
            </button>
            <button
              id="tab-metrics"
              onClick={() => setActiveTab('metrics')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'metrics'
                  ? 'bg-slate-800 text-emerald-400 border border-emerald-500/30'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <BarChart3 className="w-3.5 h-3.5" />
              <span>Eval Dashboard (/metrics)</span>
            </button>
          </nav>

          {/* Escalate to Human Expert */}
          <button
            id="btn-escalate-header"
            onClick={onOpenEscalate}
            className="hidden sm:flex items-center space-x-1 px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-amber-300 text-xs font-semibold border border-amber-500/30 transition-all shadow-sm"
          >
            <AlertCircle className="w-3.5 h-3.5 text-amber-400" />
            <span>Escalate</span>
          </button>
        </div>

      </div>
    </header>
  );
};
