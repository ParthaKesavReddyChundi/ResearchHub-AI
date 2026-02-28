interface Props {
    timing: Record<string, number>;
}

const labelMap: Record<string, string> = {
    intent_classification: 'intent classification',
    paper_search: 'paper search',
    summarizer: 'summarizer',
    comparison_and_insight: 'comparison and insight',
    gap_analysis: 'gap analysis',
    parallel_agents: 'parallel agents',
    literature_review: 'literature review',
    final_answer: 'final answer',
};

export default function TimingCards({ timing }: Props) {
    return (
        <div className="timing-grid">
            {Object.entries(timing).map(([key, value]) => (
                <div className="timing-card" key={key}>
                    <div className="label">{labelMap[key] || key.replace(/_/g, ' ')}</div>
                    <div className="value">{typeof value === 'number' ? `${value}s` : value}</div>
                </div>
            ))}
        </div>
    );
}
