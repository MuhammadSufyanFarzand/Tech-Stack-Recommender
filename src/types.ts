export interface MatchingTerm {
  term: string;
  query_weight: number;
  doc_weight: number;
  contribution: number;
}

export interface RecommendationResult {
  rank: number;
  similarity_score: number;
  match_percentage: number;
  stack_id: string;
  stack_name: string;
  category: string;
  roles: string;
  primary_language: string;
  frameworks_libraries: string;
  database_storage: string;
  infrastructure_tools: string;
  skills_description: string;
  matching_terms: MatchingTerm[];
}

export interface RecommendationApiResponse {
  query_raw: string;
  query_cleaned: string;
  total_stacks_analyzed: number;
  top_n: number;
  recommendations: RecommendationResult[];
}

export interface ProjectFile {
  path: string;
  relativePath: string;
  type: 'file' | 'dir';
  size?: number;
  content?: string;
}
