import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  ShieldCheck, Lock, CheckCircle2, FileText, 
  Printer, X, Copy, Check, ExternalLink, Award 
} from 'lucide-react';
import { ComplianceCertificate } from '../types';

interface DPDPConsentModalProps {
  isOpen: boolean;
  onClose: () => void;
  logId?: number | null;
}

export const DPDPConsentModal: React.FC<DPDPConsentModalProps> = ({ isOpen, onClose, logId }) => {
  const [cert, setCert] = useState<ComplianceCertificate | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [copied, setCopied] = useState<boolean>(false);

  useEffect(() => {
    if (isOpen && logId) {
      fetchCertificate(logId);
    }
  }, [isOpen, logId]);

  const fetchCertificate = async (id: number) => {
    setLoading(true);
    try {
      const res = await axios.get(`/api/dpdp/certificate/${id}`);
      setCert(res.data);
    } catch (err) {
      console.error('Error fetching certificate:', err);
    } finally {
      setLoading(false);
    }
  };

  const copyHash = () => {
    if (cert?.verification_hash) {
      navigator.clipboard.writeText(cert.verification_hash);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-2xl bg-slate-900 border border-emerald-500/40 rounded-2xl p-6 shadow-2xl overflow-y-auto max-h-[90vh]">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {loading ? (
          <div className="py-12 flex flex-col items-center justify-center gap-3 text-slate-400">
            <ShieldCheck className="w-8 h-8 animate-pulse text-emerald-400" />
            <p className="text-sm font-medium">Validating DPDP SHA-256 cryptographic proof...</p>
          </div>
        ) : cert ? (
          <div className="space-y-5" id="printable-certificate">
            {/* Header Certificate Seal */}
            <div className="text-center pb-4 border-b border-slate-800 space-y-1">
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-semibold border border-emerald-500/30">
                <ShieldCheck className="w-4 h-4" />
                <span>{cert.dpdp_status}</span>
              </div>
              <h2 className="text-xl font-bold text-white tracking-wide pt-2">
                Ayurvedic IP & Regulatory Compliance Certificate
              </h2>
              <p className="text-xs text-slate-400 font-mono">
                Certificate Docket ID: <span className="text-emerald-400 font-bold">{cert.certificate_id}</span>
              </p>
            </div>

            {/* Verification Hash Badge */}
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between gap-3 text-xs">
              <div className="min-w-0">
                <span className="text-[10px] text-slate-400 uppercase font-semibold block">SHA-256 Cryptographic Fingerprint:</span>
                <span className="font-mono text-emerald-300 truncate block text-[11px]">{cert.verification_hash}</span>
              </div>
              <button
                onClick={copyHash}
                className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition-colors shrink-0"
                title="Copy Hash"
              >
                {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
              </button>
            </div>

            {/* Certificate Details Grid */}
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1">
                <span className="text-slate-400 block">Formulation Classification:</span>
                <span className="font-bold text-slate-200">{cert.formulation_classification}</span>
              </div>

              <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1">
                <span className="text-slate-400 block">Grounding Confidence Rating:</span>
                <span className="font-bold text-emerald-400">{cert.confidence_rating} Confidence</span>
              </div>
            </div>

            {/* Inquiry Snippet */}
            <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 text-xs space-y-1">
              <span className="text-slate-400 block">User Legal Inquiry:</span>
              <p className="text-slate-200 italic">"{cert.user_inquiry}"</p>
            </div>

            {/* Validated Statutory Sections */}
            <div className="space-y-1.5 text-xs">
              <span className="font-semibold text-slate-300 block">Validated Statutory Seed Citations:</span>
              <div className="flex flex-wrap gap-1.5">
                {cert.statutory_citations_validated.length > 0 ? (
                  cert.statutory_citations_validated.map((cit, idx) => (
                    <span key={idx} className="px-2.5 py-1 rounded-lg bg-indigo-950/60 text-indigo-300 border border-indigo-800/40 text-[11px]">
                      {cit}
                    </span>
                  ))
                ) : (
                  <span className="text-slate-400">Standard statutory seed grounding</span>
                )}
              </div>
            </div>

            {/* ABS and TKDL checks */}
            <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800 text-xs space-y-1">
              <span className="font-semibold text-amber-400 block">Regulatory Clearances:</span>
              <p className="text-slate-300">• <strong>ABS:</strong> {cert.abs_biological_diversity_compliance.form_required}</p>
              <p className="text-slate-300">• <strong>TKDL:</strong> {cert.tkdl_prior_art_check.impact}</p>
            </div>

            {/* Disclaimer */}
            <p className="text-[10px] text-slate-400 leading-relaxed italic border-t border-slate-800 pt-3">
              {cert.legal_disclaimer}
            </p>

            {/* Actions */}
            <div className="flex justify-end gap-3 pt-2">
              <button
                onClick={handlePrint}
                className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-xl flex items-center gap-1.5 transition-colors cursor-pointer"
              >
                <Printer className="w-4 h-4" />
                <span>Print / Save as PDF</span>
              </button>
            </div>
          </div>
        ) : (
          <div className="py-8 text-center text-slate-400 text-sm">
            Certificate data not available.
          </div>
        )}
      </div>
    </div>
  );
};
