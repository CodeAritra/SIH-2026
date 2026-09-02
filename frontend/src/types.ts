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
