import re
import json
import requests
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="StepWise AI",
    layout="wide",
    initial_sidebar_state="collapsed",
)

LOCAL_MODEL_URL = "http://127.0.0.1:8080/v1/chat/completions"

# ─── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,600;1,9..144,300&display=swap');

:root {
    --bg:          #fafaf9;
    --surface:     #ffffff;
    --surface2:    #f4f4f2;
    --border:      #e7e5e0;
    --border2:     #d0cdc6;
    --text:        #18181b;
    --text2:       #52525b;
    --muted:       #a1a1aa;
    --accent:      #6366f1;
    --accent-dark: #4f46e5;
    --accent-bg:   #eef2ff;
    --accent-bdr:  #c7d2fe;
    --green:       #059669;
    --green-dark:  #047857;
    --green-bg:    #ecfdf5;
    --green-bdr:   #a7f3d0;
    --red:         #e11d48;
    --red-dark:    #be123c;
    --red-bg:      #fff1f2;
    --red-bdr:     #fecdd3;
    --amber:       #d97706;
    --amber-bg:    #fffbeb;
    --amber-bdr:   #fde68a;
    --mono:        'JetBrains Mono', monospace;
    --sans:        'Inter', sans-serif;
    --serif:       'Fraunces', serif;
    --r-sm:        6px;
    --r-md:        10px;
    --r-lg:        14px;
    --r-xl:        20px;
    --sh:          0 1px 2px rgba(0,0,0,0.05);
    --sh-md:       0 4px 16px rgba(0,0,0,0.07), 0 1px 3px rgba(0,0,0,0.04);
    --sh-lg:       0 12px 40px rgba(0,0,0,0.10), 0 2px 8px rgba(0,0,0,0.05);
}

html, body, [class*="css"] {
    font-family: var(--sans) !important;
    background: var(--bg) !important;
    color: var(--text) !important;
    -webkit-font-smoothing: antialiased;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1320px !important;
}

/* ── Wordmark ── */
.brand {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 4px;
}
.brand-name {
    font-family: var(--serif);
    font-size: 1.7rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: var(--text);
    line-height: 1;
}
.brand-pill {
    font-family: var(--mono);
    font-size: 0.58rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    background: var(--accent-bg);
    border: 1px solid var(--accent-bdr);
    padding: 3px 10px;
    border-radius: 99px;
    margin-top: 2px;
}
.brand-tagline {
    font-size: 0.8rem;
    color: var(--muted);
    margin-bottom: 2rem;
    line-height: 1.5;
}

/* ── Mode tabs ── */
.mode-tabs {
    display: flex;
    background: var(--surface2);
    border-radius: var(--r-md);
    padding: 3px;
    margin-bottom: 1.75rem;
    border: 1px solid var(--border);
}
.mode-tab {
    flex: 1;
    text-align: center;
    padding: 7px 12px;
    border-radius: 7px;
    font-size: 0.8rem;
    font-weight: 500;
    cursor: pointer;
    color: var(--muted);
    transition: all 0.18s;
    border: none;
    background: transparent;
}
.mode-tab.active {
    background: var(--surface);
    color: var(--text);
    box-shadow: var(--sh-md);
    font-weight: 600;
}

/* ── Field labels ── */
.field-label {
    font-family: var(--mono);
    font-size: 0.6rem;
    font-weight: 500;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.field-label-dot {
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--border2);
    display: inline-block;
}

/* ── Textarea ── */
textarea, .stTextArea textarea {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--r-md) !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
    line-height: 1.75 !important;
    padding: 12px 14px !important;
    box-shadow: var(--sh) !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
    resize: none !important;
}
textarea:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
    outline: none !important;
}
.stTextArea { margin-bottom: 0 !important; }
[data-testid="stTextArea"] { margin-bottom: 0 !important; }

/* ── CTA button ── */
.stButton > button {
    background: #18181b !important;
    color: #ffffff !important;
    border: none !important;
    font-family: var(--sans) !important;
    font-size: 0.875rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    padding: 13px 28px !important;
    border-radius: var(--r-lg) !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2), 0 4px 12px rgba(0,0,0,0.12) !important;
    transition: all 0.15s !important;
    width: 100% !important;
    margin-top: 1.25rem !important;
}
.stButton > button:hover {
    background: #27272a !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.22), 0 1px 4px rgba(0,0,0,0.14) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
    background: #09090b !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: var(--surface) !important;
    border: 1.5px solid var(--border2) !important;
    border-radius: var(--r-md) !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    box-shadow: var(--sh) !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* ─────────────── RIGHT PANEL ─────────────── */

/* ── Score banner ── */
.score-banner {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px 24px;
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--r-lg);
    box-shadow: var(--sh-md);
    margin-bottom: 1.75rem;
}
.score-verdict {
    display: flex;
    align-items: center;
    gap: 10px;
    flex: 1;
}
.verdict-icon {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.verdict-icon-ok  { background: var(--green-bg);  color: var(--green); }
.verdict-icon-err { background: var(--red-bg);    color: var(--red); }
.verdict-label {
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}
.verdict-label-ok  { color: var(--green); }
.verdict-label-err { color: var(--red); }
.score-chips {
    display: flex;
    gap: 10px;
    align-items: center;
}
.score-chip {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 8px 16px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    min-width: 70px;
}
.chip-label {
    font-family: var(--mono);
    font-size: 0.55rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 4px;
}
.chip-val {
    font-family: var(--sans);
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
}
.conf-chip-low  { color: var(--red);   background: var(--red-bg);   border-color: var(--red-bdr);   }
.conf-chip-med  { color: var(--amber); background: var(--amber-bg); border-color: var(--amber-bdr); }
.conf-chip-high { color: var(--green); background: var(--green-bg); border-color: var(--green-bdr); }
.chip-val-conf {
    font-family: var(--mono);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
}

/* ── Section heading ── */
.sec-head {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 1.75rem 0 0.75rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.sec-head::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Diff block ── */
.diff-wrap {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--r-lg);
    overflow: hidden;
    box-shadow: var(--sh);
}
.diff-row {
    display: flex;
    align-items: stretch;
    border-bottom: 1px solid var(--border);
    transition: background 0.1s;
}
.diff-row:last-child { border-bottom: none; }
.diff-gutter {
    width: 44px;
    min-width: 44px;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    padding: 13px 0 0;
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 500;
    user-select: none;
    flex-shrink: 0;
    border-right: 1px solid var(--border);
}
.diff-gutter-ok    { background: var(--surface2); color: var(--muted); }
.diff-gutter-wrong { background: var(--red-bg);   color: var(--red-dark); font-weight: 700; }
.diff-body-ok    { background: var(--surface); }
.diff-body-wrong { background: #fff5f7; }
.diff-content { padding: 11px 16px; flex: 1; font-family: var(--mono); font-size: 0.83rem; line-height: 1.6; }
.diff-line-ok { color: var(--text2); }
.diff-badge-wrong {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-family: var(--mono);
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: var(--red);
    background: var(--red-bg);
    border: 1px solid var(--red-bdr);
    padding: 1px 7px;
    border-radius: 99px;
    margin-bottom: 4px;
}
.diff-line-wrong {
    color: var(--red);
    text-decoration: line-through;
    text-decoration-color: rgba(225,29,72,0.35);
    opacity: 0.75;
    font-weight: 500;
}
.diff-arrow { color: var(--muted); font-size: 0.7rem; margin: 3px 0 1px; }
.diff-line-fix {
    color: var(--green-dark);
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
}
.diff-fix-badge {
    font-size: 0.58rem;
    letter-spacing: 0.1em;
    font-weight: 600;
    text-transform: uppercase;
    color: var(--green);
    background: var(--green-bg);
    border: 1px solid var(--green-bdr);
    padding: 1px 7px;
    border-radius: 99px;
}

/* ── Error detail cards ── */
.err-card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--r-lg);
    overflow: hidden;
    margin-bottom: 10px;
    box-shadow: var(--sh);
}
.err-card-head {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 16px;
    background: var(--red-bg);
    border-bottom: 1px solid var(--red-bdr);
}
.err-card-line-badge {
    font-family: var(--mono);
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--red);
    background: #fff;
    border: 1px solid var(--red-bdr);
    padding: 3px 10px;
    border-radius: 99px;
}
.err-card-body { padding: 14px 16px; }
.err-row-label {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 4px;
    margin-top: 12px;
}
.err-row-label:first-child { margin-top: 0; }
.err-why-text { font-size: 0.85rem; color: var(--text2); line-height: 1.55; }
.err-fix-text {
    font-size: 0.85rem;
    color: var(--green-dark);
    line-height: 1.55;
    font-weight: 500;
    display: flex;
    align-items: flex-start;
    gap: 6px;
}
.err-fix-text::before { content: "→"; color: var(--green); font-weight: 700; flex-shrink: 0; margin-top: 1px; }

/* ── Hint card ── */
.hint-card {
    background: linear-gradient(135deg, var(--accent-bg) 0%, #f5f3ff 100%);
    border: 1.5px solid var(--accent-bdr);
    border-radius: var(--r-lg);
    padding: 16px 18px;
    margin: 0.25rem 0;
    box-shadow: var(--sh);
}
.hint-card-label {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.hint-card-text { font-size: 0.875rem; color: #3730a3; line-height: 1.6; font-weight: 400; }

/* ── Solution card ── */
.sol-card {
    background: var(--green-bg);
    border: 1.5px solid var(--green-bdr);
    border-radius: var(--r-lg);
    padding: 16px 18px;
    box-shadow: var(--sh);
}
.sol-label {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--green);
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.sol-body {
    font-family: var(--mono);
    font-size: 0.83rem;
    line-height: 2;
    color: var(--green-dark);
    white-space: pre;
}

/* ── Markets ── */
.summary-card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--r-lg);
    padding: 18px 22px;
    box-shadow: var(--sh-md);
}
.summary-body { font-size: 0.95rem; color: var(--text2); line-height: 1.7; }
.chain-wrap {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--r-lg);
    overflow: hidden;
    box-shadow: var(--sh);
}
.chain-row {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 14px 18px;
    border-bottom: 1px solid var(--border);
}
.chain-row:last-child { border-bottom: none; }
.chain-num {
    width: 26px; height: 26px;
    border-radius: 50%;
    background: var(--accent-bg);
    border: 1.5px solid var(--accent-bdr);
    display: flex; align-items: center; justify-content: center;
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--accent);
    flex-shrink: 0;
    margin-top: 1px;
}
.chain-text { font-size: 0.875rem; color: var(--text2); line-height: 1.55; padding-top: 3px; }
.impact-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}
.impact-cell {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--r-md);
    padding: 14px 16px;
    box-shadow: var(--sh);
}
.impact-label {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 6px;
}
.impact-text { font-size: 0.84rem; color: var(--text2); line-height: 1.5; }
.assumption-row {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.84rem;
    color: var(--text2);
    line-height: 1.5;
}
.assumption-row:last-child { border-bottom: none; }
.assumption-row::before {
    content: '◦';
    color: var(--muted);
    font-size: 0.9rem;
    flex-shrink: 0;
    margin-top: 1px;
}

