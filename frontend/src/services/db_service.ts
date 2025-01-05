import { Session, CreateMessageRequest, Message } from '@/utils/types';
import axios, { AxiosError } from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/db';

export class DBService {
  private static instance: DBService;
  private constructor() {}

  public static getInstance(): DBService {
    if (!DBService.instance) {
      DBService.instance = new DBService();
    }
    return DBService.instance;
  }

  private handleError(error: unknown) {
    if (error instanceof AxiosError) {
      throw new Error(error.response?.data?.detail || 'An error occurred');
    }
    throw error;
  }

  // Session Methods
  public async getAllSessions(): Promise<Session[]> {
    try {
      const response = await axios.get<Session[]>(`${API_BASE_URL}/sessions`);
      return response.data;
    } catch (error) {
      this.handleError(error);
      return []; // TypeScript requires this, though it will never be reached
    }
  }

  public async getSessionById(sessionId: string): Promise<Session> {
    try {
      const response = await axios.get<Session>(`${API_BASE_URL}/sessions/${sessionId}`);
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  public async createSession(title: string = "New Session"): Promise<Session> {
    const body = {"title": title}
    try {
      const response = await axios.post<Session>(`${API_BASE_URL}/sessions`, body);
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  // Message Methods
  public async getSessionMessages(sessionId: string): Promise<Message[]> {
    try {
      const response = await axios.get<Message[]>(`${API_BASE_URL}/messages/${sessionId}`);
      return response.data;
    } catch (error) {
      this.handleError(error);
      return []; // TypeScript requires this, though it will never be reached
    }
  }

  public async createMessage(data: CreateMessageRequest): Promise<Message> {
    console.log('Sending request with data:', JSON.stringify(data, null, 2));
    if(data.sources == null){
      data.sources = []
    }
    try {
      const response = await axios.post<Message>(`${API_BASE_URL}/messages`, data);
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }
}

// Export a singleton instance
export const dbService = DBService.getInstance();