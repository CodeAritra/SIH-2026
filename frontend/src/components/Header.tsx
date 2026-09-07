
import React from 'react';
import { 
  Globe, Shield, Sparkles, BarChart3, MessageSquare, 
  AlertCircle, Network, FlaskConical, Lock, Languages 
} from 'lucide-react';
import { Jurisdiction, ActiveTab } from '../types';

interface HeaderProps {
  activeTab: ActiveTab;
  setActiveTab: (tab: ActiveTab) => void;
  jurisdiction: Jurisdiction;
  setJurisdiction: (j: Jurisdiction) => void;
  productCategory: string | null;
  onOpenEscalate: () => void;
  selectedLanguage: string;
  setSelectedLanguage: (lang: string) => void;
}

const LANGUAGES = [
  { code: 'en', name: 'English', native: 'English' },
  { code: 'hi', name: 'Hindi', native: 'हिन्दी' },
  { code: 'bn', name: 'Bengali', native: 'বাংলা' },
  { code: 'ta', name: 'Tamil', native: 'தமிழ்' },
  { code: 'te', name: 'Telugu', native: 'తెలుగు' },
  { code: 'mr', name: 'Marathi', native: 'मराठी' },
  { code: 'gu', name: 'Gujarati', native: 'ગુજરાતી' },
  { code: 'kn', name: 'Kannada', native: 'ಕನ್ನಡ' },
  { code: 'ml', name: 'Malayalam', native: 'മലയാളം' },
  { code: 'pa', name: 'Punjabi', native: 'ਪੰਜਾਬੀ' },
  { code: 'or', name: 'Odia', native: 'ଓଡ଼ିଆ' }
];

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  setActiveTab,
  jurisdiction,
  setJurisdiction,
  productCategory,
  onOpenEscalate,
  selectedLanguage,
  setSelectedLanguage
}) => {
  return (
    <header className="sticky top-0 z-30 glass-panel border-b border-slate-800 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-2">
        
        {/* Brand & Logo */}
        <div className="flex items-center space-x-3 shrink-0">
          <div className="w-10 h-10 rounded-xl ayush-gradient flex items-center justify-center shadow-lg shadow-emerald-900/30 border border-emerald-500/30">
            <Shield className="w-6 h-6 text-emerald-400" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-base sm:text-lg font-bold text-slate-100 tracking-tight">IP-SAKTI Sahayak</h1>
              <span className="text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 hidden sm:inline-block">
                SIH 2026 • PS 26045
              </span>
            </div>
            <p className="text-[11px] text-slate-400 hidden md:block">
              Ayurvedic IP & Regulatory Guidance • Ministry of Ayush
            </p>
          </div>
        </div>

        {/* Center Controls: Jurisdiction & Bhashini Language Switcher */}
        <div className="flex items-center gap-2">
          {/* Jurisdiction Toggle */}
          <div className="flex items-center bg-slate-900/80 p-1 rounded-xl border border-slate-800">
            <button
              id="toggle-jurisdiction-india"
              onClick={() => setJurisdiction('india')}
              className={`flex items-center space-x-1.5 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                jurisdiction === 'india'
                  ? 'bg-emerald-600 text-white shadow-sm shadow-emerald-900/50'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              <span>🇮🇳</span>
              <span className="hidden sm:inline">India Law</span>
            </button>
            <button
              id="toggle-jurisdiction-intl"
              onClick={() => setJurisdiction('international')}
              className={`flex items-center space-x-1.5 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                jurisdiction === 'international'
                  ? 'bg-emerald-600 text-white shadow-sm shadow-emerald-900/50'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              <Globe className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">International Law</span>
            </button>
          </div>

          {/* Bhashini Indic Language Selector */}
          <div className="flex items-center bg-slate-900/80 px-2 py-1 rounded-xl border border-slate-800">
            <Languages className="w-3.5 h-3.5 text-indigo-400 mr-1.5 shrink-0" />
            <select
              value={selectedLanguage}
              onChange={(e) => setSelectedLanguage(e.target.value)}
              className="bg-transparent text-xs text-slate-200 outline-none cursor-pointer font-medium"
              title="Select Indic Language (Bhashini Engine)"
            >
              {LANGUAGES.map((lang) => (
                <option key={lang.code} value={lang.code} className="bg-slate-900 text-slate-200">
                  {lang.native} ({lang.name})
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Right Navigation Tabs */}
        <div className="flex items-center space-x-2 shrink-0">
          <nav className="flex items-center bg-slate-900/80 p-1 rounded-xl border border-slate-800 overflow-x-auto max-w-full">
            <button
              id="tab-chat"
              onClick={() => setActiveTab('chat')}
              className={`flex items-center space-x-1 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'chat'
                  ? 'bg-slate-800 text-emerald-400 border border-emerald-500/30'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <MessageSquare className="w-3.5 h-3.5" />
              <span className="hidden md:inline">Assistant</span>
            </button>

            <button
              id="tab-knowledge-graph"
              onClick={() => setActiveTab('knowledge_graph')}
              className={`flex items-center space-x-1 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'knowledge_graph'
                  ? 'bg-slate-800 text-emerald-400 border border-emerald-500/30'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Network className="w-3.5 h-3.5" />
              <span className="hidden md:inline">Knowledge Graph</span>
            </button>

            <button
              id="tab-synergy"
              onClick={() => setActiveTab('synergy')}
              className={`flex items-center space-x-1 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'synergy'
                  ? 'bg-slate-800 text-emerald-400 border border-emerald-500/30'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <FlaskConical className="w-3.5 h-3.5" />
              <span className="hidden md:inline">Sec 3(e) Synergy</span>
            </button>

            <button
              id="tab-metrics"
              onClick={() => setActiveTab('metrics')}
              className={`flex items-center space-x-1 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'metrics'
                  ? 'bg-slate-800 text-emerald-400 border border-emerald-500/30'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <BarChart3 className="w-3.5 h-3.5" />
              <span className="hidden md:inline">Metrics</span>
            </button>
          </nav>

          {/* Escalate to Human Expert */}
          <button
            id="btn-escalate-header"
            onClick={onOpenEscalate}
            className="hidden lg:flex items-center space-x-1 px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-amber-300 text-xs font-semibold border border-amber-500/30 transition-all shadow-sm cursor-pointer"
          >
            <AlertCircle className="w-3.5 h-3.5 text-amber-400" />
            <span>Escalate</span>
          </button>
        </div>

      </div>
    </header>
  );
};