/* ── Await state ── */
.await-shell {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 60vh;
    text-align: center;
    gap: 12px;
}
.await-ring {
    width: 56px; height: 56px;
    border-radius: 50%;
    border: 2px solid var(--border2);
    display: flex; align-items: center; justify-content: center;
    color: var(--border2);
    font-size: 1.4rem;
    margin-bottom: 4px;
}
.await-title {
    font-family: var(--serif);
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text2);
    letter-spacing: -0.02em;
}
.await-sub { font-size: 0.82rem; color: var(--muted); line-height: 1.6; }

/* ── Footer ── */
.app-footer {
    margin-top: 3rem;
    padding-top: 1.25rem;
    border-top: 1px solid var(--border);
    font-family: var(--mono);
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    display: flex;
    gap: 16px;
}
.footer-dot { color: var(--border2); }


/* ── Code mode ── */
.lang-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: var(--mono);
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 99px;
    background: #1e1e2e;
    color: #cdd6f4;
    border: 1px solid #313244;
}
.code-diff-wrap {
    background: #1e1e2e;
    border: 1.5px solid #313244;
    border-radius: var(--r-lg);
    overflow: hidden;
    box-shadow: var(--sh-md);
}
.code-diff-row {
    display: flex;
    align-items: stretch;
    border-bottom: 1px solid #313244;
}
.code-diff-row:last-child { border-bottom: none; }
.code-gutter {
    width: 44px;
    min-width: 44px;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    padding: 12px 0 0;
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 500;
    user-select: none;
    flex-shrink: 0;
    border-right: 1px solid #313244;
    color: #6c7086;
    background: #181825;
}
.code-gutter-wrong {
    background: rgba(243,139,168,0.12);
    color: #f38ba8;
    font-weight: 700;
}
.code-content {
    padding: 10px 16px;
    flex: 1;
    font-family: var(--mono);
    font-size: 0.82rem;
    line-height: 1.7;
}
.code-ok   { background: #1e1e2e; color: #cdd6f4; }
.code-wrong-bg { background: rgba(243,139,168,0.06); }
.code-line-ok { color: #cdd6f4; }
.code-line-wrong {
    color: #f38ba8;
    text-decoration: line-through;
    text-decoration-color: rgba(243,139,168,0.4);
    opacity: 0.8;
}
.code-badge-wrong {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.58rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: #f38ba8;
    background: rgba(243,139,168,0.15);
    border: 1px solid rgba(243,139,168,0.3);
    padding: 1px 7px;
    border-radius: 99px;
    margin-bottom: 4px;
}
.code-arrow { color: #6c7086; font-size: 0.7rem; margin: 2px 0; }
.code-line-fix { color: #a6e3a1; font-weight: 500; }
.code-fix-badge {
    font-size: 0.58rem;
    letter-spacing: 0.1em;
    font-weight: 600;
    text-transform: uppercase;
    color: #a6e3a1;
    background: rgba(166,227,161,0.15);
    border: 1px solid rgba(166,227,161,0.3);
    padding: 1px 7px;
    border-radius: 99px;
    margin-right: 6px;
}
.code-err-card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--r-lg);
    overflow: hidden;
    margin-bottom: 10px;
    box-shadow: var(--sh);
}
.code-err-head {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 16px;
    background: #fff1f2;
    border-bottom: 1px solid var(--red-bdr);
}
.fixed-sol-block {
    background: #1e1e2e;
    border: 1.5px solid #313244;
    border-radius: var(--r-lg);
    padding: 16px 18px;
    box-shadow: var(--sh-md);
}
.fixed-sol-label {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #a6e3a1;
    margin-bottom: 10px;
    display: block;
}
.fixed-sol-body {
    font-family: var(--mono);
    font-size: 0.82rem;
    line-height: 1.9;
    color: #cdd6f4;
    white-space: pre;
    overflow-x: auto;
}


/* ══════════════ MARKETS MODE ══════════════ */
.thesis-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    border: 1.5px solid #312e81;
    border-radius: var(--r-lg);
    padding: 22px 24px;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(99,102,241,0.2);
    position: relative;
    overflow: hidden;
}
.thesis-card::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 140px; height: 140px;
    border-radius: 50%;
    background: rgba(99,102,241,0.08);
}
.thesis-overline {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #818cf8;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.thesis-text {
    font-family: var(--serif);
    font-size: 1.1rem;
    font-weight: 300;
    font-style: italic;
    color: #e0e7ff;
    line-height: 1.65;
    margin-bottom: 14px;
    letter-spacing: -0.01em;
}
.thesis-meta {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}
.regime-pill {
    font-family: var(--mono);
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #fbbf24;
    background: rgba(251,191,36,0.12);
    border: 1px solid rgba(251,191,36,0.3);
    padding: 4px 12px;
    border-radius: 99px;
}
.thesis-conf-pill {
    font-family: var(--mono);
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    padding: 4px 12px;
    border-radius: 99px;
}
.tcp-low  { color:#f87171;background:rgba(248,113,113,0.12);border:1px solid rgba(248,113,113,0.3); }
.tcp-med  { color:#fbbf24;background:rgba(251,191,36,0.12); border:1px solid rgba(251,191,36,0.3);  }
.tcp-high { color:#34d399;background:rgba(52,211,153,0.12); border:1px solid rgba(52,211,153,0.3);  }

/* Causal chain */
.chain-timeline {
    position: relative;
    padding-left: 28px;
}
.chain-timeline::before {
    content: '';
    position: absolute;
    left: 10px; top: 8px; bottom: 8px;
    width: 1.5px;
    background: linear-gradient(to bottom, var(--accent), transparent);
}
.ct-row {
    position: relative;
    margin-bottom: 12px;
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--r-md);
    padding: 12px 14px;
    box-shadow: var(--sh);
}
.ct-row::before {
    content: '';
    position: absolute;
    left: -22px; top: 50%;
    transform: translateY(-50%);
    width: 9px; height: 9px;
    border-radius: 50%;
    background: var(--accent);
    border: 2px solid var(--bg);
    box-shadow: 0 0 0 2px var(--accent-bdr);
}
.ct-row:last-child { margin-bottom: 0; }
.ct-step { font-size: 0.875rem; color: var(--text); line-height: 1.5; margin-bottom: 6px; }
.ct-badges {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
}
.ct-badge {
    font-family: var(--mono);
    font-size: 0.58rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    padding: 2px 8px;
    border-radius: 99px;
}
.ct-conf-low  { color:var(--red);  background:var(--red-bg);  border:1px solid var(--red-bdr);  }
.ct-conf-med  { color:var(--amber);background:var(--amber-bg);border:1px solid var(--amber-bdr); }
.ct-conf-high { color:var(--green);background:var(--green-bg);border:1px solid var(--green-bdr); }
.ct-lag { color:var(--muted);background:var(--surface2);border:1px solid var(--border);
          font-family:var(--mono);font-size:0.58rem;font-weight:500;letter-spacing:0.06em;
          padding:2px 8px;border-radius:99px; }

/* Asset grid */
.asset-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}
.asset-cell {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--r-md);
    padding: 14px 16px;
    box-shadow: var(--sh);
}
.asset-label { font-family:var(--mono);font-size:0.58rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--muted);margin-bottom:8px; }
.asset-direction {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    padding: 3px 10px;
    border-radius: 99px;
    margin-bottom: 8px;
}
.dir-bull { color:var(--green);background:var(--green-bg);border:1px solid var(--green-bdr); }
.dir-bear { color:var(--red);  background:var(--red-bg);  border:1px solid var(--red-bdr);  }
.dir-neut { color:var(--muted);background:var(--surface2);border:1px solid var(--border);   }
.asset-mag {
    font-family:var(--mono);font-size:0.58rem;font-weight:500;letter-spacing:0.08em;
    color:var(--muted);background:var(--surface2);border:1px solid var(--border);
    padding:2px 7px;border-radius:99px;margin-left:4px;
}
.asset-reasoning { font-size:0.8rem;color:var(--text2);line-height:1.5; }

