/* ──────────────────────────────────────────────────────────
   All 16 result-section renderers in a single file.
   Each takes its typed data and renders inside a SectionCard.
   ────────────────────────────────────────────────────────── */

import SectionCard from './SectionCard';
import Markdown from 'react-markdown';
import {
    MessageSquare, Book, GitGraph, ArrowLeftRight, AlertTriangle,
    Lightbulb, Sparkles, TrendingUp, Wrench, FlaskConical,
    Map, ShieldCheck, Eye, FileText, Target, Activity, Zap
} from 'lucide-react';
import type { AnalysisResult } from '../types/api';

// ── Helpers ──────────────────────────────────────────────
function renderList(items: unknown[]) {
    return (
        <ul style={{ paddingLeft: 16 }}>
            {items.map((item, i) => (
                <li key={i} className="list-item">
                    {typeof item === 'string' ? item : JSON.stringify(item, null, 2)}
                </li>
            ))}
        </ul>
    );
}

function renderKeyValue(obj: Record<string, unknown>) {
    return Object.entries(obj).map(([k, v]) => (
        <div className="status-row" key={k}>
            <span className="label">{k.replace(/_/g, ' ')}</span>
            <span className="value">
                {typeof v === 'string' || typeof v === 'number' ? String(v) : JSON.stringify(v)}
            </span>
        </div>
    ));
}

// ── Sections ──────────────────────────────────────────────
export function DirectAnswerSection({ data }: { data: AnalysisResult['direct_answer'] }) {
    if (!data) return null;
    return (
        <SectionCard title="Direct Answer" icon={<MessageSquare size={16} />} tag="Section 1" defaultOpen>
            <p><strong>Query:</strong> {data.query}</p>
            <p><strong>Papers found:</strong> {data.papers_found} (arXiv: {data.sources.arxiv}, PubMed: {data.sources.pubmed})</p>
            {data.intent && (
                <p><strong>Intent:</strong> {typeof data.intent === 'string' ? data.intent : JSON.stringify(data.intent)}</p>
            )}
        </SectionCard>
    );
}

