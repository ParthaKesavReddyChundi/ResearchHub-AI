import { useState, type ReactNode } from 'react';
import { ChevronDown } from 'lucide-react';

interface Props {
    title: string;
    icon: ReactNode;
    tag?: string;
    defaultOpen?: boolean;
    children: ReactNode;
}

export default function SectionCard({ title, icon, tag, defaultOpen = false, children }: Props) {
    const [open, setOpen] = useState(defaultOpen);

    return (
        <div className="card">
            <div className="card-header" onClick={() => setOpen(!open)}>
                <span className="icon">{icon}</span>
                <h3>{title}</h3>
                {tag && <span className="section-tag">{tag}</span>}
                <ChevronDown size={16} className={`chevron ${open ? 'open' : ''}`} />
            </div>
            {open && <div className="card-body">{children}</div>}
        </div>
    );
}