/* Assumptions */
.assumption-card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--r-md);
    padding: 14px 16px;
    margin-bottom: 8px;
    box-shadow: var(--sh);
}
.assumption-text { font-size:0.875rem;color:var(--text);line-height:1.5;margin-bottom:6px;font-weight:500; }
.vuln-label {
    font-family:var(--mono);font-size:0.58rem;letter-spacing:0.1em;text-transform:uppercase;
    color:var(--amber);margin-bottom:3px;display:flex;align-items:center;gap:5px;
}
.vuln-text { font-size:0.8rem;color:#92400e;line-height:1.5; }

/* Bear case */
.bear-card {
    background: linear-gradient(135deg, #fff1f2 0%, #fff7ed 100%);
    border: 1.5px solid var(--red-bdr);
    border-radius: var(--r-md);
    padding: 14px 18px;
    box-shadow: var(--sh);
}
.bear-label {
    font-family:var(--mono);font-size:0.58rem;letter-spacing:0.14em;text-transform:uppercase;
    color:var(--red);margin-bottom:6px;display:flex;align-items:center;gap:6px;
}
.bear-text { font-size:0.875rem;color:#9f1239;line-height:1.6; }

/* Watch list */
.watch-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
}
.watch-item {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--r-sm);
    padding: 10px 13px;
    font-family: var(--mono);
    font-size: 0.75rem;
    color: var(--text2);
    line-height: 1.4;
    display: flex;
    align-items: flex-start;
    gap: 7px;
    box-shadow: var(--sh);
}
.watch-item::before {
    content: '◉';
    color: var(--accent);
    font-size: 0.6rem;
    flex-shrink: 0;
    margin-top: 2px;
}


.sev-badge {
    font-family: var(--mono);
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 99px;
}
.sev-critical { color:#be123c;background:#fff1f2;border:1px solid #fecdd3; }
.sev-high     { color:#c2410c;background:#fff7ed;border:1px solid #fed7aa; }
.sev-medium   { color:#b45309;background:#fffbeb;border:1px solid #fde68a; }

/* ── Streamlit overrides ── */
.stAlert {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--r-md) !important;
}
details, [data-testid="stExpander"] {
    border: 1.5px solid var(--border) !important;
    border-radius: var(--r-md) !important;
    background: var(--surface) !important;
    box-shadow: var(--sh) !important;
}
[data-testid="column"]:first-child { padding-right: 2rem !important; }
</style>
""", unsafe_allow_html=True)


# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="brand">
    <span class="brand-name">StepWise</span>
    <span class="brand-pill">AI Diagnostic</span>
</div>
<div class="brand-tagline">Pinpoints where reasoning breaks — not just whether it does.</div>
""", unsafe_allow_html=True)


# ─── Mode selector (rendered as styled HTML, wired via st.selectbox hidden) ──
use_mock = st.sidebar.toggle("Mock mode", value=False)

# ── Mode tabs ──
st.markdown("""
<style>
/* ── Mode tabs: segment control ── */
div[data-testid="stRadio"] > div {
    display: flex !important;
    flex-direction: row !important;
    gap: 0 !important;
    background: #ebebea !important;
    border: 1.5px solid #d8d5ce !important;
    border-radius: 12px !important;
    padding: 4px !important;
    width: fit-content !important;
    margin-bottom: 1.5rem !important;
}
div[data-testid="stRadio"] label {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-width: 96px !important;
    padding: 8px 20px !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: #9c9890 !important;
    white-space: nowrap !important;
    transition: all 0.15s ease !important;
    margin: 0 !important;
    line-height: 1.2 !important;
}
div[data-testid="stRadio"] label:has(input:checked) {
    background: #ffffff !important;
    color: #18181b !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.08) !important;
}
div[data-testid="stRadio"] label > div:first-child { display: none !important; }
div[data-testid="stRadio"] label p {
    font-size: 0.85rem !important;
    font-weight: inherit !important;
    color: inherit !important;
    margin: 0 !important;
    line-height: 1.2 !important;
}
div[data-testid="stRadio"] > label { display: none !important; }
</style>
""", unsafe_allow_html=True)

mode = st.radio("", ["Learning", "Code", "Markets"], horizontal=True, label_visibility="collapsed")


# ─── Helpers ─────────────────────────────────────────────────────────────────
def number_lines(text: str) -> str:
    return "\n".join(f"{i}. {line.rstrip()}" for i, line in enumerate(text.splitlines(), 1))


def call_claude(system_prompt: str, user_prompt: str) -> str:
    """Call the local Nemotron-3-Nano-30B via llama.cpp OpenAI-compatible endpoint."""
    payload = {
        "model": "nvidia--NVIDIA-Nemotron-3-Nano-30B-NVFP3",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        "temperature": 0.0,
        "max_tokens": 2048,
        "response_format": {"type": "json_object"},  # force JSON output
    }
    r = requests.post(LOCAL_MODEL_URL, json=payload, timeout=180)
    r.raise_for_status()
    data = r.json()
    content = data["choices"][0].get("message", {}).get("content", "")
    if not content.strip():
        raise ValueError(f"Empty response from model: {data}")
    return content


# ─── Learning: parse JSON response ───────────────────────────────────────────
def get_learning_result(problem: str, attempt: str):
    lines = attempt.strip().splitlines()
    numbered = "\n".join(f"{i+1}. {l}" for i, l in enumerate(lines))

    system = (
        "You are a precise math tutor. "
        "You MUST output ONLY a valid JSON object. No markdown. No <think> tags. Just raw JSON.\n\n"
        "Required JSON schema:\n"
        "{\n"
        '  "status": "Correct" or "Incorrect",\n'
        '  "confidence": "Low" or "Medium" or "High",\n'
        '  "overall_hint": "one sentence — encouraging if correct, pointing to main mistake if wrong",\n'
        '  "solution": "complete correct working, one step per line",\n'
        '  "errors": [\n'
        "    {\n"
        '      "line": <integer, 1-based>,\n'
        '      "wrong": "<exact student text>",\n'
        '      "corrected": "<correct version derived from the original problem>",\n'
        '      "why": "<why this is wrong>",\n'
        '      "fix": "<what to do>"\n'
        "    }\n"
        "  ]\n"
        "}\n\n"
        "VERIFICATION RULES — follow in order:\n"
        "1. Solve the problem yourself completely. Write out every step and the final answer.\n"
        "2. Substitute the student final answer back into the ORIGINAL PROBLEM and check it satisfies it.\n"
        "   If substitution fails, the final answer line is WRONG — add it to errors.\n"
        "3. Check every intermediate line arithmetically against your own working.\n"
        "4. Only set status Correct if substitution passes AND every line matches your working exactly.\n"
        "5. Never include a line in errors if it is genuinely correct.\n"
        "6. overall_hint must never be empty — if correct write a short praise; if wrong name the key mistake."
    )

    user = (
        f"ORIGINAL PROBLEM:\n{problem}\n\n"
        "STEP 1 — Solve it yourself:\n"
        "Work through every step and find the correct final answer.\n\n"
        "STEP 2 — Verify the student final answer by substitution:\n"
        "Take the student last line, plug those values back into the original problem equation, "
        "and check whether it holds true. If it does not, that line is wrong.\n\n"
        f"STEP 3 — Check every line:\n{numbered}\n\n"
        "For each line compare it to your own working. "
        "If the value or expression is different from what it should be, add it to errors.\n"
        "The corrected field must always come from YOUR working, never from the student attempt.\n\n"
        "Output JSON only."
    )

    raw = call_claude(system, user)

    # strip any accidental markdown fences or <think> blocks Nemotron may emit
    clean = re.sub(r"<think>[\s\S]*?</think>", "", raw, flags=re.IGNORECASE).strip()
    clean = re.sub(r"^```(?:json)?\s*", "", clean, flags=re.IGNORECASE)
    clean = re.sub(r"\s*```$", "", clean).strip()

    try:
        data = json.loads(clean)
    except json.JSONDecodeError:
        # try to extract first {...} block as last resort
        m = re.search(r"\{[\s\S]+\}", clean)
        try:
            data = json.loads(m.group()) if m else {}
        except Exception:
            data = {}

    if not data:
        data = {
            "status": "Parse error",
            "confidence": "Low",
            "overall_hint": "Model response could not be parsed — see raw output below.",
            "solution": "",
            "errors": [{"line": None, "wrong": "", "corrected": "",
                        "why": raw[:400], "fix": "Check raw output in the expander."}],
        }

    # Normalise solution — model sometimes returns a list instead of a string
    if "solution" in data:
        sol = data["solution"]
        if isinstance(sol, list):
            data["solution"] = "\n".join(str(s) for s in sol)
        elif isinstance(sol, str):
            # strip "Step N:" prefixes and list brackets if model wrapped it
            sol = sol.strip().lstrip("[").rstrip("]").strip("'\"")
            # if it looks like a Python list repr, parse it
            if sol.startswith("[") or ("', '" in sol) or ('", "' in sol):
                import ast as _ast
                try:
                    parsed = _ast.literal_eval(data["solution"])
                    if isinstance(parsed, list):
                        data["solution"] = "\n".join(str(s) for s in parsed)
                except Exception:
                    pass

    # Safety filter: remove any error the model flagged as actually correct
    if "errors" in data:
        def is_spurious(e):
            why = e.get("why", "").lower()
            wrong = e.get("wrong", "").strip()
            corrected = e.get("corrected", "").strip()
            # Drop if model says it's correct, or if wrong == corrected (no real change)
            return ("this line is correct" in why or
                    "line is correct" in why or
                    "is correct" in why or
                    (wrong and corrected and wrong == corrected))
        data["errors"] = [e for e in data["errors"] if not is_spurious(e)]
        data["error_count"] = len(data["errors"])
        if not data["errors"]:
            data["status"] = "Correct"
    data["_lines"] = lines
    return data, raw


# ─── Markets ─────────────────────────────────────────────────────────────────
def _parse_markets_raw(raw: str) -> dict:
    """Try multiple strategies to extract valid JSON from model output."""
    clean = re.sub(r"<think>[\s\S]*?</think>", "", raw, flags=re.IGNORECASE).strip()
    clean = re.sub(r"^```(?:json)?\s*", "", clean, flags=re.IGNORECASE)
    clean = re.sub(r"\s*```$", "", clean).strip()

    # Strategy 1: direct parse
    try:
        return json.loads(clean)
    except Exception:
        pass

    # Strategy 2: find outermost { ... }
    m = re.search(r"\{[\s\S]+\}", clean)
    if m:
        try:
            return json.loads(m.group())
        except Exception:
            pass

    # Strategy 3: fix common Nemotron issues — trailing commas, unquoted values
    fixed = re.sub(r",\s*([}\]])", r"", clean)  # trailing commas
    try:
        return json.loads(fixed)
    except Exception:
        pass

    return {}


def _normalise_markets(data: dict) -> dict:
    """Normalise flat or nested model output into our expected schema."""
    # causal_chain: accept list of strings OR list of dicts
    chain = data.get("causal_chain", [])
    norm_chain = []
    for item in chain:
        if isinstance(item, str):
            norm_chain.append({"step": item, "confidence": "Medium", "lag": ""})
        elif isinstance(item, dict):
            norm_chain.append({
                "step":       item.get("step", item.get("description", str(item))),
                "confidence": item.get("confidence", "Medium"),
                "lag":        item.get("lag", item.get("timing", "")),
            })
    data["causal_chain"] = norm_chain

    # asset_impacts: accept nested dict OR flat strings
    ai = data.get("asset_impacts", {})
    if not isinstance(ai, dict):
        ai = {}
    norm_ai = {}
    for asset in ["equities", "bonds", "currency", "commodities"]:
        val = ai.get(asset, data.get(asset, ""))
        if isinstance(val, str):
            # flat string like "Bearish — yields rise"
            direction = "Neutral"
            for d in ["Bullish", "Bearish", "Neutral"]:
                if d.lower() in val.lower():
                    direction = d
                    break
            norm_ai[asset] = {"direction": direction, "magnitude": "Medium", "reasoning": val or "—"}
        elif isinstance(val, dict):
            norm_ai[asset] = {
                "direction": val.get("direction", "Neutral"),
                "magnitude": val.get("magnitude", "Medium"),
                "reasoning": val.get("reasoning", val.get("reason", "—")),
            }
        else:
            norm_ai[asset] = {"direction": "Neutral", "magnitude": "Medium", "reasoning": "—"}
    data["asset_impacts"] = norm_ai

    # key_assumptions: accept list of strings OR list of dicts
    assumptions = data.get("key_assumptions", data.get("assumptions", []))
    norm_assumptions = []
    for a in assumptions:
        if isinstance(a, str):
            norm_assumptions.append({"assumption": a, "vulnerability": ""})
        elif isinstance(a, dict):
            norm_assumptions.append({
                "assumption":   a.get("assumption", a.get("text", str(a))),
                "vulnerability": a.get("vulnerability", a.get("risk", "")),
            })
    data["key_assumptions"] = norm_assumptions

    # indicators: accept list of strings or dicts
    indicators = data.get("indicators_to_watch", data.get("indicators", []))
    data["indicators_to_watch"] = [
        i if isinstance(i, str) else i.get("indicator", i.get("name", str(i)))
        for i in indicators
    ]

    # ensure required scalar fields exist
    data.setdefault("thesis",     data.get("summary", data.get("thesis", "No thesis returned.")))
    data.setdefault("regime",     data.get("macro_regime", "Unknown"))
    data.setdefault("confidence", "Medium")
    data.setdefault("bear_case",  data.get("downside_scenario", data.get("bear_case", "—")))

    return data


def get_markets_result(event_text: str):
    system = (
        "You are a senior macro investor at Bridgewater Associates. "
        "You MUST output ONLY valid JSON. No markdown. No <think> tags. No extra text.\n\n"
        "Output this exact JSON structure — keep all keys, use simple string values:\n"
        "{\n"
        '  "thesis": "single sentence: the key market implication",\n'
        '  "regime": "3-5 word macro regime label",\n'
        '  "confidence": "Low" or "Medium" or "High",\n'
        '  "causal_chain": [\n'
        '    {"step": "what happens", "confidence": "High", "lag": "0-1 months"},\n'
        '    {"step": "next effect", "confidence": "Medium", "lag": "1-3 months"},\n'
        '    {"step": "downstream impact", "confidence": "Medium", "lag": "3-6 months"}\n'
        "  ],\n"
        '  "asset_impacts": {\n'
        '    "equities":    {"direction": "Bearish", "magnitude": "High",   "reasoning": "why"},\n'
        '    "bonds":       {"direction": "Bearish", "magnitude": "Medium", "reasoning": "why"},\n'
        '    "currency":    {"direction": "Bullish", "magnitude": "Medium", "reasoning": "why"},\n'
        '    "commodities": {"direction": "Bearish", "magnitude": "Medium", "reasoning": "why"}\n'
        "  },\n"
        '  "key_assumptions": [\n'
        '    {"assumption": "what must be true", "vulnerability": "what breaks it"},\n'
        '    {"assumption": "second assumption",  "vulnerability": "what breaks it"}\n'
        "  ],\n"
        '  "bear_case": "one sentence: most credible scenario where thesis is wrong",\n'
        '  "indicators_to_watch": ["10y-2y Treasury spread", "ISM PMI", "Core PCE YoY"]\n'
        "}\n\n"
        "Replace the example values with your actual analysis. Output JSON only."
    )

    user = (
        f"Macro event: {event_text}\n\n"
        "Analyse this event as a Bridgewater macro investor. "
        "Fill every field with specific, substantive analysis. "
        "Output JSON only."
    )

    raw = call_claude(system, user)
    data = _parse_markets_raw(raw)

    if not data or not data.get("thesis") or data.get("thesis") == "single sentence: the key market implication":
        # model may have returned the template — try one more parse pass
        data = {}

    if not data:
        data = {
            "thesis": "Model returned unparseable output — check Raw model output below.",
            "regime": "Unknown", "confidence": "Low",
            "causal_chain": [], "asset_impacts": {
                "equities":    {"direction":"Neutral","magnitude":"Low","reasoning":"—"},
                "bonds":       {"direction":"Neutral","magnitude":"Low","reasoning":"—"},
                "currency":    {"direction":"Neutral","magnitude":"Low","reasoning":"—"},
                "commodities": {"direction":"Neutral","magnitude":"Low","reasoning":"—"},
            },
            "key_assumptions": [], "bear_case": "—", "indicators_to_watch": [],
        }
    else:
        data = _normalise_markets(data)

    return data, raw


# ─── Mock data ────────────────────────────────────────────────────────────────
def learning_mock_response(problem, attempt):
    lines = attempt.strip().splitlines()
    return {
        "status": "Incorrect",
        "confidence": "High",
        "overall_hint": "Distribute correctly before solving — multiply 2 by every term inside the brackets.",
        "solution": "2(x - 3) = 10\n2x - 6 = 10\n2x = 16\nx = 8",
        "errors": [
            {
                "line": 1,
                "wrong": lines[0] if lines else "2x - 3 = 10",
                "corrected": "2x - 6 = 10",
                "why": "2(x − 3) expands to 2x − 6, not 2x − 3. The −3 must also be multiplied by 2.",
                "fix": "Apply the distributive law: 2 × (−3) = −6.",
            },
            {
                "line": 2,
                "wrong": lines[1] if len(lines) > 1 else "2x = 13",
                "corrected": "2x = 16",
                "why": "This follows from the wrong line 1; 10 + 6 = 16, not 13.",
                "fix": "Once line 1 is corrected to 2x − 6 = 10, add 6 to both sides to get 2x = 16.",
            },
            {
                "line": 3,
                "wrong": lines[2] if len(lines) > 2 else "x = 6.5",
                "corrected": "x = 8",
                "why": "16 ÷ 2 = 8, not 6.5.",
                "fix": "Divide both sides of 2x = 16 by 2.",
            },
        ],
        "_lines": lines,
    }

def markets_mock_response(event_text):
    return {
        "thesis": "Fed tightening into slowing growth creates a stagflationary headwind — short duration, long dollar, underweight cyclicals.",
        "regime": "Late Cycle Tightening",
        "confidence": "Medium",
        "causal_chain": [
            {"step": "Fed raises rates → short-end yields reprice upward immediately", "confidence": "High", "lag": "0–1 weeks"},
            {"step": "Higher borrowing costs compress corporate margins and household spending power", "confidence": "High", "lag": "1–3 months"},
            {"step": "Forward earnings estimates revised down; equity risk premium rises", "confidence": "Medium", "lag": "2–4 months"},
            {"step": "Credit spreads widen as refinancing risk increases for leveraged borrowers", "confidence": "Medium", "lag": "3–6 months"},
            {"step": "Growth expectations fall → commodity demand weakens, curve inverts further", "confidence": "Medium", "lag": "6–12 months"},
        ],
        "asset_impacts": {
            "equities":    {"direction": "Bearish",  "magnitude": "High",   "reasoning": "Multiple compression from higher discount rate; growth names hit hardest via longer duration cash flows."},
            "bonds":       {"direction": "Bearish",  "magnitude": "Medium", "reasoning": "Short end sells off on rate path; long end anchored by growth fears — curve flattening or inversion likely."},
            "currency":    {"direction": "Bullish",  "magnitude": "Medium", "reasoning": "Rate differential widens vs trading partners on divergent policy; carry trade favors USD."},
            "commodities": {"direction": "Bearish",  "magnitude": "Medium", "reasoning": "Demand-sensitive commodities (copper, crude) weaken on growth slowdown; gold ambiguous."},
        },
        "key_assumptions": [
            {"assumption": "Inflation remains above target, forcing the Fed to stay hawkish", "vulnerability": "If CPI drops faster than expected, the Fed pivots — reversing the entire thesis."},
            {"assumption": "Labour market stays tight, preventing an immediate recession", "vulnerability": "A sharp unemployment rise would accelerate recession fears and trigger a bond rally."},
            {"assumption": "No exogenous supply shock re-ignites energy inflation", "vulnerability": "A geopolitical supply disruption would complicate the stagflationary dynamic unpredictably."},
        ],
        "bear_case": "Fed executes a soft landing — inflation falls without a growth shock, real rates stay manageable, and equity markets re-rate higher on a Goldilocks backdrop.",
        "indicators_to_watch": [
            "10y–2y Treasury spread (inversion depth and duration)",
            "ISM Manufacturing PMI — sub-50 signals contraction",
            "Core PCE YoY — Fed's preferred inflation gauge",
            "IG and HY credit spreads (Bloomberg Barclays)",
            "University of Michigan 5y inflation expectations",
            "Fed Funds futures implied terminal rate",
        ],
    }


def run_learning(problem, attempt):
    if use_mock:
        return learning_mock_response(problem, attempt), "Mock mode"
    return get_learning_result(problem, attempt)

def run_markets(event_text):
    if use_mock:
        return markets_mock_response(event_text), "Mock mode"
    return get_markets_result(event_text)



# ─── Code debugging ───────────────────────────────────────────────────────────
def get_code_result(code: str):
    lines = code.strip().splitlines()
    numbered = "\n".join(f"{i+1}. {l}" for i, l in enumerate(lines))

    system = (
        "You are a senior software engineer and expert debugger. "
        "You MUST output ONLY a valid JSON object. No markdown. No <think> tags. Just raw JSON.\n\n"
        "Auto-detect the programming language. Then deeply analyse the code for ALL bugs.\n\n"
        "Required JSON schema:\n"
        "{\n"
        '  "language": "Python" or "JavaScript" or "C++" or other,\n'
        '  "status": "Buggy" or "Clean",\n'
        '  "confidence": "Low" or "Medium" or "High",\n'
        '  "summary": "one sentence: what this code is trying to do",\n'
        '  "complexity": "Simple" or "Moderate" or "Complex",\n'
        '  "root_cause": "one sentence: the single deepest cause of failure if buggy",\n'
        '  "fixed_code": "complete corrected code as a string with \\n line breaks",\n'
        '  "errors": [\n'
        "    {\n"
        '      "line": <1-based integer>,\n'
        '      "wrong": "<exact buggy line>",\n'
        '      "corrected": "<fixed version>",\n'
        '      "type": "SyntaxError|NameError|TypeError|IndexError|LogicError|OffByOne|NullRef|InfiniteLoop|other",\n'
        '      "severity": "Critical" or "High" or "Medium",\n'
        '      "why": "<precise explanation of what goes wrong at runtime>",\n'
        '      "fix": "<exact actionable fix>",\n'
        '      "consequence": "<what happens if unfixed: crash / wrong output / security risk / etc>"\n'
        "    }\n"
        "  ]\n"
        "}\n\n"
        "RULES:\n"
        "1. Mentally execute the code line by line before reporting bugs.\n"
        "2. Flag ALL bugs: syntax, logic, runtime, off-by-one, undefined names, wrong operators, type errors, infinite loops.\n"
        "3. Do NOT flag style, naming conventions, or performance.\n"
        "4. Severity: Critical=crash or data corruption, High=wrong output, Medium=edge-case failure.\n"
        "5. fixed_code must be the complete working file.\n"
        "6. root_cause is the deepest systemic issue, not a list.\n"
        "7. Never include correct lines in errors."
    )

    user = (
        f"Code to debug (numbered lines):\n{numbered}\n\n"
        "Step 1: What language, what does this code do?\n"
        "Step 2: Execute it mentally line by line and find every bug.\n"
        "Step 3: For each bug — line, wrong text, corrected, type, severity, why, fix, consequence.\n"
        "Step 4: Write the complete fixed version in fixed_code.\n"
        "Output JSON only."
    )

    raw = call_claude(system, user)
    clean = re.sub(r"<think>[\s\S]*?</think>", "", raw, flags=re.IGNORECASE).strip()
    clean = re.sub(r"^```(?:json)?\s*", "", clean, flags=re.IGNORECASE)
    clean = re.sub(r"\s*```$", "", clean).strip()

    try:
        data = json.loads(clean)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]+\}", clean)
        try:
            data = json.loads(m.group()) if m else {}
        except Exception:
            data = {}

    if not data:
        data = {
            "language": "Unknown", "status": "Parse error", "confidence": "Low",
            "summary": "Could not parse model response.", "complexity": "Unknown",
            "root_cause": "—", "fixed_code": raw, "errors": [],
        }

    if "errors" in data:
        data["errors"] = [
            e for e in data["errors"]
            if "is correct" not in e.get("why", "").lower()
            and e.get("wrong","").strip() != e.get("corrected","").strip()
        ]
    data["_lines"] = lines
    return data, raw
