import { Activity } from 'lucide-react';

interface Props {
    pipelineTime?: number;
    agentsCount?: number;
}

export default function SystemStatus({ pipelineTime, agentsCount }: Props) {
    return (
        <div className="status-card">
            <h3>
                <Activity size={16} style={{ color: 'var(--amber)' }} />
                System Status
            </h3>
            <div className="status-row">
                <span className="label">Status</span>
                <span className="value green">Operational</span>
            </div>
            <div className="status-row">
                <span className="label">Active Agents</span>
                <span className="value blue">{agentsCount ?? 11}</span>
            </div>
            <div className="status-row">
                <span className="label">Pipeline Version</span>
                <span className="value">v4.0</span>
            </div>
            <div className="status-row">
                <span className="label">Data Sources</span>
                <span className="value amber">arXiv, PubMed</span>
            </div>
            {pipelineTime !== undefined && (
                <div className="status-row">
                    <span className="label">Last Run</span>
                    <span className="value">{pipelineTime}s</span>
                </div>
            )}
        </div>
    );
}
