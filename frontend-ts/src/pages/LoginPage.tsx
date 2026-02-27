import { useState, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Sparkles } from 'lucide-react';

export default function LoginPage() {
    const [tab, setTab] = useState<'login' | 'register'>('login');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(false);
    const { login, register } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        setLoading(true);

        try {
            if (tab === 'login') {
                await login(email, password);
                navigate('/');
            } else {
                const msg = await register(email, password);
                setSuccess(msg || 'Registered successfully! You can now login.');
                setTab('login');
            }
        } catch (err: unknown) {
            if (err && typeof err === 'object' && 'response' in err) {
                const axiosErr = err as { response?: { data?: { detail?: string } } };
                setError(axiosErr.response?.data?.detail || 'Something went wrong');
            } else {
                setError('Network error — is the backend running?');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-page">
            <div className="login-card">
                <h1>
                    <Sparkles size={24} style={{ color: 'var(--accent)' }} />
                    ResearchHub AI
                </h1>
                <p className="subtitle">Multi-agent scientific reasoning system</p>

                <div className="tabs">
                    <button
                        className={`tab ${tab === 'login' ? 'active' : ''}`}
                        onClick={() => { setTab('login'); setError(''); setSuccess(''); }}
                    >
                        Sign In
                    </button>
                    <button
                        className={`tab ${tab === 'register' ? 'active' : ''}`}
                        onClick={() => { setTab('register'); setError(''); setSuccess(''); }}
                    >
                        Register
                    </button>
                </div>

                {error && <div className="error-msg">{error}</div>}
                {success && <div className="success-msg">{success}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="you@example.com"
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="••••••••"
                            required
                            minLength={6}
                        />
                    </div>
                    <button
                        type="submit"
                        className="btn btn-primary btn-full"
                        disabled={loading}
                    >
                        {loading ? 'Please wait...' : tab === 'login' ? 'Sign In' : 'Create Account'}
                    </button>
                </form>
            </div>
        </div>
    );
}