def code_mock_response():
    lines = [
        "def find_max(lst):",
        "    max_val = lst[0]",
        "    for i in range(len(lst)):",
        "        if lst[i] > max_val:",
        "            max_val = lst[i]",
        "    return max_val",
        "",
        "numbers = [3, 1, 4, 1, 5, 9]",
        "print(find_max(numbers[1:]))",
    ]
    return {
        "language": "Python",
        "status": "Buggy",
        "confidence": "High",
        "summary": "Finds the maximum value in a list of numbers.",
        "complexity": "Simple",
        "root_cause": "The function is called with a sliced list, silently discarding the first element before the max search begins.",
        "fixed_code": "def find_max(lst):\n    max_val = lst[0]\n    for i in range(len(lst)):\n        if lst[i] > max_val:\n            max_val = lst[i]\n    return max_val\n\nnumbers = [3, 1, 4, 1, 5, 9]\nprint(find_max(numbers))",
        "errors": [
            {
                "line": 9,
                "wrong": "print(find_max(numbers[1:]))",
                "corrected": "print(find_max(numbers))",
                "type": "LogicError",
                "severity": "High",
                "why": "numbers[1:] slices off index 0 (value 3) before passing to find_max, so the function never considers the first element.",
                "fix": "Pass the full list — change numbers[1:] to numbers.",
                "consequence": "Returns wrong output: finds max of [1,4,1,5,9] instead of [3,1,4,1,5,9]. Silently incorrect — no crash, no error message.",
            }
        ],
        "_lines": lines,
    }


