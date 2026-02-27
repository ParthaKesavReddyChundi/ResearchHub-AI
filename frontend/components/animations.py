"""
ResearchHub-AI — Loading Animations
Pipeline agent progress indicator during the 30-90 second analysis.
"""

import streamlit as st
import time

PIPELINE_STAGES = [
    ("🔍", "Searching papers across arXiv & PubMed"),
    ("📄", "Summarizing research papers"),
    ("⚖️", "Comparing methodologies & findings"),
    ("🧠", "Extracting deep insights"),
    ("🚧", "Identifying research gaps"),
    ("🌐", "Building knowledge graph"),
    ("🌟", "Scoring novelty & uniqueness"),
    ("📈", "Forecasting research trends"),
    ("🧪", "Critiquing methodologies"),
    ("🗺️", "Generating researcher roadmap"),
    ("📚", "Writing literature review"),
    ("✅", "Assembling final output"),
]


def render_agent_progress(stage_index: int) -> str:
    """Render the pipeline progress indicator with Elicit-like minimal style."""
    parts = ['<div style="max-width:560px; margin:16px auto; font-family:Inter,sans-serif;">']

    for i, (emoji, label) in enumerate(PIPELINE_STAGES):
        if i < stage_index:
            parts.append(f"""
            <div style="display:flex; align-items:center; gap:10px; padding:8px 14px;
                        margin-bottom:4px; border-radius:6px; opacity:0.55;">
                <span style="font-size:0.9rem; color:#16A34A;">✓</span>
                <span style="font-size:0.85rem; text-decoration:line-through; color:#8A8578;">
                    {emoji} {label}
                </span>
            </div>
            """)
        elif i == stage_index:
            parts.append(f"""
            <div style="display:flex; align-items:center; gap:10px; padding:10px 16px;
                        margin-bottom:4px; border-radius:8px;
                        background:#E6F2F0; border:1px solid #B0D8D2;">
                <span style="font-size:1.05rem;">{emoji}</span>
                <span style="font-size:0.9rem; font-weight:600; color:#004D4D;">
                    {label}...
                </span>
                <span style="margin-left:auto; display:inline-block; width:8px; height:8px;
                             border-radius:50%; background:#004D4D;
                             animation: blink 1.2s ease infinite;"></span>
            </div>
            <style>
                @keyframes blink {{
                    0%, 100% {{ opacity: 0.3; }}
                    50% {{ opacity: 1; }}
                }}
            </style>
            """)
        else:
            parts.append(f"""
            <div style="display:flex; align-items:center; gap:10px; padding:8px 14px;
                        margin-bottom:4px; border-radius:6px; opacity:0.35;">
                <span style="font-size:0.9rem;">{emoji}</span>
                <span style="font-size:0.85rem; color:#B0A999;">{label}</span>
            </div>
            """)

    parts.append("</div>")
    return "\n".join(parts)
