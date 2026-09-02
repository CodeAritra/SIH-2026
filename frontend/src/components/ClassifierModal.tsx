import React from 'react';
import { HelpCircle, ChevronRight, Sparkles } from 'lucide-react';
import { ClassifierQuestion } from '../types';

interface ClassifierModalProps {
  question: ClassifierQuestion;
  onSelectOption: (optionKey: string) => void;
  onSkip?: () => void;
}

export const ClassifierModal: React.FC<ClassifierModalProps> = ({
  question,
  onSelectOption,
  onSkip
}) => {
  return (
    <div className="bg-slate-900/90 border border-emerald-500/30 rounded-2xl p-5 shadow-2xl shadow-emerald-950/50 backdrop-blur-xl animate-in fade-in slide-in-from-bottom-3 duration-300 my-4">
      <div className="flex items-start space-x-3 mb-4">
        <div className="p-2 rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 shrink-0">
          <HelpCircle className="w-5 h-5" />
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400">
              Formulation Classification Required
            </span>
          </div>
          <h3 className="text-sm font-semibold text-slate-100 mt-1">
            {question.question}
          </h3>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-2.5">
        {question.options.map((opt) => (
          <button
            key={opt.key}
            onClick={() => onSelectOption(opt.key)}
            className="flex items-center justify-between p-3 rounded-xl bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 hover:border-emerald-500/50 text-left transition-all group"
          >
            <div>
              <div className="text-xs font-semibold text-slate-200 group-hover:text-emerald-300">
                {opt.label}
              </div>
              <div className="text-[11px] text-slate-400 mt-0.5">
                {opt.desc}
              </div>
            </div>
            <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-emerald-400 transition-transform group-hover:translate-x-0.5 shrink-0 ml-2" />
          </button>
        ))}
      </div>

      {onSkip && (
        <div className="mt-3 text-right">
          <button
            onClick={onSkip}
            className="text-xs text-slate-400 hover:text-slate-200 underline underline-offset-2"
          >
            Skip classification and answer directly
          </button>
        </div>
      )}
    </div>
  );
};
