"""
ResearchHub-AI — Design System
Inspired by Elicit and Litmaps: warm academic palette, serif headings,
generous whitespace, clean cards, and sophisticated color hierarchy.
"""


def get_global_css() -> str:
    return """
<style>
/* ── Google Fonts ─────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Root Variables ───────────────────────────────────────── */
:root {
    --teal: #004D4D;
    --teal-light: #006D6D;
    --teal-muted: #3D8B8B;
    --cream: #FAF8F3;
    --cream-dark: #F2EDE4;
    --warm-white: #FEFDFB;
    --card-bg: #FFFFFF;
    --card-border: #E8E3DA;
    --card-hover-border: #CBBFAF;
    --text-primary: #1A1A1A;
    --text-secondary: #4A4A4A;
    --text-muted: #8A8578;
    --text-light: #B0A999;
    --accent-green: #1D8B6F;
    --accent-blue: #2563EB;
    --accent-coral: #E05A47;
    --accent-amber: #D4930D;
    --success: #16A34A;
    --warning: #CA8A04;
    --danger: #DC2626;
    --shadow-xs: 0 1px 2px rgba(0,0,0,0.04);
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.04), 0 2px 4px rgba(0,0,0,0.03);
    --shadow-lg: 0 10px 15px rgba(0,0,0,0.06), 0 4px 6px rgba(0,0,0,0.03);
    --radius: 12px;
    --radius-sm: 8px;
    --radius-xs: 6px;
    --serif: 'Newsreader', 'Georgia', 'Times New Roman', serif;
    --sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* ── Global Typography ────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: var(--sans) !important;
    color: var(--text-primary) !important;
}
.stApp {
    background: var(--cream) !important;
}

h1, .stMarkdown h1 {
    font-family: var(--serif) !important;
    font-weight: 500 !important;
    color: var(--teal) !important;
    letter-spacing: -0.02em !important;
    line-height: 1.2 !important;
}
h2, .stMarkdown h2 {
    font-family: var(--serif) !important;
    font-weight: 500 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.01em !important;
}
h3, h4, h5, h6,
.stMarkdown h3, .stMarkdown h4 {
    font-family: var(--sans) !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
}
p, li, span, div, label {
    font-family: var(--sans) !important;
}

/* ── Hide Streamlit Chrome ────────────────────────────────── */
#MainMenu, header, footer, .stDeployButton,
[data-testid="stSidebarNav"],
div[data-testid="stSidebarNavItems"],
section[data-testid="stSidebar"] > div > div:first-child > ul {
    display: none !important;
}

/* ── Sidebar ──────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: var(--warm-white) !important;
    border-right: 1px solid var(--card-border) !important;
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2 {
    font-family: var(--serif) !important;
    color: var(--teal) !important;
    font-size: 1.15rem !important;
}

/* ── Card System ──────────────────────────────────────────── */
.card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: var(--radius);
    padding: 28px 32px;
    margin-bottom: 16px;
    box-shadow: var(--shadow-xs);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    animation: fadeIn 0.4s ease both;
}
.card:hover {
    border-color: var(--card-hover-border);
    box-shadow: var(--shadow-md);
}

/* Hero card — dark teal background */
.hero-card {
    background: var(--teal);
    border: none;
    border-radius: var(--radius);
    padding: 40px 44px;
    margin-bottom: 20px;
    color: #fff !important;
    box-shadow: var(--shadow-lg);
    animation: fadeIn 0.4s ease both;
}
.hero-card *, .hero-card h2, .hero-card h3, .hero-card p, .hero-card span {
    color: #fff !important;
}

/* Section card with left accent */
.section-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-left: 3px solid var(--teal);
    border-radius: 2px var(--radius) var(--radius) 2px;
    padding: 28px 32px;
    margin-bottom: 16px;
    box-shadow: var(--shadow-xs);
    animation: fadeIn 0.4s ease both;
}

/* Section header inside cards */
.section-hdr {
    margin-bottom: 20px;
    padding-bottom: 14px;
    border-bottom: 1px solid var(--card-border);
}
.section-hdr .sec-emoji {
    font-size: 1.3rem;
    margin-right: 10px;
}
.section-hdr .sec-title {
    font-family: var(--serif);
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--text-primary);
}
.section-hdr .sec-sub {
    display: block;
    font-family: var(--sans);
    font-size: 0.82rem;
    color: var(--text-muted);
    margin-top: 3px;
    font-weight: 400;
}

/* ── Badges & Pills ───────────────────────────────────────── */
.pill {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 600;
    font-family: var(--sans);
    letter-spacing: 0.03em;
    text-transform: uppercase;
}
.pill-teal { background: #E6F2F0; color: var(--teal); }
.pill-green { background: #ECFDF5; color: #15803D; }
.pill-red { background: #FEF2F2; color: #B91C1C; }
.pill-amber { background: #FFFBEB; color: #92400E; }
.pill-blue { background: #EFF6FF; color: #1D4ED8; }
.pill-gray { background: #F3F4F6; color: #4B5563; }

.tag {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 6px;
    font-size: 0.82rem;
    font-weight: 500;
    font-family: var(--sans);
    margin: 2px 3px;
    background: var(--cream);
    color: var(--text-secondary);
    border: 1px solid var(--card-border);
}
.tag-teal { background: #E6F2F0; border-color: #B0D8D2; color: var(--teal); }
.tag-green { background: #ECFDF5; border-color: #A7F3D0; color: #15803D; }
.tag-red { background: #FEF2F2; border-color: #FECACA; color: #B91C1C; }
.tag-amber { background: #FFFBEB; border-color: #FDE68A; color: #92400E; }
.tag-blue { background: #EFF6FF; border-color: #BFDBFE; color: #1D4ED8; }

/* ── Buttons ──────────────────────────────────────────────── */
.stButton > button {
    background: var(--teal) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    font-family: var(--sans) !important;
    font-size: 0.88rem !important;
    transition: all 0.2s ease !important;
    box-shadow: var(--shadow-sm) !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    background: var(--teal-light) !important;
    box-shadow: var(--shadow-md) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Text Inputs ──────────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border: 1.5px solid var(--card-border) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--sans) !important;
    font-size: 0.92rem !important;
    padding: 12px 16px !important;
    background: var(--card-bg) !important;
    color: var(--text-primary) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 3px rgba(0,77,77,0.08) !important;
}

/* Large search input */
.big-search .stTextInput > div > div > input {
    font-size: 1.05rem !important;
    padding: 16px 24px !important;
    border-radius: 50px !important;
    border: 2px solid var(--card-border) !important;
    background: var(--card-bg) !important;
}
.big-search .stTextInput > div > div > input:focus {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 4px rgba(0,77,77,0.06) !important;
}

/* ── Expanders ────────────────────────────────────────────── */
details[data-testid="stExpander"] {
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: var(--radius-sm) !important;
    box-shadow: none !important;
    margin-bottom: 8px !important;
}
.streamlit-expanderHeader {
    font-family: var(--sans) !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    color: var(--text-primary) !important;
}

/* ── Tabs ─────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 1px solid var(--card-border);
}
.stTabs [data-baseweb="tab"] {
    font-family: var(--sans) !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    padding: 10px 20px !important;
    border-radius: 0 !important;
    color: var(--text-muted) !important;
}
.stTabs [aria-selected="true"] {
    color: var(--teal) !important;
    border-bottom: 2px solid var(--teal) !important;
    background: transparent !important;
}

/* ── Metric Cards ─────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: var(--radius-sm);
    padding: 16px 20px;
}
[data-testid="stMetricLabel"] {
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    color: var(--text-muted) !important;
}

/* ── Score Bars ────────────────────────────────────────────── */
.score-bar {
    width: 100%;
    height: 8px;
    background: var(--cream-dark);
    border-radius: 4px;
    overflow: hidden;
    margin: 4px 0 12px;
}
.score-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.8s ease;
}
.fill-green { background: var(--success); }
.fill-amber { background: var(--warning); }
.fill-red { background: var(--danger); }

/* ── Stat Box ─────────────────────────────────────────────── */
.stat-box {
    text-align: center;
    padding: 16px 12px;
    border-radius: var(--radius-sm);
    background: var(--cream);
    border: 1px solid var(--card-border);
}
.stat-box .stat-val {
    font-family: var(--serif);
    font-size: 1.8rem;
    font-weight: 600;
    color: var(--teal);
    line-height: 1.2;
}
.stat-box .stat-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-muted);
    margin-top: 4px;
}

/* ── Agent Pipeline ───────────────────────────────────────── */
.agent-pill {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 100px;
    font-size: 0.78rem;
    font-weight: 500;
    margin: 3px;
    font-family: var(--sans);
}
.agent-done {
    background: #ECFDF5;
    color: #15803D;
    border: 1px solid #A7F3D0;
}
.agent-active {
    background: var(--teal);
    color: #fff;
    animation: pulse-agent 1.5s ease infinite;
}
.agent-idle {
    background: var(--cream);
    color: var(--text-light);
    border: 1px solid var(--card-border);
}

/* ── Animations ───────────────────────────────────────────── */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulse-agent {
    0%, 100% { box-shadow: 0 0 0 0 rgba(0,77,77,0.2); }
    50% { box-shadow: 0 0 0 6px rgba(0,77,77,0); }
}

/* Stagger delays */
.delay-1 { animation-delay: 0.05s !important; }
.delay-2 { animation-delay: 0.10s !important; }
.delay-3 { animation-delay: 0.15s !important; }
.delay-4 { animation-delay: 0.20s !important; }
.delay-5 { animation-delay: 0.25s !important; }
.delay-6 { animation-delay: 0.30s !important; }

/* ── Login Page ───────────────────────────────────────────── */
.login-wrap {
    max-width: 420px;
    margin: 80px auto 0;
    animation: fadeIn 0.5s ease both;
}
.login-brand {
    text-align: center;
    margin-bottom: 32px;
}
.login-brand h1 {
    font-family: var(--serif) !important;
    font-size: 2.2rem !important;
    font-weight: 500 !important;
    color: var(--teal) !important;
    margin-bottom: 6px !important;
}
.login-brand p {
    font-size: 0.92rem;
    color: var(--text-muted);
}

/* ── History Card ─────────────────────────────────────────── */
.history-item {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: var(--radius-sm);
    padding: 18px 22px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    animation: fadeIn 0.3s ease both;
}
.history-item:hover {
    border-color: var(--teal-muted);
    box-shadow: var(--shadow-sm);
}

/* ── Paper Item ───────────────────────────────────────────── */
.paper-item {
    padding: 14px 18px;
    border-bottom: 1px solid var(--card-border);
    transition: background 0.15s ease;
}
.paper-item:hover {
    background: var(--cream);
}
.paper-item:last-child {
    border-bottom: none;
}

/* ── Coming Soon ──────────────────────────────────────────── */
.soon-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: var(--cream);
    border: 1px dashed var(--card-hover-border);
    border-radius: var(--radius-sm);
    padding: 12px 20px;
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--text-muted);
}

/* ── Misc ─────────────────────────────────────────────────── */
.divider {
    height: 1px;
    background: var(--card-border);
    margin: 20px 0;
}
.muted { color: var(--text-muted); }
.small { font-size: 0.82rem; }

/* ── Scrollbar ────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--card-border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--card-hover-border); }

/* ── Responsive ───────────────────────────────────────────── */
@media (max-width: 768px) {
    .card, .section-card { padding: 20px 18px; }
    .hero-card { padding: 28px 24px; }
}
</style>
"""
