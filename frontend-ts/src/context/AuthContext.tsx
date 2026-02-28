import { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import api from '../api/client';
import type { Workspace } from '../types/api';

interface AuthState {
    token: string | null;
    email: string | null;
    workspaces: Workspace[];
    activeWorkspace: Workspace | null;
    isLoading: boolean;
}

interface AuthContextType extends AuthState {
    login: (email: string, password: string) => Promise<void>;
    register: (email: string, password: string) => Promise<string>;
    logout: () => void;
    loadWorkspaces: () => Promise<void>;
    setActiveWorkspace: (ws: Workspace) => void;
    createWorkspace: (name: string) => Promise<void>;
    deleteWorkspace: (id: number) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
    // Restore active workspace from localStorage
    const savedWs = localStorage.getItem('activeWorkspace');
    const initialWs = savedWs ? JSON.parse(savedWs) as Workspace : null;

    const [state, setState] = useState<AuthState>({
        token: localStorage.getItem('token'),
        email: localStorage.getItem('email'),
        workspaces: [],
        activeWorkspace: initialWs,
        isLoading: false,
    });

    const login = async (email: string, password: string) => {
        const res = await api.login(email, password);
        localStorage.setItem('token', res.access_token);
        localStorage.setItem('email', email);
        setState((s) => ({ ...s, token: res.access_token, email }));
    };

    const register = async (email: string, password: string): Promise<string> => {
        const res = await api.register(email, password);
        return res.message;
    };

    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('email');
        localStorage.removeItem('activeWorkspace');
        setState({ token: null, email: null, workspaces: [], activeWorkspace: null, isLoading: false });
    };

    const loadWorkspaces = async () => {
        try {
            const ws = await api.listWorkspaces();
            setState((s) => {
                // Restore saved workspace if it still exists, otherwise pick first
                const saved = s.activeWorkspace;
                const stillExists = saved && ws.find((w) => w.id === saved.id);
                const active = stillExists ? saved : ws[0] ?? null;
                if (active) localStorage.setItem('activeWorkspace', JSON.stringify(active));
                return { ...s, workspaces: ws, activeWorkspace: active };
            });
        } catch {
            // Token might be invalid
        }
    };

    const setActiveWorkspace = (ws: Workspace) => {
        localStorage.setItem('activeWorkspace', JSON.stringify(ws));
        setState((s) => ({ ...s, activeWorkspace: ws }));
    };

    const createWorkspace = async (name: string) => {
        const newWs = await api.createWorkspace(name);
        await loadWorkspaces();
        // Auto-select the new workspace
        setActiveWorkspace(newWs);
    };

    const deleteWorkspace = async (id: number) => {
        await api.deleteWorkspace(id);
        if (state.activeWorkspace?.id === id) {
            localStorage.removeItem('activeWorkspace');
        }
        setState((s) => ({
            ...s,
            activeWorkspace: s.activeWorkspace?.id === id ? null : s.activeWorkspace,
        }));
        await loadWorkspaces();
    };

    useEffect(() => {
        if (state.token) loadWorkspaces();
    }, [state.token]);

    return (
        <AuthContext.Provider
            value={{
                ...state,
                login,
                register,
                logout,
                loadWorkspaces,
                setActiveWorkspace,
                createWorkspace,
                deleteWorkspace,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error('useAuth must be inside AuthProvider');
    return ctx;
}