def run_code(code):
    if use_mock:
        return code_mock_response(), "Mock mode"
    return get_code_result(code)



# ─── Execution trace ──────────────────────────────────────────────────────────
def get_execution_trace(code: str, language: str):
    """Ask the model to simulate step-by-step execution and return variable states."""
    system = (
        "You are a code interpreter simulator. "
        "You MUST output ONLY a valid JSON object. No markdown. No <think> tags.\n\n"
        "Simulate executing the given code line by line. For each executed line, record the program state.\n\n"
        "Required JSON schema:\n"
        "{\n"
        '  "steps": [\n'
        "    {\n"
        '      "step": <1-based integer>,\n'
        '      "line": <line number in source>,\n'
        '      "code": "<the line of code being executed>",\n'
        '      "variables": {"var_name": "value_as_string", ...},\n'
        '      "output": "<any print/console output from this line, or empty string>",\n'
        '      "note": "<one short phrase explaining what this step does>",\n'
        '      "is_bug": true or false\n'
        "    }\n"
        "  ],\n"
        '  "final_output": "<the complete program output>",\n'
        '  "terminates": true or false,\n'
        '  "error": "<runtime error message if it crashes, else empty string>"\n'
        "}\n\n"
        "RULES:\n"
        "1. Only include lines that actually execute (skip blank lines, comments, pure definitions until called).\n"
        "2. Show variables AFTER the line executes — include all variables in scope.\n"
        "3. For loops: show each iteration as a separate step.\n"
        "4. Max 40 steps — if the code would run longer, stop and set terminates to false.\n"
        "5. Mark is_bug true on any step where the code does something incorrect.\n"
        "6. Values should be human-readable strings: lists as [1,2,3], dicts as {a:1}, etc."
    )
    user = (
        f"Language: {language}\n\nCode:\n{code}\n\n"
        "Simulate execution step by step. Show variable state after each line. Output JSON only."
    )
    raw = call_claude(system, user)
    clean = re.sub(r"<think>[\s\S]*?</think>", "", raw, flags=re.IGNORECASE).strip()
    clean = re.sub(r"^```(?:json)?\s*", "", clean, flags=re.IGNORECASE)
    clean = re.sub(r"\s*```$", "", clean).strip()
    try:
        return json.loads(clean), raw
    except Exception:
        m = re.search(r"\{[\s\S]+\}", clean)
        try:
            return json.loads(m.group()), raw
        except Exception:
            return {"steps":[],"final_output":"","terminates":True,"error":"Parse error"}, raw