export function ContextSummarySection({ data }: { data: AnalysisResult['context_summary'] }) {
    if (!data) return null;
    return (
        <SectionCard title="Context Summary" icon={<Book size={16} />} tag="Section 2">
            <p><strong>{data.total_papers} papers</strong> retrieved</p>
            <table className="data-table">
                <thead>
                    <tr><th>Title</th><th>Source</th><th>Authors</th></tr>
                </thead>
                <tbody>
                    {data.papers.map((p, i) => (
                        <tr key={i}>
                            <td><a href={p.url} target="_blank" rel="noreferrer" style={{ color: 'var(--blue)' }}>{p.title}</a></td>
                            <td><span className={`badge ${p.source === 'arxiv' ? 'badge-blue' : 'badge-green'}`}>{p.source}</span></td>
                            <td>{p.authors}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </SectionCard>
    );
}

export function KnowledgeGraphSection({ data }: { data: AnalysisResult['knowledge_graph'] }) {
    if (!data) return null;
    return (
        <SectionCard title="Knowledge Graph" icon={<GitGraph size={16} />} tag="Section 3">
            <div style={{ display: 'flex', gap: 20, marginBottom: 12 }}>
                <div><strong>{data.node_count}</strong> nodes</div>
                <div><strong>{data.edge_count}</strong> edges</div>
            </div>
            {data.key_concepts && (
                <>
                    <p><strong>Key Concepts:</strong></p>
                    <div className="badges-row">
                        {data.key_concepts.map((c, i) => <span key={i} className="badge badge-purple">{c}</span>)}
                    </div>
                </>
            )}
            {data.graph_insights && <p style={{ marginTop: 12 }}>{data.graph_insights}</p>}
            {data.hidden_connections?.length > 0 && (
                <>
                    <p style={{ marginTop: 12 }}><strong>Hidden Connections:</strong></p>
                    {renderList(data.hidden_connections)}
                </>
            )}
        </SectionCard>
    );
}

export function ComparisonSection({ data }: { data: AnalysisResult['comparison'] }) {
    if (!data || 'error' in data) return null;
    return (
        <SectionCard title="Comparison Table" icon={<ArrowLeftRight size={16} />} tag="Section 4">
            {renderKeyValue(data as Record<string, unknown>)}
        </SectionCard>
    );
}

export function GapAnalysisSection({ data }: { data: AnalysisResult['gap_analysis'] }) {
    if (!data || 'error' in data) return null;
    return (
        <SectionCard title="Gap Analysis" icon={<AlertTriangle size={16} />} tag="Section 5">
            {Object.entries(data as Record<string, unknown>).map(([key, val]) => (
                <div key={key} style={{ marginBottom: 12 }}>
                    <strong style={{ textTransform: 'capitalize' }}>{key.replace(/_/g, ' ')}:</strong>
                    {Array.isArray(val) ? renderList(val) : <p>{String(val)}</p>}
                </div>
            ))}
        </SectionCard>
    );
}

export function DeepInsightsSection({ data }: { data: AnalysisResult['deep_insights'] }) {
    if (!data || 'error' in data) return null;
    return (
        <SectionCard title="Deep Insights" icon={<Lightbulb size={16} />} tag="Section 6">
            {Object.entries(data as Record<string, unknown>).map(([key, val]) => (
                <div key={key} style={{ marginBottom: 12 }}>
                    <strong style={{ textTransform: 'capitalize' }}>{key.replace(/_/g, ' ')}:</strong>
                    {Array.isArray(val) ? renderList(val) : <p>{String(val)}</p>}
                </div>
            ))}
        </SectionCard>
    );
}

export function NoveltyScoreSection({ data }: { data: AnalysisResult['novelty_score'] }) {
    if (!data) return null;
    const scores = [
        { label: 'Uniqueness', val: data.uniqueness_score },
        { label: 'Scientific Novelty', val: data.scientific_novelty_score },
        { label: 'Practical Novelty', val: data.practical_novelty_score },
        { label: 'Redundancy Risk', val: data.redundancy_risk_score },
        { label: 'Opportunity', val: data.opportunity_score },
    ];
    return (
        <SectionCard title="Novelty Score" icon={<Sparkles size={16} />} tag="Section 7">
            <div style={{ textAlign: 'center', marginBottom: 16 }}>
                <div className="score-big">{data.overall_score}/100</div>
            </div>
            {scores.map((s) => s.val !== undefined && (
                <div key={s.label} style={{ marginBottom: 10 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12 }}>
                        <span>{s.label}</span><span style={{ fontWeight: 700 }}>{s.val}</span>
                    </div>
                    <div className="score-bar"><div className="score-bar-fill" style={{ width: `${s.val}%` }} /></div>
                </div>
            ))}
            {data.explanation && <p style={{ marginTop: 12 }}>{data.explanation}</p>}
        </SectionCard>
    );
}

export function TrendForecastSection({ data }: { data: AnalysisResult['trend_forecast'] }) {
    if (!data || 'error' in data) return null;
    return (
        <SectionCard title="Trend Forecast" icon={<TrendingUp size={16} />} tag="Section 8">
            {Object.entries(data as Record<string, unknown>).map(([key, val]) => (
                <div key={key} style={{ marginBottom: 12 }}>
                    <strong style={{ textTransform: 'capitalize' }}>{key.replace(/_/g, ' ')}:</strong>
                    {Array.isArray(val) ? renderList(val) : <p>{String(val)}</p>}
                </div>
            ))}
        </SectionCard>
    );
}

export function RecommendedMethodsSection({ data }: { data: AnalysisResult['recommended_methods_datasets'] }) {
    if (!data) return null;
    return (
        <SectionCard title="Recommended Methods & Datasets" icon={<Wrench size={16} />} tag="Section 9">
            {renderKeyValue(data as Record<string, unknown>)}
        </SectionCard>
    );
}

export function ExperimentSuggestionsSection({ data }: { data: AnalysisResult['experiment_suggestions'] }) {
    if (!data) return null;
    return (
        <SectionCard title="Experiment Suggestions" icon={<FlaskConical size={16} />} tag="Section 10">
            {renderList(data)}
        </SectionCard>
    );
}

export function ResearcherRoadmapSection({ data }: { data: AnalysisResult['researcher_roadmap'] }) {
    if (!data || 'error' in data) return null;
    return (
        <SectionCard title="Researcher Roadmap" icon={<Map size={16} />} tag="Section 11">
            {Object.entries(data as Record<string, unknown>).map(([key, val]) => (
                <div key={key} style={{ marginBottom: 12 }}>
                    <strong style={{ textTransform: 'capitalize' }}>{key.replace(/_/g, ' ')}:</strong>
                    {Array.isArray(val) ? renderList(val) : typeof val === 'object' && val !== null
                        ? renderKeyValue(val as Record<string, unknown>)
                        : <p>{String(val)}</p>}
                </div>
            ))}
        </SectionCard>
    );
}

export function ArgumentStrengthSection({ data }: { data: AnalysisResult['argument_strength'] }) {
    if (!data || !Array.isArray(data) || data.length === 0) return null;
    return (
        <SectionCard title="Argument Strength" icon={<ShieldCheck size={16} />} tag="Section 12">
            <table className="data-table">
                <thead>
                    <tr><th>Claim</th><th>Strength</th><th>Reliability</th><th>Bias</th></tr>
                </thead>
                <tbody>
                    {data.map((item, i) => (
                        <tr key={i}>
                            <td>{item.claim}</td>
                            <td><span className={`badge ${item.evidence_strength === 'strong' ? 'badge-green' : item.evidence_strength === 'moderate' ? 'badge-amber' : 'badge-red'}`}>{item.evidence_strength}</span></td>
                            <td>{item.reliability}</td>
                            <td>{item.bias_indicators}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </SectionCard>
    );
}

export function ScientificCritiqueSection({ data }: { data: AnalysisResult['scientific_critique'] }) {
    if (!data || 'error' in data) return null;
    return (
        <SectionCard title="Scientific Critique" icon={<Eye size={16} />} tag="Section 13">
            {Object.entries(data as Record<string, unknown>).map(([key, val]) => (
                <div key={key} style={{ marginBottom: 12 }}>
                    <strong style={{ textTransform: 'capitalize' }}>{key.replace(/_/g, ' ')}:</strong>
                    {Array.isArray(val) ? renderList(val) : <p>{String(val)}</p>}
                </div>
            ))}
        </SectionCard>
    );
}

export function LiteratureReviewSection({ data }: { data: AnalysisResult['literature_review'] }) {
    if (!data) return null;
    return (
        <SectionCard title="Literature Review" icon={<FileText size={16} />} tag="Section 14">
            <div className="markdown-content">
                <Markdown>{data}</Markdown>
            </div>
        </SectionCard>
    );
}

export function FinalAnswerSection({ data }: { data: AnalysisResult['final_simplified_answer'] }) {
    if (!data) return null;
    return (
        <SectionCard title="Final Simplified Answer" icon={<Zap size={16} />} tag="Final" defaultOpen>
            <p>{data}</p>
        </SectionCard>
    );
}

export function ConfidenceScoreSection({ data }: { data: AnalysisResult['confidence_score'] }) {
    if (!data) return null;
    return (
        <SectionCard title="Confidence Score" icon={<Target size={16} />} tag="Section 15">
            <div style={{ textAlign: 'center', marginBottom: 12 }}>
                <div className="score-big">{data.overall}/100</div>
            </div>
            {data.factors && Object.entries(data.factors).map(([k, v]) => (
                <div key={k} style={{ marginBottom: 8 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12 }}>
                        <span>{k.replace(/_/g, ' ')}</span><span style={{ fontWeight: 700 }}>{v}</span>
                    </div>
                    <div className="score-bar"><div className="score-bar-fill" style={{ width: `${v}%` }} /></div>
                </div>
            ))}
        </SectionCard>
    );
}

export function ExplainabilityLogSection({ data }: { data: AnalysisResult['explainability_log'] }) {
    if (!data) return null;
    return (
        <SectionCard title="Explainability Log" icon={<Activity size={16} />} tag="Section 16">
            <p><strong>Agents activated:</strong> {data.total_agents}</p>
            <div className="badges-row" style={{ marginBottom: 12 }}>
                {data.agents_activated.map((a, i) => <span key={i} className="badge badge-blue">{a}</span>)}
            </div>
            {data.pipeline_metadata && renderKeyValue(data.pipeline_metadata as Record<string, unknown>)}
        </SectionCard>
    );
}

// ── Master Renderer ─────────────────────────────────────
export default function AllSections({ result }: { result: AnalysisResult }) {
    return (
        <div className="sections-list">
            <DirectAnswerSection data={result.direct_answer} />
            <FinalAnswerSection data={result.final_simplified_answer} />
            <ContextSummarySection data={result.context_summary} />
            <KnowledgeGraphSection data={result.knowledge_graph} />
            <ComparisonSection data={result.comparison} />
            <GapAnalysisSection data={result.gap_analysis} />
            <DeepInsightsSection data={result.deep_insights} />
            <NoveltyScoreSection data={result.novelty_score} />
            <TrendForecastSection data={result.trend_forecast} />
            <RecommendedMethodsSection data={result.recommended_methods_datasets} />
            <ExperimentSuggestionsSection data={result.experiment_suggestions} />
            <ResearcherRoadmapSection data={result.researcher_roadmap} />
            <ArgumentStrengthSection data={result.argument_strength} />
            <ScientificCritiqueSection data={result.scientific_critique} />
            <LiteratureReviewSection data={result.literature_review} />
            <ConfidenceScoreSection data={result.confidence_score} />
            <ExplainabilityLogSection data={result.explainability_log} />
        </div>
    );
}
