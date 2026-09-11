import React, { useState, useRef, useEffect } from 'react';
import { 
  Send, Sparkles, AlertTriangle, ShieldCheck, ExternalLink, 
  BookOpen, ChevronDown, ChevronUp, AlertCircle, RefreshCw, Lock 
} from 'lucide-react';
import { Message, Jurisdiction, ClassifierQuestion } from '../types';
import { ClassifierModal } from './ClassifierModal';

interface ChatInterfaceProps {
  messages: Message[];
  onSendMessage: (query: string) => void;
  onClassifierAnswer: (questionId: string, optionKey: string) => void;
  loading: boolean;
  jurisdiction: Jurisdiction;
  productCategory: string | null;
  onOpenEscalate: (query?: string) => void;
  onResetSession: () => void;
  onOpenDPDPCertificate?: (logId: number) => void;
  onNavigateToKnowledgeGraph?: () => void;
  onNavigateToSynergy?: () => void;
  selectedLanguage?: string;
}


const QUICK_PROMPTS = [
  { label: 'Traditional Knowledge Patentability', text: 'Can I patent an Ayurvedic herbal formulation based on classical texts?' },
  { label: 'NBA / ABS Clearance', text: 'Do non-citizens need NBA clearance before applying for patents using Indian biological resources?' },
  { label: 'FSSAI Ayurveda-Aahar Rules', text: 'What are the packaging and disease-claim rules for FSSAI Ayurveda-Aahar food supplements?' },
  { label: 'WIPO GRTK Treaty 2024', text: 'What is the mandatory patent disclosure requirement under the 2024 WIPO Genetic Resources Treaty?' }
];

const parseInlineMarkdown = (text: string) => {
  if (!text) return null;
  const tokens = text.split(/(\*\*[^*]+\*\*|\*[^*]+\*)/g);
  return tokens.map((token, i) => {
    if (token.startsWith('**') && token.endsWith('**')) {
      return (
        <strong key={i} className="font-semibold text-emerald-300">
          {token.slice(2, -2)}
        </strong>
      );
    } else if (token.startsWith('*') && token.endsWith('*')) {
      return (
        <em key={i} className="italic text-slate-300">
          {token.slice(1, -1)}
        </em>
      );
    }
    return token;
  });
};

