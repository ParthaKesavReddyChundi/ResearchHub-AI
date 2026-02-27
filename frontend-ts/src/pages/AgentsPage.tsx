import { Cpu, Zap } from 'lucide-react';

const AGENTS = [
    { name: 'Intent Router', desc: 'Classifies user query into research intent category', icon: '🎯' },
    { name: 'Summarizer', desc: 'Generates structured summaries of all retrieved papers', icon: '📝' },
    { name: 'Comparison', desc: 'Compares methodologies, results, and approaches across papers', icon: '⚖️' },
    { name: 'Insight', desc: 'Extracts deep cross-paper insights and hidden patterns', icon: '💡' },
    { name: 'Gap Detection', desc: 'Identifies research gaps and unexplored combinations', icon: '🔍' },
    { name: 'Knowledge Graph', desc: 'Builds concept-relationship graph from research data', icon: '🕸️' },
    { name: 'Novelty Scorer', desc: 'Scores the novelty and uniqueness of the research area', icon: '🆕' },
    { name: 'Trend Forecaster', desc: 'Predicts 1-year and 5-year trends in the research field', icon: '📈' },
    { name: 'Critique', desc: 'Evaluates argument strength, biases, and methodology quality', icon: '🧐' },
    { name: 'Roadmap', desc: 'Creates a 30-day action plan for researchers', icon: '🗺️' },
    { name: 'Literature Review', desc: 'Synthesizes a complete literature review narrative', icon: '📚' },
];

export default function AgentsPage() {
    return (
        <div className="page-content">
            <h2 style={{ marginBottom: 6, fontSize: 20, fontWeight: 700, display: 'flex', alignItems: 'center', gap: 8 }}>
                <Cpu size={20} style={{ color: 'var(--accent)' }} />
                Active Agents
            </h2>
            <p style={{ color: 'var(--text-muted)', fontSize: 13, marginBottom: 20 }}>
                All 11 agents that power the ResearchHub multi-agent analysis pipeline.
            </p>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
                {AGENTS.map((agent) => (
                    <div key={agent.name} className="card" style={{ padding: 16, display: 'flex', gap: 12, alignItems: 'flex-start' }}>
                        <div style={{ fontSize: 24, lineHeight: 1 }}>{agent.icon}</div>
                        <div style={{ flex: 1 }}>
                            <div style={{ fontWeight: 700, fontSize: 14, marginBottom: 4, display: 'flex', alignItems: 'center', gap: 6 }}>
                                {agent.name}
                                <Zap size={12} style={{ color: '#22c55e' }} />
                            </div>
                            <p style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.5, margin: 0 }}>
                                {agent.desc}
                            </p>
                        </div>
                    </div>
                ))}
            </div>

            {/* Data sources */}
            <div className="card" style={{ padding: 16, marginTop: 20 }}>
                <h3 style={{ fontSize: 14, fontWeight: 700, marginBottom: 10 }}>Data Sources</h3>
                <div style={{ display: 'flex', gap: 12 }}>
                    <div style={{ padding: '8px 16px', borderRadius: 8, background: 'var(--accent-light)', fontWeight: 600, fontSize: 13 }}>
                        🔬 arXiv (5 papers/query)
                    </div>
                    <div style={{ padding: '8px 16px', borderRadius: 8, background: 'var(--accent-light)', fontWeight: 600, fontSize: 13 }}>
                        🏥 PubMed (5 papers/query)
                    </div>
                    <div style={{ padding: '8px 16px', borderRadius: 8, background: 'var(--accent-light)', fontWeight: 600, fontSize: 13 }}>
                        🧠 Groq LLM (Llama 3.3 70B)
                    </div>
                </div>
            </div>
        </div>
    );
}
