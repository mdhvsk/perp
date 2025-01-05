export interface Session {
    id: string;
    title: string;
    created_at: string;
    updated_at: string;
  }
  
  export interface Message {
    id: string;
    session_id: string;
    role: string;
    message: string;
    created_at: string;
  }
  
  export interface CreateSessionRequest {
    title: string;
  }
  
  export interface CreateMessageRequest {
    session_id: string;
    role: string;
    message: string;
  }