def build_execution_widget(trace, code):
    import json as _j
    sj = _j.dumps(trace.get("steps", []))
    cl = _j.dumps(code.strip().splitlines())
    fo = _j.dumps(trace.get("final_output", ""))
    em = _j.dumps(trace.get("error", ""))

    # Build HTML as a list then join — avoids any f-string / escape issues
    parts = []
    parts.append("<!DOCTYPE html><html><head><meta charset='utf-8'><style>")
    parts.append("*{box-sizing:border-box;margin:0;padding:0}")
    parts.append("body{background:#1e1e2e;font-family:'JetBrains Mono','Fira Code',monospace;color:#cdd6f4}")
    parts.append("#shell{border:1.5px solid #313244;border-radius:14px;overflow:hidden}")
    parts.append(".tb{display:flex;align-items:center;gap:10px;padding:10px 16px;background:#181825;border-bottom:1px solid #313244}")
    parts.append(".dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:4px}")
    parts.append(".tl{font-size:.62rem;letter-spacing:.12em;text-transform:uppercase;color:#6c7086}")
    parts.append("#ctr{margin-left:auto;font-size:.68rem;color:#6c7086}")
    parts.append(".panels{display:grid;grid-template-columns:1fr 1fr;min-height:240px}")
    parts.append(".ph{padding:7px 12px;background:#11111b;border-bottom:1px solid #313244;font-size:.58rem;letter-spacing:.12em;text-transform:uppercase;color:#6c7086}")
    parts.append("#cp{border-right:1px solid #313244;overflow-y:auto}")
    parts.append("#cl{padding:4px 0}")
    parts.append(".cr{display:flex;align-items:stretch}")
    parts.append(".cn{min-width:34px;text-align:right;padding:3px 8px 3px 0;font-size:.64rem;color:#45475a;user-select:none;flex-shrink:0}")
    parts.append(".ct{padding:3px 12px 3px 0;font-size:.77rem;white-space:pre;flex:1}")
    parts.append("#vp{overflow-y:auto;display:flex;flex-direction:column}")
    parts.append("#vars{padding:10px 14px;flex:1;min-height:80px}")
    parts.append(".vr{display:flex;align-items:baseline;gap:8px;padding:4px 0;border-bottom:1px solid #313244}")
    parts.append(".vk{font-size:.72rem;color:#89b4fa;min-width:88px;flex-shrink:0}")
    parts.append(".vv{font-size:.74rem;color:#cdd6f4;word-break:break-all}")
    parts.append("#ow{border-top:1px solid #313244;padding:10px 14px;display:none}")
    parts.append(".ol{font-size:.55rem;letter-spacing:.12em;text-transform:uppercase;color:#6c7086;margin-bottom:5px}")
    parts.append("#ot{font-size:.77rem;color:#a6e3a1;line-height:1.6;white-space:pre-wrap}")
    parts.append("#nb{padding:9px 16px;background:#181825;border-top:1px solid #313244;min-height:34px;font-size:.75rem;line-height:1.4}")
    parts.append(".ctrl{display:flex;align-items:center;gap:8px;padding:10px 16px;background:#11111b;border-top:1px solid #313244}")
    parts.append(".btn{padding:6px 13px;border-radius:6px;border:1px solid #45475a;background:#1e1e2e;color:#cdd6f4;font-family:inherit;font-size:.7rem;cursor:pointer}")
    parts.append(".btn:hover{background:#313244}")
    parts.append("#bn{border:none;background:#a6e3a1;color:#1e1e2e;font-weight:700}")
    parts.append("#bn:hover{background:#bef8b0}")
    parts.append("#sw{margin-left:auto;display:flex;align-items:center;gap:6px;font-size:.62rem;color:#6c7086}")
    parts.append("input[type=range]{width:74px;accent-color:#a6e3a1}")
    parts.append(".empty{font-size:.72rem;color:#45475a}")
    parts.append("</style></head><body>")
    parts.append("<div id='shell'>")
    parts.append("<div class='tb'>")
    parts.append("<span><span class='dot' style='background:#f38ba8'></span><span class='dot' style='background:#f9e2af'></span><span class='dot' style='background:#a6e3a1'></span></span>")
    parts.append("<span class='tl'>Step Execution Visualizer</span>")
    parts.append("<span id='ctr'>Step 0 / 0</span></div>")
    parts.append("<div class='panels'>")
    parts.append("<div id='cp'><div class='ph'>Source</div><div id='cl'></div></div>")
    parts.append("<div id='vp'><div class='ph'>Variables</div><div id='vars'><span class='empty'>No variables yet</span></div>")
    parts.append("<div id='ow'><div class='ol'>Output</div><div id='ot'></div></div></div>")
    parts.append("</div>")
    parts.append("<div id='nb'>Click Next &#8594; to step through the code</div>")
    parts.append("<div class='ctrl'>")
    parts.append("<button class='btn' id='br'>&#9198; Reset</button>")
    parts.append("<button class='btn' id='bprev'>&#8592; Prev</button>")
    parts.append("<button class='btn' id='bn'>Next &#8594;</button>")
    parts.append("<button class='btn' id='bpl'>&#9654; Play</button>")
    parts.append("<div id='sw'>Speed <input type='range' id='spd' min='150' max='1400' value='650' step='50'></div>")
    parts.append("</div></div>")

    # JavaScript — written as a plain string, no f-string substitution needed
    js = """
<script>
(function() {
  var S = """ + sj + """;
  var C = """ + cl + """;
  var FO = """ + fo + """;
  var EM = """ + em + """;
  var cur = -1, playing = false, timer = null;

  function esc(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  function render(i) {
    cur = Math.max(-1, Math.min(S.length - 1, i));
    var step = cur >= 0 ? S[cur] : null;

    document.getElementById('ctr').textContent =
      'Step ' + (cur < 0 ? 0 : cur + 1) + ' / ' + S.length;

    var seen = [];
    if (cur >= 0) { for (var x = 0; x <= cur; x++) seen.push(S[x].line); }

    var h = '';
    for (var j = 0; j < C.length; j++) {
      var ln = j + 1;
      var isA = step && step.line === ln;
      var isB = isA && step.is_bug;
      var wasS = seen.indexOf(ln) >= 0 && !isA;
      var bg  = isB ? 'rgba(243,139,168,0.15)' : isA ? 'rgba(166,227,161,0.12)' : 'transparent';
      var clr = isB ? '#f38ba8' : isA ? '#a6e3a1' : wasS ? '#7f849c' : '#6c7086';
      var bl  = isB ? '3px solid #f38ba8' : isA ? '3px solid #a6e3a1' : '3px solid transparent';
      h += '<div class="cr" style="border-left:' + bl + ';background:' + bg + '">'
        +  '<span class="cn">' + ln + '</span>'
        +  '<span class="ct" style="color:' + clr + '">' + esc(C[j] || ' ') + '</span>'
        +  '</div>';
    }
    document.getElementById('cl').innerHTML = h;

    var ve = document.getElementById('vars');
    if (!step || !step.variables || !Object.keys(step.variables).length) {
      ve.innerHTML = '<span class="empty">No variables yet</span>';
    } else {
      var vh = '';
      for (var k in step.variables) {
        vh += '<div class="vr"><span class="vk">' + esc(k) + '</span>'
            + '<span class="vv">= ' + esc(step.variables[k]) + '</span></div>';
      }
      ve.innerHTML = vh;
    }

    var outs = '';
    if (cur >= 0) { for (var x = 0; x <= cur; x++) { if (S[x].output) outs += S[x].output + '\\n'; } }
    var ow = document.getElementById('ow');
    if (outs.trim() || (cur === S.length - 1 && FO)) {
      ow.style.display = 'block';
      document.getElementById('ot').textContent = outs.trim() || FO;
    } else {
      ow.style.display = 'none';
    }

    var nb = document.getElementById('nb');
    if (step) {
      nb.innerHTML = step.is_bug
        ? '<span style="color:#f38ba8">&#9888; BUG: </span>' + esc(step.note)
        : '<span style="color:#6c7086">&rarr; </span>' + esc(step.note);
    } else if (EM) {
      nb.innerHTML = '<span style="color:#f38ba8">&#10007; ' + esc(EM) + '</span>';
    } else {
      nb.textContent = 'Click Next \u2192 to step through the code';
    }
  }

  function stopPlay() {
    playing = false;
    clearTimeout(timer);
    timer = null;
    document.getElementById('bpl').textContent = '\u25B6 Play';
  }

  document.getElementById('br').addEventListener('click', function() { stopPlay(); render(-1); });
  document.getElementById('bprev').addEventListener('click', function() { stopPlay(); render(cur - 1); });
  document.getElementById('bn').addEventListener('click', function() { stopPlay(); render(cur + 1); });
  document.getElementById('bpl').addEventListener('click', function() {
    if (playing) { stopPlay(); return; }
    if (cur >= S.length - 1) render(-1);
    playing = true;
    document.getElementById('bpl').textContent = '\u23F8 Pause';
    function tick() {
      if (!playing || cur >= S.length - 1) { stopPlay(); return; }
      render(cur + 1);
      timer = setTimeout(tick, parseInt(document.getElementById('spd').value, 10));
    }
    timer = setTimeout(tick, parseInt(document.getElementById('spd').value, 10));
  });

  render(-1);
})();
</script></body></html>"""

    parts.append(js)
    return "".join(parts)

