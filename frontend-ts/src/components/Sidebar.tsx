import { useLocation, useNavigate } from 'react-router-dom';
import {
    LayoutDashboard,
    FileSearch,
    FileText,
    GitGraph,
    Users,
    BarChart3,
    Settings,
} from 'lucide-react';

const navItems = [
    { icon: LayoutDashboard, path: '/', label: 'Dashboard' },
    { icon: FileSearch, path: '/analysis', label: 'Analysis' },
    { icon: FileText, path: '/papers', label: 'Papers' },
    { icon: GitGraph, path: '/graph', label: 'Graph' },
    { icon: Users, path: '/agents', label: 'Agents' },
    { icon: BarChart3, path: '/insights', label: 'Insights' },
];

export default function Sidebar() {
    const location = useLocation();
    const navigate = useNavigate();

    return (
        <aside className="sidebar">
            <div className="sidebar-logo">R</div>
            <nav className="sidebar-nav">
                {navItems.map((item) => (
                    <button
                        key={item.label}
                        className={`sidebar-btn ${location.pathname === item.path ? 'active' : ''}`}
                        onClick={() => navigate(item.path)}
                        title={item.label}
                    >
                        <item.icon size={20} />
                    </button>
                ))}
            </nav>
            <div className="sidebar-bottom">
                <button className="sidebar-btn" title="Settings">
                    <Settings size={20} />
                </button>
            </div>
        </aside>
    );
}
