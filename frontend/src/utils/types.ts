export interface Session {
    id: string;
    title: string;
    created_at: string;
    updated_at: string;
  }
  
  export interface Message {
    id: string;
    session_id: string;
    question: string;
    answer: string;
    created_at: string;
    sources: object[];  

  }
  
  
  export interface CreateMessageRequest {
    session_id: string;
    question: string;
    answer: string;
    sources: Record<string, string>[];  
  }
export interface QueryGeneralRequest {
  query: string;
}

export interface SearchResponse {
  query: string;
  results: Record<string, string>[];
  sources: Record<string, string>[];
  related_topics: string[];
  medical_disclaimer: string;
}

export interface GeneralSearchResponse {
  question: string;
  answer: string;
  sources: Record<string, string>[]; 
  error: string | null;
}

export interface NutritionSearchParams {
  query: string;
  dietary_restrictions?: string[];
  allergies?: string[];
}

export interface MedicalSearchParams {
  query: string;
  include_research?: boolean;
  credentials?: Record<string, string>;
}