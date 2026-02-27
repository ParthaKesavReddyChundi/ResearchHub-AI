"""
ResearchHub-AI — Charts
Plotly gauges and bar charts with the academic design palette.
"""

import plotly.graph_objects as go
from typing import List


def _score_color(v: float) -> str:
    if v >= 70: return "#16A34A"
    if v >= 40: return "#CA8A04"
    return "#DC2626"


def create_gauge(score: float, title: str = "", max_score: float = 100) -> go.Figure:
    color = _score_color(score)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"font": {"size": 44, "family": "Newsreader", "color": "#1A1A1A"},
                "suffix": f"/{int(max_score)}"},
        gauge={
            "axis": {"range": [0, max_score], "tickwidth": 0,
                     "tickfont": {"size": 10, "color": "#B0A999"}, "dtick": 25},
            "bar": {"color": color, "thickness": 0.28},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "rgba(220,38,38,0.04)"},
                {"range": [40, 70], "color": "rgba(202,138,4,0.04)"},
                {"range": [70, max_score], "color": "rgba(22,163,74,0.04)"},
            ],
        },
        title={"text": title, "font": {"size": 13, "family": "Inter", "color": "#8A8578"}},
    ))
    fig.update_layout(
        height=240, margin=dict(l=24, r=24, t=36, b=16),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter"},
    )
    return fig


def create_horizontal_bars(labels: List[str], values: List[float], max_value: float = 100) -> go.Figure:
    colors = [_score_color(v) for v in values]
    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker_color=colors, marker_line_width=0,
        text=[f"{v:.0f}" for v in values], textposition="auto",
        textfont={"family": "Inter", "size": 11, "color": "#fff"},
    ))
    fig.update_layout(
        height=max(160, len(labels) * 40),
        margin=dict(l=8, r=16, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(range=[0, max_value], showgrid=True, gridcolor="rgba(0,0,0,0.04)",
                   zeroline=False, tickfont={"family": "Inter", "size": 10, "color": "#B0A999"}),
        yaxis=dict(autorange="reversed",
                   tickfont={"family": "Inter", "size": 12, "color": "#4A4A4A"}),
        font={"family": "Inter"}, bargap=0.35,
    )
    return fig


def create_timing_chart(names: List[str], times: List[float]) -> go.Figure:
    max_t = max(times) if times else 1
    fig = go.Figure(go.Bar(
        x=times, y=names, orientation="h",
        marker_color=[f"rgba(0,77,77,{0.25 + 0.75*(t/max_t)})" for t in times],
        marker_line_width=0,
        text=[f"{t:.1f}s" for t in times], textposition="outside",
        textfont={"family": "Inter", "size": 11, "color": "#4A4A4A"},
    ))
    fig.update_layout(
        height=max(180, len(names) * 34),
        margin=dict(l=8, r=50, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.04)", zeroline=False,
                   tickfont={"family": "Inter", "size": 10, "color": "#B0A999"}),
        yaxis=dict(autorange="reversed",
                   tickfont={"family": "Inter", "size": 11, "color": "#4A4A4A"}),
        font={"family": "Inter"}, bargap=0.3,
    )
    return fig