def render_learning(result, raw, attempt):
    status     = result.get("status", "Unknown")
    confidence = result.get("confidence", "Medium")
    errors     = result.get("errors", [])
    hint       = result.get("overall_hint", "")
    solution   = result.get("solution", "")
    orig_lines = result.get("_lines", attempt.strip().splitlines())

    is_correct = status.lower() in ("correct", "no errors")
    conf_cls   = {"Low": "conf-chip-low", "Medium": "conf-chip-med", "High": "conf-chip-high"}.get(confidence, "conf-chip-med")

    # ── Score banner ──
    if is_correct:
        icon_cls, icon, label_cls = "verdict-icon-ok", "✓", "verdict-label-ok"
    else:
        icon_cls, icon, label_cls = "verdict-icon-err", "✗", "verdict-label-err"

    st.markdown(f"""
    <div class="score-banner">
        <div class="score-verdict">
            <div class="verdict-icon {icon_cls}">{icon}</div>
            <span class="verdict-label {label_cls}">{status}</span>
        </div>
        <div class="score-chips">
            <div class="score-chip">
                <span class="chip-label">Errors</span>
                <span class="chip-val">{len(errors)}</span>
            </div>
            <div class="score-chip {conf_cls}">
                <span class="chip-label">Confidence</span>
                <span class="chip-val-conf">{confidence}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Line diff ──
    error_by_line = {e["line"]: e for e in errors if e.get("line") is not None}
    st.markdown('<div class="sec-head">Line-by-line diagnosis</div>', unsafe_allow_html=True)

    rows_html = ""
    for i, line_text in enumerate(orig_lines, 1):
        err = error_by_line.get(i)
        if err:
            corrected = err.get("corrected", "")
            rows_html += f"""<div class="diff-row">
                <div class="diff-gutter diff-gutter-wrong">{i}</div>
                <div class="diff-content diff-body-wrong">
                    <div class="diff-badge-wrong">✗ wrong</div>
                    <div class="diff-line-wrong">{line_text}</div>
                    <div class="diff-arrow">↳</div>
                    <div class="diff-line-fix"><span class="diff-fix-badge">corrected</span>{corrected}</div>
                </div>
            </div>"""
        else:
            rows_html += f"""<div class="diff-row">
                <div class="diff-gutter diff-gutter-ok">{i}</div>
                <div class="diff-content diff-body-ok">
                    <div class="diff-line-ok">{line_text}</div>
                </div>
            </div>"""

    st.markdown(f'<div class="diff-wrap">{rows_html}</div>', unsafe_allow_html=True)

    # ── Error cards ──
    if errors:
        st.markdown('<div class="sec-head">Error details</div>', unsafe_allow_html=True)
        for err in errors:
            line_no  = err.get("line")
            line_tag = f"Line {line_no}" if line_no is not None else "General"
            st.markdown(f"""
            <div class="err-card">
                <div class="err-card-head">
                    <span class="err-card-line-badge">{line_tag}</span>
                </div>
                <div class="err-card-body">
                    <div class="err-row-label">Why it's wrong</div>
                    <div class="err-why-text">{err.get("why","")}</div>
                    <div class="err-row-label">How to fix it</div>
                    <div class="err-fix-text">{err.get("fix","")}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── Hint ──
    st.markdown('<div class="sec-head">Overall hint</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="hint-card">
        <div class="hint-card-label">◈ Insight</div>
        <div class="hint-card-text">{hint}</div>
    </div>""", unsafe_allow_html=True)

    # ── Solution ──
    st.markdown('<div class="sec-head">Correct solution</div>', unsafe_allow_html=True)
    sol_lines = [l for l in solution.splitlines() if l.strip()]
    sol_rows = "".join(
        f'<div style="display:flex;align-items:baseline;gap:12px;padding:9px 0;border-bottom:1px solid #d1fae5">' +
        f'<span style="font-family:var(--mono);font-size:0.6rem;font-weight:700;color:#6ee7b7;min-width:20px;flex-shrink:0">{i+1}</span>' +
        f'<span style="font-family:var(--mono);font-size:0.84rem;color:#065f46;font-weight:500">{ln}</span>' +
        '</div>'
        for i, ln in enumerate(sol_lines)
    )
    st.markdown(f'''<div style="background:#ecfdf5;border:1.5px solid #a7f3d0;border-radius:12px;padding:16px 20px;box-shadow:0 1px 3px rgba(0,0,0,0.05)">
        <div style="font-family:var(--mono);font-size:0.58rem;letter-spacing:0.14em;text-transform:uppercase;color:#059669;margin-bottom:10px">✓ Step-by-step</div>
        {sol_rows}
    </div>''', unsafe_allow_html=True)

    with st.expander("Raw model output"):
        st.code(raw, language="text")


def render_code(result, raw):
    status     = result.get("status", "Unknown")
    confidence = result.get("confidence", "Medium")
    errors     = result.get("errors", [])
    language   = result.get("language", "Code")
    summary    = result.get("summary", "")
    complexity = result.get("complexity", "")
    root_cause = result.get("root_cause", "")
    fixed_code = result.get("fixed_code", "")
    orig_lines = result.get("_lines", [])

    is_clean = status.lower() in ("clean", "no bugs")
    conf_cls = {"Low":"conf-chip-low","Medium":"conf-chip-med","High":"conf-chip-high"}.get(confidence,"conf-chip-med")

    sev_counts = {}
    for e in errors:
        s = e.get("severity","Medium")
        sev_counts[s] = sev_counts.get(s,0) + 1

    sev_html = ""
    for sev, cls in [("Critical","sev-critical"),("High","sev-high"),("Medium","sev-medium")]:
        if sev_counts.get(sev,0):
            sev_html += f'<span class="sev-badge {cls}">{sev_counts[sev]} {sev}</span>'

    # ── Banner ──
    icon_cls = "verdict-icon-ok" if is_clean else "verdict-icon-err"
    icon     = "✓" if is_clean else "✗"
    lbl_cls  = "verdict-label-ok" if is_clean else "verdict-label-err"
    verdict  = "No bugs found" if is_clean else f"{len(errors)} bug{'s' if len(errors)!=1 else ''} found"

    st.markdown(f"""
    <div class="score-banner">
        <div class="score-verdict" style="flex-wrap:wrap;gap:10px">
            <div class="verdict-icon {icon_cls}">{icon}</div>
            <span class="verdict-label {lbl_cls}">{verdict}</span>
            <span class="lang-badge">{language}</span>
            {sev_html}
        </div>
        <div class="score-chips">
            <div class="score-chip"><span class="chip-label">Bugs</span><span class="chip-val">{len(errors)}</span></div>
            <div class="score-chip"><span class="chip-label">Complexity</span><span class="chip-val" style="font-size:0.75rem">{complexity}</span></div>
            <div class="score-chip {conf_cls}"><span class="chip-label">Confidence</span><span class="chip-val-conf">{confidence}</span></div>
        </div>
    </div>""", unsafe_allow_html=True)

    if summary:
        st.markdown(f'<div style="font-size:0.84rem;color:var(--text2);margin:0.25rem 0 0.5rem;line-height:1.5">{summary}</div>', unsafe_allow_html=True)

    # ── Root cause ──
    if root_cause and not is_clean:
        st.markdown(f"""
        <div style="background:#fff7ed;border:1.5px solid #fed7aa;border-left:4px solid #f97316;border-radius:10px;padding:12px 16px;margin:0.75rem 0">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;letter-spacing:0.12em;text-transform:uppercase;color:#ea580c;margin-bottom:4px">⚡ Root cause</div>
            <div style="font-size:0.85rem;color:#9a3412;line-height:1.55;font-weight:500">{root_cause}</div>
        </div>""", unsafe_allow_html=True)

    # ── Code diff ──
    error_by_line = {e["line"]: e for e in errors if e.get("line") is not None}
    st.markdown('<div class="sec-head">Line-by-line diagnosis</div>', unsafe_allow_html=True)

    rows_html = ""
    for i, line_text in enumerate(orig_lines, 1):
        err = error_by_line.get(i)
        safe_line = line_text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        if err:
            safe_fix  = err.get("corrected","").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
            err_type  = err.get("type","Bug")
            severity  = err.get("severity","High")
            sev_color = {"Critical":"#f38ba8","High":"#fab387","Medium":"#f9e2af"}.get(severity,"#fab387")
            rows_html += f"""<div class="code-diff-row">
                <div class="code-gutter code-gutter-wrong">{i}</div>
                <div class="code-content code-wrong-bg">
                    <div style="display:flex;gap:6px;margin-bottom:4px">
                        <span class="code-badge-wrong">✗ {err_type}</span>
                        <span style="font-family:var(--mono);font-size:0.58rem;font-weight:700;letter-spacing:0.08em;padding:1px 7px;border-radius:99px;background:rgba(0,0,0,0.15);color:{sev_color};border:1px solid {sev_color}40">{severity}</span>
                    </div>
                    <div class="code-line-wrong">{safe_line}</div>
                    <div class="code-arrow">↳</div>
                    <div class="code-line-fix"><span class="code-fix-badge">fixed</span>{safe_fix}</div>
                </div>
            </div>"""
        else:
            rows_html += f"""<div class="code-diff-row">
                <div class="code-gutter">{i}</div>
                <div class="code-content code-ok"><div class="code-line-ok">{safe_line if safe_line.strip() else "&nbsp;"}</div></div>
            </div>"""

    st.markdown(f'<div class="code-diff-wrap">{rows_html}</div>', unsafe_allow_html=True)

    # ── Bug detail cards ──
    if errors:
        st.markdown('<div class="sec-head">Bug details</div>', unsafe_allow_html=True)
        for err in errors:
            line_no    = err.get("line")
            line_tag   = f"Line {line_no}" if line_no else "General"
            err_type   = err.get("type", "Bug")
            severity   = err.get("severity","High")
            consequence= err.get("consequence","")
            sev_bg     = {"Critical":"#fff1f2","High":"#fff7ed","Medium":"#fffbeb"}.get(severity,"#fff7ed")
            sev_bdr    = {"Critical":"#fecdd3","High":"#fed7aa","Medium":"#fde68a"}.get(severity,"#fed7aa")
            sev_col    = {"Critical":"#be123c","High":"#c2410c","Medium":"#b45309"}.get(severity,"#c2410c")
            st.markdown(f"""
            <div class="code-err-card" style="border-color:{sev_bdr}">
                <div class="code-err-head" style="background:{sev_bg};border-bottom-color:{sev_bdr}">
                    <span class="err-card-line-badge">{line_tag}</span>
                    <span style="font-family:var(--mono);font-size:0.62rem;font-weight:600;color:{sev_col};background:#fff;border:1px solid {sev_bdr};padding:3px 10px;border-radius:99px">{err_type}</span>
                    <span style="font-family:var(--mono);font-size:0.62rem;font-weight:700;color:{sev_col};background:{sev_bg};border:1px solid {sev_bdr};padding:3px 10px;border-radius:99px;margin-left:auto">{severity}</span>
                </div>
                <div class="err-card-body">
                    <div class="err-row-label">Why it fails</div>
                    <div class="err-why-text">{err.get("why","")}</div>
                    <div class="err-row-label">How to fix it</div>
                    <div class="err-fix-text">{err.get("fix","")}</div>
                    {f'<div class="err-row-label" style="color:#d97706">Consequence if unfixed</div><div style="font-size:0.84rem;color:#92400e;line-height:1.55">{consequence}</div>' if consequence else ""}
                </div>
            </div>""", unsafe_allow_html=True)

    # ── Fixed code ──
    st.markdown('<div class="sec-head">Fixed code</div>', unsafe_allow_html=True)
    safe_fixed = fixed_code.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    st.markdown(f"""
    <div class="fixed-sol-block">
        <span class="fixed-sol-label">✓ Complete corrected file</span>
        <div class="fixed-sol-body">{safe_fixed}</div>
    </div>""", unsafe_allow_html=True)

    # ── Execution visualizer ──
    if st.session_state.get("exec_trace_" + str(hash(result.get("fixed_code","")))):
        trace = st.session_state["exec_trace_" + str(hash(result.get("fixed_code","")))]
        st.markdown('<div class="sec-head">Step-by-step execution</div>', unsafe_allow_html=True)
        widget_html = build_execution_widget(trace, result.get("fixed_code",""))
        st.components.v1.html(widget_html, height=520, scrolling=False)

    with st.expander("Raw model output"):
        st.code(raw, language="text")

def render_markets(result, raw):
    confidence  = result.get("confidence", "Medium")
    thesis      = result.get("thesis", "")
    regime      = result.get("regime", "")
    chain       = result.get("causal_chain", [])
    assets      = result.get("asset_impacts", {})
    assumptions = result.get("key_assumptions", [])
    bear_case   = result.get("bear_case", "")
    indicators  = result.get("indicators_to_watch", [])

    tcp_cls = {"Low":"tcp-low","Medium":"tcp-med","High":"tcp-high"}.get(confidence,"tcp-med")

    # ── Thesis card (hero) ──
    st.markdown(f"""
    <div class="thesis-card">
        <div class="thesis-overline">◈ Investment Thesis</div>
        <div class="thesis-text">"{thesis}"</div>
        <div class="thesis-meta">
            <span class="regime-pill">⬡ {regime}</span>
            <span class="thesis-conf-pill {tcp_cls}">{confidence} Confidence</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── Causal chain ──
    st.markdown('<div class="sec-head">Causal mechanism</div>', unsafe_allow_html=True)
    rows = ""
    for item in chain:
        step = item.get("step","") if isinstance(item, dict) else str(item)
        conf = item.get("confidence","Medium") if isinstance(item, dict) else "Medium"
        lag  = item.get("lag","") if isinstance(item, dict) else ""
        cc   = {"Low":"ct-conf-low","Medium":"ct-conf-med","High":"ct-conf-high"}.get(conf,"ct-conf-med")
        lag_html = f'<span class="ct-badge ct-lag">⏱ {lag}</span>' if lag else ""
        rows += f'''<div class="ct-row">
            <div class="ct-step">{step}</div>
            <div class="ct-badges">
                <span class="ct-badge {cc}">{conf}</span>
                {lag_html}
            </div>
        </div>'''
    st.markdown(f'<div class="chain-timeline">{rows}</div>', unsafe_allow_html=True)

    # ── Asset impacts ──
    st.markdown('<div class="sec-head">Asset class impacts</div>', unsafe_allow_html=True)
    cells = ""
    dir_icons = {"Bullish":"▲","Bearish":"▼","Neutral":"→"}
    dir_cls   = {"Bullish":"dir-bull","Bearish":"dir-bear","Neutral":"dir-neut"}
    for name in ["equities","bonds","currency","commodities"]:
        a = assets.get(name, {})
        d = a.get("direction","Neutral")
        m = a.get("magnitude","Low")
        r = a.get("reasoning","")
        ic  = dir_icons.get(d,"→")
        cls = dir_cls.get(d,"dir-neut")
        cells += f'''<div class="asset-cell">
            <div class="asset-label">{name.title()}</div>
            <div>
                <span class="asset-direction {cls}">{ic} {d}</span>
                <span class="asset-mag">{m}</span>
            </div>
            <div class="asset-reasoning">{r}</div>
        </div>'''
    st.markdown(f'<div class="asset-grid">{cells}</div>', unsafe_allow_html=True)

    # ── Key assumptions + vulnerabilities ──
    st.markdown('<div class="sec-head">Key assumptions & stress tests</div>', unsafe_allow_html=True)
    for a in assumptions:
        assumption = a.get("assumption","") if isinstance(a,dict) else str(a)
        vuln       = a.get("vulnerability","") if isinstance(a,dict) else ""
        vuln_html  = f'''<div class="vuln-label">⚡ Vulnerability</div>
            <div class="vuln-text">{vuln}</div>''' if vuln else ""
        st.markdown(f'''<div class="assumption-card">
            <div class="assumption-text">{assumption}</div>
            {vuln_html}
        </div>''', unsafe_allow_html=True)

    # ── Bear case ──
    st.markdown('<div class="sec-head">Bear case / thesis invalidator</div>', unsafe_allow_html=True)
    st.markdown(f'''<div class="bear-card">
        <div class="bear-label">⚠ What breaks this thesis</div>
        <div class="bear-text">{bear_case}</div>
    </div>''', unsafe_allow_html=True)

    # ── Indicators to watch ──
    if indicators:
        st.markdown('<div class="sec-head">Indicators to watch</div>', unsafe_allow_html=True)
        items = "".join(f'<div class="watch-item">{ind}</div>' for ind in indicators)
        st.markdown(f'<div class="watch-grid">{items}</div>', unsafe_allow_html=True)

    with st.expander("Raw model output"):
        st.code(raw, language="text")


# ─── Main layout ──────────────────────────────────────────────────────────────
if mode == "Code":
    col1, col2 = st.columns([420/1320, 1 - 420/1320], gap="large")

    with col1:
        st.markdown('<div class="field-label"><span class="field-label-dot"></span>Paste your code</div>', unsafe_allow_html=True)
        code_input = st.text_area(
            "", value='def add(a, b):\n    return a - b  # bug: should be +\n\nresult = add(3, 4)\nprint("Sum:", results)  # bug: undefined variable',
            height=280, label_visibility="collapsed", key="code_input"
        )
        run       = st.button("Debug Code →", use_container_width=True)
        trace_run = st.button("⚡ Trace Execution", use_container_width=True)

        if trace_run and "last_code_result" in st.session_state:
            res = st.session_state["last_code_result"]
            lang = res.get("language","Python")
            code_to_trace = res.get("fixed_code","") or st.session_state.get("last_code_input","")
            with st.spinner("Tracing execution…"):
                if use_mock:
                    # build a simple mock trace
                    trace = {"steps":[
                        {"step":1,"line":1,"code":"def find_max(lst):","variables":{},"output":"","note":"Define function find_max","is_bug":False},
                        {"step":2,"line":8,"code":"numbers = [3, 1, 4, 1, 5, 9]","variables":{"numbers":"[3,1,4,1,5,9]"},"output":"","note":"Assign list to numbers","is_bug":False},
                        {"step":3,"line":9,"code":"print(find_max(numbers))","variables":{"numbers":"[3,1,4,1,5,9]"},"output":"","note":"Call find_max with full list","is_bug":False},
                        {"step":4,"line":2,"code":"    max_val = lst[0]","variables":{"lst":"[3,1,4,1,5,9]","max_val":"3"},"output":"","note":"Initialise max_val to first element","is_bug":False},
                        {"step":5,"line":3,"code":"    for i in range(len(lst)):","variables":{"lst":"[3,1,4,1,5,9]","max_val":"3","i":"0"},"output":"","note":"Start loop i=0","is_bug":False},
                        {"step":6,"line":4,"code":"        if lst[0] > max_val:","variables":{"lst":"[3,1,4,1,5,9]","max_val":"3","i":"0"},"output":"","note":"3 > 3 is False","is_bug":False},
                        {"step":7,"line":3,"code":"    for i in range(len(lst)):","variables":{"lst":"[3,1,4,1,5,9]","max_val":"3","i":"1"},"output":"","note":"Loop i=1","is_bug":False},
                        {"step":8,"line":4,"code":"        if lst[1] > max_val:","variables":{"lst":"[3,1,4,1,5,9]","max_val":"3","i":"1"},"output":"","note":"1 > 3 is False","is_bug":False},
                        {"step":9,"line":3,"code":"    for i in range(len(lst)):","variables":{"lst":"[3,1,4,1,5,9]","max_val":"3","i":"2"},"output":"","note":"Loop i=2","is_bug":False},
                        {"step":10,"line":4,"code":"        if lst[2] > max_val:","variables":{"lst":"[3,1,4,1,5,9]","max_val":"3","i":"2"},"output":"","note":"4 > 3 is True — update max","is_bug":False},
                        {"step":11,"line":5,"code":"            max_val = lst[2]","variables":{"lst":"[3,1,4,1,5,9]","max_val":"4","i":"2"},"output":"","note":"max_val updated to 4","is_bug":False},
                        {"step":12,"line":6,"code":"    return max_val","variables":{"lst":"[3,1,4,1,5,9]","max_val":"9","i":"5"},"output":"","note":"Return 9","is_bug":False},
                        {"step":13,"line":9,"code":"print(find_max(numbers))","variables":{"numbers":"[3,1,4,1,5,9]","max_val":"9"},"output":"9","note":"Prints 9","is_bug":False},
                    ], "final_output":"9", "terminates":True, "error":""}
                else:
                    trace, _ = get_execution_trace(code_to_trace, lang)
            key = "exec_trace_" + str(hash(res.get("fixed_code","")))
            st.session_state[key] = trace
            st.rerun()

    with col2:
        if run:
            with st.spinner("Debugging with Nemotron…"):
                result, raw = run_code(code_input)
            st.session_state["last_code_result"] = result
            st.session_state["last_code_raw"]    = raw
            st.session_state["last_code_input"]  = code_input
            render_code(result, raw)
        elif "last_code_result" in st.session_state:
            result = st.session_state["last_code_result"]
            raw    = st.session_state["last_code_raw"]
            render_code(result, raw)
        else:
            st.markdown("""
            <div class="await-shell">
                <div class="await-ring" style="font-family:var(--mono);font-size:1rem">&lt;/&gt;</div>
                <div class="await-title">Ready to debug</div>
                <div class="await-sub">Paste your buggy code on the left<br>and click Debug Code.</div>
            </div>""", unsafe_allow_html=True)

elif mode == "Learning":
    col1, col2 = st.columns([420/1320, 1 - 420/1320], gap="large")

    with col1:
        st.markdown('<div class="field-label"><span class="field-label-dot"></span>Problem</div>', unsafe_allow_html=True)
        problem = st.text_area(
            "", value="Solve 2(x - 3) = 10",
            height=100, label_visibility="collapsed", key="problem"
        )
        st.markdown('<div class="field-label" style="margin-top:1.25rem"><span class="field-label-dot"></span>Student attempt</div>', unsafe_allow_html=True)
        attempt = st.text_area(
            "", value="2x - 3 = 10\n2x = 13\nx = 6.5",
            height=140, label_visibility="collapsed", key="attempt"
        )
        run = st.button("Run Diagnostic →", use_container_width=True)

    with col2:
        if run:
            with st.spinner("Analysing with Nemotron…"):
                result, raw = run_learning(problem, attempt)
            render_learning(result, raw, attempt)
        else:
            st.markdown("""
            <div class="await-shell">
                <div class="await-ring">◎</div>
                <div class="await-title">Ready to diagnose</div>
                <div class="await-sub">Enter a problem and student attempt<br>on the left, then run the diagnostic.</div>
            </div>""", unsafe_allow_html=True)

else:  # Markets
    col1, col2 = st.columns([420/1320, 1 - 420/1320], gap="large")

    with col1:
        st.markdown('''<div style="background:linear-gradient(135deg,#0f172a,#1e1b4b);border:1px solid #312e81;border-radius:10px;padding:14px 16px;margin-bottom:1.25rem">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;letter-spacing:0.14em;text-transform:uppercase;color:#818cf8;margin-bottom:6px">◈ Bridgewater-Style Analysis</div>
            <div style="font-size:0.78rem;color:#c7d2fe;line-height:1.55">Build a full investment thesis: causal chain, asset impacts, assumptions, stress tests, and the bear case.</div>
        </div>''', unsafe_allow_html=True)
        st.markdown('<div class="field-label"><span class="field-label-dot"></span>Macro event or hypothesis</div>', unsafe_allow_html=True)
        event_text = st.text_area(
            "", value="The Federal Reserve signals it will keep interest rates higher for longer as inflation remains sticky above 3%.",
            height=160, label_visibility="collapsed", key="event"
        )
        run = st.button("Build Thesis →", use_container_width=True)

    with col2:
        if run:
            with st.spinner("Building thesis with Nemotron…"):
                result, raw = run_markets(event_text)
            render_markets(result, raw)
        else:
            st.markdown("""
            <div class="await-shell">
                <div class="await-ring" style="border-color:#312e81;color:#818cf8;background:linear-gradient(135deg,#0f172a,#1e1b4b)">◈</div>
                <div class="await-title">Build an investment thesis</div>
                <div class="await-sub">Describe a macro event on the left.<br>Get a full causal chain, asset impacts,<br>assumptions, and bear case.</div>
            </div>""", unsafe_allow_html=True)

st.markdown(
    f'<div class="app-footer">' +
    f'<span>StepWise AI</span><span class="footer-dot">·</span>' +
    f'<span>{"Mock mode" if use_mock else "Nemotron-3-Nano-30B · DGX"}</span><span class="footer-dot">·</span>' +
    f'<span>{"Learning" if mode == "Learning" else "Markets"}</span></div>',
    unsafe_allow_html=True
)