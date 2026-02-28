import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api/client';
import type { AnalysisHistoryItem } from '../types/api';
import { GitGraph, AlertCircle } from 'lucide-react';

export default function GraphPage() {
    const { activeWorkspace } = useAuth();
    const [history, setHistory] = useState<AnalysisHistoryItem[]>([]);
    const [selectedId, setSelectedId] = useState<number | null>(null);
    const [graphData, setGraphData] = useState<Record<string, unknown> | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (activeWorkspace) {
            api.getHistory(activeWorkspace.id).then(setHistory).catch(() => { });
        }
    }, [activeWorkspace]);

    const loadGraph = async (id: number) => {
        setSelectedId(id);
        setLoading(true);
        try {
            const res = await api.getResult(id);
            setGraphData((res.result as Record<string, unknown>)?.knowledge_graph as Record<string, unknown> ?? null);
        } catch {
            setGraphData(null);
        }
        setLoading(false);
    };

    if (!activeWorkspace) {
        return (
            <div className="page-content">
                <div className="card" style={{ padding: 40, textAlign: 'center' }}>
                    <AlertCircle size={32} style={{ color: 'var(--text-muted)', marginBottom: 8 }} />
                    <p style={{ color: 'var(--text-muted)' }}>Select a workspace first.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="page-content">
            <h2 style={{ marginBottom: 16, fontSize: 20, fontWeight: 700, display: 'flex', alignItems: 'center', gap: 8 }}>
                <GitGraph size={20} style={{ color: 'var(--accent)' }} />
                Knowledge Graph
            </h2>

            {history.length === 0 ? (
                <div className="card" style={{ padding: 30, textAlign: 'center' }}>
                    <p style={{ color: 'var(--text-muted)' }}>Run an analysis first to generate a knowledge graph.</p>
                </div>
            ) : (
                <div style={{ display: 'grid', gridTemplateColumns: '260px 1fr', gap: 16 }}>
                    {/* History list */}
                    <div className="card" style={{ padding: 12 }}>
                        <h4 style={{ fontSize: 13, fontWeight: 700, marginBottom: 10 }}>Select Analysis</h4>
                        {history.map((h) => (
                            <div
                                key={h.id}
                                onClick={() => loadGraph(h.id)}
                                style={{
                                    padding: '8px 10px', borderRadius: 6, cursor: 'pointer', fontSize: 12,
                                    background: selectedId === h.id ? 'var(--accent-light)' : 'transparent',
                                    border: selectedId === h.id ? '1px solid var(--accent)' : '1px solid transparent',
                                    marginBottom: 4, fontWeight: 500,
                                }}
                            >
                                {h.query}
                            </div>
                        ))}
                    </div>

                    {/* Graph display */}
                    <div className="card" style={{ padding: 20 }}>
                        {loading ? (
                            <div style={{ textAlign: 'center', padding: 40 }}><div className="spinner" /></div>
                        ) : !graphData ? (
                            <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: 40, fontSize: 13 }}>
                                Click an analysis to view its knowledge graph.
                            </p>
                        ) : (
                            <div>
                                <div style={{ display: 'flex', gap: 16, marginBottom: 16 }}>
                                    <div className="card" style={{ padding: 14, flex: 1, textAlign: 'center' }}>
                                        <div style={{ fontSize: 28, fontWeight: 800, color: 'var(--accent)' }}>
                                            {(graphData as Record<string, number>).node_count ?? 0}
                                        </div>
                                        <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>Nodes</div>
                                    </div>
                                    <div className="card" style={{ padding: 14, flex: 1, textAlign: 'center' }}>
                                        <div style={{ fontSize: 28, fontWeight: 800, color: 'var(--accent)' }}>
                                            {(graphData as Record<string, number>).edge_count ?? 0}
                                        </div>
                                        <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>Edges</div>
                                    </div>
                                </div>

                                {/* Key concepts */}
                                {Array.isArray((graphData as Record<string, unknown>).key_concepts) && (
                                    <div style={{ marginBottom: 14 }}>
                                        <h4 style={{ fontSize: 13, fontWeight: 700, marginBottom: 8 }}>Key Concepts</h4>
                                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                                            {((graphData as Record<string, string[]>).key_concepts || []).map((c, i) => (
                                                <span key={i} className="badge badge-blue">{c}</span>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Graph insights */}
                                {(graphData as Record<string, string>).graph_insights && (
                                    <div>
                                        <h4 style={{ fontSize: 13, fontWeight: 700, marginBottom: 8 }}>Graph Insights</h4>
                                        <p style={{ fontSize: 13, lineHeight: 1.6 }}>
                                            {(graphData as Record<string, string>).graph_insights}
                                        </p>
                                    </div>
                                )}

                                {/* Hidden connections */}
                                {Array.isArray((graphData as Record<string, unknown>).hidden_connections) && (
                                    <div style={{ marginTop: 14 }}>
                                        <h4 style={{ fontSize: 13, fontWeight: 700, marginBottom: 8 }}>Hidden Connections</h4>
                                        {((graphData as Record<string, Array<Record<string, string>>>).hidden_connections || []).map((conn, i) => (
                                            <div key={i} style={{ padding: 8, background: 'var(--bg-input)', borderRadius: 6, marginBottom: 4, fontSize: 12 }}>
                                                {Object.entries(conn).map(([k, v]) => (
                                                    <span key={k}><strong>{k}:</strong> {v} &nbsp;</span>
                                                ))}
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}
