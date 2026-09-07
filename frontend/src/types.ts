export type Jurisdiction = 'india' | 'international';

export interface Citation {
  source_title: string;
  source_section: string;
  ip_type: string;
  jurisdiction: string;
  snippet: string;
}

export interface RegistryLink {
  name: string;
  url: string;
  desc: string;
}

export interface RuleAlert {
  triggered: boolean;
  title: string | null;
  message: string | null;
}

export interface ClassifierOption {
  key: string;
  label: string;
  desc: string;
}

export interface ClassifierQuestion {
  id: string;
  question: string;
  options: ClassifierOption[];
}

export interface Message {
  id: string;
  sender: 'user' | 'bot';
  text: string;
  timestamp: string;
  confidence?: 'High' | 'Medium' | 'Low';
  top_score?: number;
  citations?: Citation[];
  jurisdiction?: Jurisdiction;
  product_category?: string;
  abs_alert?: RuleAlert | null;
  tkdl_pointer?: RuleAlert | null;
  registry_links?: RegistryLink[];
  is_blocked?: boolean;
  response_type?: 'grounded' | 'greeting' | 'out_of_domain' | 'ungrounded';
  needs_classification?: boolean;
  classifier_question?: ClassifierQuestion;
}

export interface EvalDetail {
  id: string;
  query: string;
  jurisdiction: string;
  expected_source: string | null;
  expected_section: string | null;
  hit_found: boolean;
  rank: number;
  top_score: number;
  confidence: string;
  top_retrieved_chunk: string | null;
  is_valid_citation: boolean;
  is_abstained: boolean;
  correct_behavior: boolean;
}

export interface EvalRun {
  id: number;
  timestamp: string;
  run_name: string;
  total_queries: number;
  precision_at_k: number;
  recall_at_k: number;
  mrr: number;
  citation_validity_rate: number;
  abstention_rate: number;
  details: EvalDetail[];
}

export interface QueryLog {
  id: number;
  timestamp: string;
  session_id: string;
  user_query: string;
  jurisdiction: string;
  classification: string | null;
  retrieved_chunks: any[];
  llm_raw_answer: string;
  citations: Citation[];
  confidence: string;
  is_blocked: boolean;
  abs_triggered: boolean;
  tkdl_triggered: boolean;
}
export type Jurisdiction = 'india' | 'international';
export type ActiveTab = 'chat' | 'knowledge_graph' | 'synergy' | 'metrics' | 'dpdp';

export interface Citation {
  source_title: string;
  source_section: string;
  ip_type: string;
  jurisdiction: string;
  snippet: string;
}

export interface RegistryLink {
  name: string;
  url: string;
  desc: string;
}

export interface RuleAlert {
  triggered: boolean;
  title: string | null;
  message: string | null;
}

export interface ClassifierOption {
  key: string;
  label: string;
  desc: string;
}

export interface ClassifierQuestion {
  id: string;
  question: string;
  options: ClassifierOption[];
}

export interface Message {
  id: string;
  sender: 'user' | 'bot';
  text: string;
  timestamp: string;
  confidence?: 'High' | 'Medium' | 'Low';
  top_score?: number;
  citations?: Citation[];
  jurisdiction?: Jurisdiction;
  product_category?: string;
  abs_alert?: RuleAlert | null;
  tkdl_pointer?: RuleAlert | null;
  registry_links?: RegistryLink[];
  is_blocked?: boolean;
  needs_classification?: boolean;
  classifier_question?: ClassifierQuestion;
  crypto_hash?: string;
  log_id?: number;
  target_language?: string;
}

export interface EvalDetail {
  id: string;
  query: string;
  jurisdiction: string;
  expected_source: string | null;
  expected_section: string | null;
  hit_found: boolean;
  rank: number;
  top_score: number;
  confidence: string;
  top_retrieved_chunk: string | null;
  is_valid_citation: boolean;
  is_abstained: boolean;
  correct_behavior: boolean;
}

export interface EvalRun {
  id: number;
  timestamp: string;
  run_name: string;
  total_queries: number;
  precision_at_k: number;
  recall_at_k: number;
  mrr: number;
  citation_validity_rate: number;
  abstention_rate: number;
  details: EvalDetail[];
}

export interface QueryLog {
  id: number;
  timestamp: string;
  session_id: string;
  user_query: string;
  jurisdiction: string;
  classification: string | null;
  retrieved_chunks: any[];
  llm_raw_answer: string;
  citations: Citation[];
  confidence: string;
  is_blocked: boolean;
  abs_triggered: boolean;
  tkdl_triggered: boolean;
  crypto_hash?: string;
  dpdp_consent?: boolean;
}

// Phase 2: Knowledge Graph Types
export interface HerbInfo {
  id: string;
  common_name: string;
  botanical_name: string;
  sanskrit_name: string;
  family: string;
  classical_texts: string[];
  bioactives: string[];
  therapeutic_indications: string[];
  gi_tag?: string;
  tkdl_entries: string[];
  nba_clearance_required: boolean;
  nba_rationale: string;
  sec_3p_risk: string;
  sec_3e_synergy_potential: string;
  recommended_ip_strategy: string;
}

export interface GraphNode {
  id: string;
  label: string;
  sublabel: string;
  type: 'herb' | 'classical_text' | 'bioactive' | 'statutory_bar' | 'regulatory_mandate';
  color: string;
  details?: Record<string, any>;
  x?: number;
  y?: number;
}

export interface GraphEdge {
  source: string;
  target: string;
  label: string;
  color: string;
}

export interface PathwaySummary {
  formulation_type: string;
  herbs_analyzed: string[];
  sec_3p_tk_risk: string;
  sec_3e_synergy_mandate: string;
  nba_approval_required: boolean;
  nba_form: string;
  gi_opportunities: { herb: string; gi: string }[];
  recommended_path: string;
}

export interface PathwayResponse {
  nodes: GraphNode[];
  edges: GraphEdge[];
  pathway_summary: PathwaySummary;
  matched_herbs: HerbInfo[];
}

export interface SynergyProtocolStep {
  step: string;
  description: string;
}

export interface SynergyResult {
  herbs_evaluated: string[];
  therapeutic_claim: string;
  extraction_method: string;
  patentability_verdict: string;
  verdict_color: string;
  risk_radar: {
    sec_3p_traditional_knowledge_risk: number;
    sec_3e_mere_admixture_risk: number;
    sec_3j_biological_substance_risk: number;
    nba_abs_clearance_mandate: number;
  };
  recommended_ip_filing_route: string;
  protocol_steps: SynergyProtocolStep[];
}

// Phase 3: DPDP Compliance Certificate Types
export interface ComplianceCertificate {
  certificate_id: string;
  issuing_system: string;
  timestamp: string;
  verification_hash: string;
  dpdp_status: string;
  compliance_status: string;
  jurisdiction_evaluated: string;
  formulation_classification: string;
  user_inquiry: string;
  confidence_rating: string;
  statutory_citations_validated: string[];
  abs_biological_diversity_compliance: {
    triggered: boolean;
    statute: string;
    form_required: string;
  };
  tkdl_prior_art_check: {
    triggered: boolean;
    impact: string;
  };
  legal_disclaimer: string;
}
