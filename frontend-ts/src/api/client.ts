import axios, { type AxiosInstance } from 'axios';
import type {
    TokenResponse,
    Workspace,
    ChatResponse,
    AnalysisHistoryItem,
    PaperItem,
} from '../types/api';

const BASE_URL = 'http://localhost:8000';

class ApiClient {
    private http: AxiosInstance;

    constructor() {
        this.http = axios.create({ baseURL: BASE_URL });
        this.http.interceptors.request.use((config) => {
            const token = localStorage.getItem('token');
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        });
    }

    // ── Auth ──────────────────────────────────────────────
    async login(email: string, password: string): Promise<TokenResponse> {
        const form = new URLSearchParams();
        form.append('username', email);
        form.append('password', password);
        const { data } = await this.http.post<TokenResponse>('/auth/login', form, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });
        return data;
    }

    async register(email: string, password: string): Promise<{ message: string }> {
        const { data } = await this.http.post('/auth/register', { email, password });
        return data;
    }

    // ── Workspaces ────────────────────────────────────────
    async listWorkspaces(): Promise<Workspace[]> {
        const { data } = await this.http.get<Workspace[]>('/workspaces/');
        return data;
    }

    async createWorkspace(name: string): Promise<Workspace> {
        const { data } = await this.http.post<Workspace>('/workspaces/', { name });
        return data;
    }

    async deleteWorkspace(id: number): Promise<void> {
        await this.http.delete(`/workspaces/${id}`);
    }

    // ── Analysis ──────────────────────────────────────────
    async runAnalysis(query: string, workspaceId?: number): Promise<ChatResponse> {
        const { data } = await this.http.post<ChatResponse>('/chat/analyze', {
            query,
            workspace_id: workspaceId ?? null,
        });
        return data;
    }

    async getHistory(workspaceId: number): Promise<AnalysisHistoryItem[]> {
        const { data } = await this.http.get<AnalysisHistoryItem[]>(
            `/chat/history/${workspaceId}`
        );
        return data;
    }

    async getResult(analysisId: number): Promise<{ result: Record<string, unknown> }> {
        const { data } = await this.http.get(`/chat/result/${analysisId}`);
        return data;
    }

    // ── Papers ────────────────────────────────────────────
    async uploadPaper(workspaceId: number, file: File): Promise<PaperItem> {
        const form = new FormData();
        form.append('file', file);
        const { data } = await this.http.post<PaperItem>(
            `/papers/${workspaceId}`,
            form,
            { headers: { 'Content-Type': 'multipart/form-data' } }
        );
        return data;
    }

    async listPapers(workspaceId: number): Promise<PaperItem[]> {
        const { data } = await this.http.get<PaperItem[]>(`/papers/${workspaceId}`);
        return data;
    }
}

const api = new ApiClient();
export default api;