const renderFormattedText = (text: string) => {
  if (!text) return null;

  const paragraphs = text.split(/\n\n+/);

  return (
    <div className="space-y-3">
      {paragraphs.map((para, pIdx) => {
        const trimmed = para.trim();

        // Horizontal rule like --- or ***
        if (/^[\-\*_]{3,}$/.test(trimmed)) {
          return <hr key={pIdx} className="border-slate-800 my-2" />;
        }

        const lines = trimmed.split('\n');
        return (
          <div key={pIdx} className="space-y-1">
            {lines.map((line, lIdx) => {
              let cleanLine = line.trim();

              // Headers like # Header or ## Header
              if (cleanLine.startsWith('#')) {
                cleanLine = cleanLine.replace(/^#+\s*/, '');
                return (
                  <div key={lIdx} className="font-bold text-slate-100 text-xs mt-2 mb-1">
                    {parseInlineMarkdown(cleanLine)}
                  </div>
                );
              }

              // List items starting with - or *
              if (/^[\-\*]\s+/.test(cleanLine)) {
                cleanLine = cleanLine.replace(/^[\-\*]\s+/, '');
                return (
                  <div key={lIdx} className="flex items-start space-x-2 pl-2 text-slate-200">
                    <span className="text-emerald-400 font-bold">•</span>
                    <div>{parseInlineMarkdown(cleanLine)}</div>
                  </div>
                );
              }

              return (
                <div key={lIdx} className="leading-relaxed">
                  {parseInlineMarkdown(cleanLine)}
                </div>
              );
            })}
          </div>
        );
      })}
    </div>
  );
};

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  messages,
  onSendMessage,
  onClassifierAnswer,
  loading,
  jurisdiction,
  productCategory,
  onOpenEscalate,
  onResetSession
}) => {
  const [inputQuery, setInputQuery] = useState('');
  const [expandedCitations, setExpandedCitations] = useState<Record<string, boolean>>({});
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputQuery.trim() || loading) return;
    onSendMessage(inputQuery);
    setInputQuery('');
  };

  const toggleCitation = (msgId: string) => {
    setExpandedCitations(prev => ({ ...prev, [msgId]: !prev[msgId] }));
  };

  return (
    <div className="flex-1 flex flex-col max-w-5xl mx-auto w-full h-[calc(100vh-4rem)] p-4">
      
      {/* Top Banner / Session Bar */}
      <div className="flex items-center justify-between bg-slate-900/60 p-3 rounded-2xl border border-slate-800 mb-4 backdrop-blur-md">
        <div className="flex items-center space-x-3 text-xs">
          <div className="flex items-center space-x-1.5 font-semibold text-slate-300">
            <span className="text-sm">{jurisdiction === 'india' ? '🇮🇳' : '🌐'}</span>
            <span className="capitalize">{jurisdiction} Jurisdiction Filter Active</span>
          </div>
          <span className="text-slate-600">•</span>
          <div className="flex items-center space-x-1 text-slate-400">
            <span>Product Type:</span>
            <span className="text-emerald-400 font-semibold">{productCategory || 'Not yet classified'}</span>
          </div>
        </div>

        <button
          onClick={onResetSession}
          className="flex items-center space-x-1 text-[11px] text-slate-400 hover:text-slate-200 px-2 py-1 rounded-lg hover:bg-slate-800 transition-all"
          title="Reset session and formulation classification"
        >
          <RefreshCw className="w-3 h-3" />
          <span>Reset Session</span>
        </button>
      </div>

      {/* Message Feed */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-2">
        {messages.length === 0 && (
          <div className="py-12 text-center space-y-4 max-w-md mx-auto">
            <div className="w-16 h-16 rounded-2xl ayush-gradient flex items-center justify-center mx-auto shadow-xl shadow-emerald-950/50 border border-emerald-500/30">
              <Sparkles className="w-8 h-8 text-emerald-400" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-100">Welcome to IP-SAKTI Sahayak</h2>
              <p className="text-xs text-slate-400 mt-1">
                Your RAG-grounded assistant for Ayurvedic patents, traditional knowledge (TKDL), ABS compliance, and regulatory drug approvals.
              </p>
            </div>

            {/* Quick Prompts */}
            <div className="grid grid-cols-1 gap-2 pt-2">
              {QUICK_PROMPTS.map((qp, idx) => (
                <button
                  key={idx}
                  onClick={() => onSendMessage(qp.text)}
                  className="p-3 rounded-xl bg-slate-900/80 hover:bg-slate-800 border border-slate-800 hover:border-emerald-500/40 text-left text-xs transition-all group"
                >
                  <div className="font-semibold text-emerald-400 group-hover:text-emerald-300">{qp.label}</div>
                  <div className="text-slate-400 text-[11px] truncate mt-0.5">{qp.text}</div>
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg) => {
          const isGroundedDomain = msg.response_type === 'grounded' || Boolean(msg.citations && msg.citations.length > 0);

          return (
            <div
              key={msg.id}
              className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
            >
              {/* User Message */}
              {msg.sender === 'user' ? (
                <div className="max-w-2xl px-4 py-3 rounded-2xl bg-emerald-600 text-white text-xs font-medium shadow-md shadow-emerald-950/30">
                  {msg.text}
                </div>
              ) : (
                /* Bot Response Card */
                <div className="max-w-3xl w-full glass-panel rounded-2xl p-5 border border-slate-800 space-y-4 shadow-xl">
                  
                  {/* Response Header */}
                  <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                    <div className="flex items-center space-x-2">
                      <ShieldCheck className="w-4 h-4 text-emerald-400" />
                      <span className="text-xs font-bold text-slate-200">IP-SAKTI Sahayak</span>
                      {isGroundedDomain && msg.product_category && (
                        <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-medium">
                          {msg.product_category}
                        </span>
                      )}
                    </div>

                    {isGroundedDomain && msg.confidence && (
                      <div className="flex items-center space-x-1.5">
                        <span className="text-[10px] font-semibold text-slate-400">Retrieval Confidence:</span>
                        <span
                          className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded-full ${
                            msg.confidence === 'High'
                              ? 'badge-high'
                              : msg.confidence === 'Medium'
                              ? 'badge-medium'
                              : 'badge-low'
                          }`}
                        >
                          {msg.confidence} {msg.top_score ? `(${Math.round(msg.top_score * 100)}%)` : ''}
                        </span>
                      </div>
                    )}
                  </div>

                  {/* Hard-Gate Block Banner if applies */}
                  {msg.is_blocked && (
                    <div className="flex items-start space-x-2.5 p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
                      <Lock className="w-4 h-4 shrink-0 mt-0.5 text-rose-400" />
                      <div>
                        <span className="font-bold">Hard-Gate Citation Enforcement Active:</span> Ungrounded claims blocked. Showing safe abstention notice.
                      </div>
                    </div>
                  )}

                  {/* Inline Formulation Classifier Modal */}
                  {msg.needs_classification && msg.classifier_question && (
                    <ClassifierModal
                      question={msg.classifier_question}
                      onSelectOption={(optionKey) => onClassifierAnswer(msg.classifier_question!.id, optionKey)}
                    />

                  )}

                  {/* Main Grounded Answer Text */}
                  <div className="text-xs text-slate-200 leading-relaxed font-normal">
                    {renderFormattedText(msg.text)}
                  </div>

                  {/* ABS Compliance Alert Banner */}
                  {isGroundedDomain && msg.abs_alert && msg.abs_alert.triggered && (
                    <div className="flex items-start space-x-2.5 p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs">
                      <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5 text-amber-400" />
                      <div>
                        <div className="font-bold">{msg.abs_alert.title}</div>
                        <div className="mt-0.5 text-[11px] text-amber-200/90 leading-tight">{msg.abs_alert.message}</div>
                      </div>
                    </div>
                  )}

                  {/* TKDL Prior-Art Pointer */}
                  {isGroundedDomain && msg.tkdl_pointer && msg.tkdl_pointer.triggered && (
                    <div className="flex items-start space-x-2.5 p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs">
                      <BookOpen className="w-4 h-4 shrink-0 mt-0.5 text-emerald-400" />
                      <div>
                        <div className="font-bold">{msg.tkdl_pointer.title}</div>
                        <div className="mt-0.5 text-[11px] text-emerald-200/90 leading-tight">{msg.tkdl_pointer.message}</div>
                      </div>
                    </div>
                  )}

                  {/* Citations Accordion */}
                  {msg.citations && msg.citations.length > 0 && (
                    <div className="border border-slate-800 rounded-xl overflow-hidden bg-slate-900/40">
                      <button
                        onClick={() => toggleCitation(msg.id)}
                        className="w-full flex items-center justify-between p-3 text-xs font-semibold text-slate-300 hover:bg-slate-800/50 transition-all"
                      >
                        <div className="flex items-center space-x-2">
                          <BookOpen className="w-3.5 h-3.5 text-emerald-400" />
                          <span>Grounded Source Citations ({msg.citations.length})</span>
                        </div>
                        {expandedCitations[msg.id] ? (
                          <ChevronUp className="w-4 h-4 text-slate-400" />
                        ) : (
                          <ChevronDown className="w-4 h-4 text-slate-400" />
                        )}
                      </button>

                      {expandedCitations[msg.id] && (
                        <div className="p-3 border-t border-slate-800 space-y-2 bg-slate-950/40">
                          {msg.citations.map((c, cIdx) => (
                            <div key={cIdx} className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 text-xs space-y-1">
                              <div className="flex items-center justify-between font-bold text-emerald-400">
                                <span>{c.source_title}</span>
                                <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 uppercase">
                                  {c.source_section}
                                </span>
                              </div>
                              <p className="text-[11px] text-slate-400 italic">"{c.snippet}"</p>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}

                  {/* External Registry Buttons */}
                  {isGroundedDomain && msg.registry_links && msg.registry_links.length > 0 && (
                    <div className="pt-1 flex flex-wrap gap-2">
                      {msg.registry_links.map((link, lIdx) => (
                        <a
                          key={lIdx}
                          href={link.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-[11px] font-medium border border-slate-700/60 transition-all"
                        >
                          <span>{link.name}</span>
                          <ExternalLink className="w-3 h-3 text-slate-400" />
                        </a>
                      ))}
                    </div>
                  )}

                  {/* Footer Disclaimer & Escalate Action */}
                  <div className="flex items-center justify-between pt-2 border-t border-slate-800/60 text-[10px] text-slate-500">
                    <span>Informational guidance only • Not legal advice</span>
                    {isGroundedDomain && (
                      <button
                        onClick={() => onOpenEscalate(msg.text)}
                        className="text-amber-400 hover:underline flex items-center space-x-1"
                      >
                        <AlertCircle className="w-3 h-3" />
                        <span>Escalate query to human expert</span>
                      </button>
                    )}
                  </div>

                </div>
              )}
            </div>
          );
        })}

        {loading && (
          <div className="flex items-center space-x-2 text-xs text-slate-400 p-4">
            <RefreshCw className="w-4 h-4 animate-spin text-emerald-400" />
            <span>Retrieving grounded legal chunks & analyzing via Gemini...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Bar */}
      <form onSubmit={handleSubmit} className="mt-4 relative">
        <div className="relative flex items-center">
          <input
            id="chat-input-field"
            type="text"
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            placeholder={`Ask any IP or regulatory question (${jurisdiction.toUpperCase()} law active)...`}
            className="w-full pl-4 pr-12 py-3.5 bg-slate-900 border border-slate-800 focus:border-emerald-500 rounded-2xl text-xs text-slate-100 placeholder-slate-500 focus:outline-none shadow-xl"
          />
          <button
            id="chat-submit-btn"
            type="submit"
            disabled={!inputQuery.trim() || loading}
            className="absolute right-2 p-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white disabled:opacity-40 transition-all shadow-md shadow-emerald-950/50"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </form>

    </div>
  );
};