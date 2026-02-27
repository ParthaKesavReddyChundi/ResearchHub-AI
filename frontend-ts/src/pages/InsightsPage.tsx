import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api/client';
import type { AnalysisHistoryItem } from '../types/api';
import { BarChart3, AlertCircle, TrendingUp, Lightbulb, Target } from 'lucide-react';

export default function InsightsPage() {
    const { activeWorkspace } = useAuth();
    const [history, setHistory] = useState<AnalysisHistoryItem[]>([]);
    const [selectedId, setSelectedId] = useState<number | null>(null);
    const [insightData, setInsightData] = useState<Record<string, unknown> | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (activeWorkspace) {
            api.getHistory(activeWorkspace.id).then(setHistory).catch(() => { });
        }
    }, [activeWorkspace]);

    const loadInsights = async (id: number) => {
        setSelectedId(id);
        setLoading(true);
        try {
            const res = await api.getResult(id);
            setInsightData(res.result as Record<string, unknown>);
        } catch {
            setInsightData(null);
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

    const novelty = insightData?.novelty_score as Record<string, unknown> | undefined;
    const confidence = insightData?.confidence_score as Record<string, unknown> | undefined;
    const trend = insightData?.trend_forecast as Record<string, unknown> | undefined;
    const gaps = insightData?.gap_analysis as Record<string, unknown> | undefined;

    return (
        <div className="page-content">
            <h2 style={{ marginBottom: 16, fontSize: 20, fontWeight: 700, display: 'flex', alignItems: 'center', gap: 8 }}>
                <BarChart3 size={20} style={{ color: 'var(--accent)' }} />
                Research Insights
            </h2>

            {history.length === 0 ? (
                <div className="card" style={{ padding: 30, textAlign: 'center' }}>
                    <p style={{ color: 'var(--text-muted)' }}>Run an analysis first to see insights.</p>
                </div>
            ) : (
                <div style={{ display: 'grid', gridTemplateColumns: '260px 1fr', gap: 16 }}>
                    {/* History selector */}
                    <div className="card" style={{ padding: 12 }}>
                        <h4 style={{ fontSize: 13, fontWeight: 700, marginBottom: 10 }}>Select Analysis</h4>
                        {history.map((h) => (
                            <div
                                key={h.id}
                                onClick={() => loadInsights(h.id)}
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

                    {/* Insights display */}
                    <div>
                        {loading ? (
                            <div className="card" style={{ padding: 40, textAlign: 'center' }}><div className="spinner" /></div>
                        ) : !insightData ? (
                            <div className="card" style={{ padding: 40, textAlign: 'center' }}>
                                <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>Click an analysis to view insights.</p>
                            </div>
                        ) : (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                                {/* Score cards */}
                                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12 }}>
                                    <div className="card" style={{ padding: 16, textAlign: 'center' }}>
                                        <Lightbulb size={20} style={{ color: 'var(--accent)', marginBottom: 6 }} />
                                        <div style={{ fontSize: 28, fontWeight: 800, color: 'var(--accent)' }}>
                                            {(novelty?.overall_score as number) ?? 'N/A'}
                                        </div>
                                        <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>Novelty Score</div>
                                    </div>
                                    <div className="card" style={{ padding: 16, textAlign: 'center' }}>
                                        <Target size={20} style={{ color: '#22c55e', marginBottom: 6 }} />
                                        <div style={{ fontSize: 28, fontWeight: 800, color: '#22c55e' }}>
                                            {(confidence?.score as number) ?? 'N/A'}
                                        </div>
                                        <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>Confidence</div>
                                    </div>
                                    <div className="card" style={{ padding: 16, textAlign: 'center' }}>
                                        <TrendingUp size={20} style={{ color: '#3b82f6', marginBottom: 6 }} />
                                        <div style={{ fontSize: 28, fontWeight: 800, color: '#3b82f6' }}>
                                            {Array.isArray((trend as Record<string, unknown>)?.emerging_topics)
                                                ? (trend as Record<string, string[]>).emerging_topics.length
                                                : '—'}
                                        </div>
                                        <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>Emerging Topics</div>
                                    </div>
                                </div>

                                {/* Novelty explanation */}
                                {novelty?.explanation && (
                                    <div className="card" style={{ padding: 16 }}>
                                        <h4 style={{ fontSize: 13, fontWeight: 700, marginBottom: 8 }}>Novelty Analysis</h4>
                                        <p style={{ fontSize: 13, lineHeight: 1.6, margin: 0 }}>{novelty.explanation as string}</p>
                                    </div>
                                )}

                                {/* Gap Analysis */}
                                {gaps && !('error' in gaps) && (
                                    <div className="card" style={{ padding: 16 }}>
                                        <h4 style={{ fontSize: 13, fontWeight: 700, marginBottom: 8 }}>Research Gaps Detected</h4>
                                        {Array.isArray(gaps.novel_research_directions) && (
                                            <ul style={{ fontSize: 13, lineHeight: 1.8, margin: 0, paddingLeft: 16 }}>
                                                {(gaps.novel_research_directions as string[]).slice(0, 5).map((g, i) => (
                                                    <li key={i}>{typeof g === 'string' ? g : JSON.stringify(g)}</li>
                                                ))}
                                            </ul>
                                        )}
                                    </div>
                                )}

                                {/* Confidence breakdown */}
                                {confidence?.breakdown && (
                                    <div className="card" style={{ padding: 16 }}>
                                        <h4 style={{ fontSize: 13, fontWeight: 700, marginBottom: 8 }}>Confidence Breakdown</h4>
                                        {(confidence.breakdown as string[]).map((reason, i) => (
                                            <div key={i} style={{
                                                padding: '6px 10px', fontSize: 12, borderRadius: 6,
                                                background: 'var(--bg-input)', marginBottom: 4,
                                            }}>
                                                ✓ {reason}
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
