import streamlit as st
from groq import Groq
import time

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Prompt Architect Pro",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS  –  Dark editorial aesthetic
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root tokens ── */
:root {
    --bg:        #0a0a0f;
    --surface:   #111118;
    --border:    #1e1e2e;
    --accent:    #7c3aed;
    --accent2:   #a78bfa;
    --glow:      rgba(124,58,237,0.25);
    --text:      #e2e8f0;
    --muted:     #64748b;
    --success:   #10b981;
    --warn:      #f59e0b;
    --mono:      'Space Mono', monospace;
    --sans:      'DM Sans', sans-serif;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: var(--sans);
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.main .block-container {
    padding: 2rem 2rem 4rem;
    max-width: 780px;
}

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.hero-badge {
    display: inline-block;
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent2);
    border: 1px solid var(--accent);
    padding: 0.2rem 0.75rem;
    border-radius: 2px;
    margin-bottom: 1rem;
    box-shadow: 0 0 12px var(--glow);
}
.hero h1 {
    font-family: var(--mono) !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #fff 0%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.5rem !important;
    padding: 0 !important;
}
.hero p {
    font-size: 0.9rem;
    color: var(--muted);
    margin: 0;
}

/* ── Card wrapper ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), transparent);
}
.card-label {
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent2);
    margin-bottom: 0.75rem;
}

/* ── Textarea ── */
.stTextArea textarea {
    background: #0d0d14 !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
    font-size: 0.92rem !important;
    line-height: 1.6 !important;
    resize: vertical !important;
    transition: border-color 0.2s;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--glow) !important;
}

/* ── Primary button ── */
.stButton > button[kind="primary"],
.stButton > button {
    width: 100% !important;
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.65rem 1.5rem !important;
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.08em !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 20px var(--glow) !important;
}
.stButton > button:hover {
    background: #6d28d9 !important;
    box-shadow: 0 6px 28px rgba(124,58,237,0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── Selectbox & slider ── */
.stSelectbox > div > div {
    background: #0d0d14 !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
}
.stSlider > div { padding: 0 !important; }

/* ── Code block (output) ── */
.stCodeBlock {
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    background: #0d0d14 !important;
}
.stCodeBlock code {
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
    line-height: 1.7 !important;
    color: var(--accent2) !important;
}

/* ── Metrics row ── */
.metric-row {
    display: flex;
    gap: 0.75rem;
    margin-bottom: 1.25rem;
}
.metric-box {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.9rem 1rem;
    text-align: center;
}
.metric-value {
    font-family: var(--mono);
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--accent2);
}
.metric-label {
    font-size: 0.7rem;
    color: var(--muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 0.2rem;
}

/* ── History item ── */
.hist-item {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 4px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.6rem;
    font-size: 0.82rem;
    color: var(--muted);
    cursor: pointer;
    transition: border-color 0.2s;
}
.hist-item:hover { border-left-color: var(--accent2); color: var(--text); }
.hist-item strong { color: var(--text); display: block; font-size: 0.85rem; margin-bottom: 0.2rem; }

/* ── Status badges ── */
.badge-success {
    display: inline-block;
    background: rgba(16,185,129,0.12);
    color: var(--success);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 3px;
    padding: 0.15rem 0.6rem;
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 0.1em;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stTextInput label {
    color: var(--muted) !important;
    font-family: var(--mono) !important;
    font-size: 0.7rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Token counter pill ── */
.token-pill {
    display: inline-block;
    background: rgba(124,58,237,0.1);
    border: 1px solid var(--accent);
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--accent2);
}

/* ── Spinner override ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── Info / warning boxes ── */
.stAlert {
    border-radius: 6px !important;
    border: 1px solid var(--border) !important;
    background: var(--surface) !important;
}

/* ── Copy hint ── */
.copy-hint {
    font-family: var(--mono);
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 0.1em;
    text-align: right;
    margin-top: -0.5rem;
    margin-bottom: 0.5rem;
}

/* ── Hide Streamlit branding ── */
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []          # list of {input, output, model, style, tokens}
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0
if "total_prompts" not in st.session_state:
    st.session_state.total_prompts = 0


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
VALID_MODELS = {
    "llama-3.3-70b-versatile":  "Best logic & structure",
    "llama3-70b-8192":          "Fast & reliable",
    "llama3-8b-8192":           "Ultra-fast / lightweight",
    "gemma2-9b-it":             "Google Gemma 2 – balanced",
    "mixtral-8x7b-32768":       "Long context (32k)",
}

with st.sidebar:
    st.markdown('<p style="font-family:\'Space Mono\',monospace;font-size:0.65rem;letter-spacing:0.2em;color:#7c3aed;text-transform:uppercase;margin-bottom:1rem;">⚙ Configuration</p>', unsafe_allow_html=True)

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get yours at console.groq.com",
    )

    model_choice = st.selectbox(
        "Model",
        options=list(VALID_MODELS.keys()),
        format_func=lambda m: f"{m}  —  {VALID_MODELS[m]}",
    )

    st.markdown("---")

    prompt_style = st.selectbox(
        "Prompt Style",
        ["🎯 Analytical",  "🎨 Creative", "⚙️ Technical", "📊 Structured Report", "🗣️ Conversational"],
        help="Controls the meta-instructions sent to the model.",
    )

    temperature = st.slider(
        "Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.05,
        help="Higher = more creative. Lower = more deterministic.",
    )

    max_input_chars = st.slider(
        "Max Input Length (chars)", min_value=200, max_value=3000, value=1500, step=100,
    )

    st.markdown("---")

    # Stats
    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace;font-size:0.65rem;color:#64748b;line-height:2;">
    PROMPTS GENERATED &nbsp;&nbsp;<span style="color:#a78bfa">{st.session_state.total_prompts}</span><br>
    TOKENS USED &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#a78bfa">{st.session_state.total_tokens:,}</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑 Clear History"):
        st.session_state.history = []
        st.session_state.total_tokens = 0
        st.session_state.total_prompts = 0
        st.rerun()


# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">v2.0  ·  Groq Powered</div>
    <h1>Prompt Architect</h1>
    <p>Transform raw ideas into precision-engineered AI prompts.</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  INPUT CARD
# ─────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-label">// Input</div>', unsafe_allow_html=True)

user_vibe = st.text_area(
    label="Raw Idea",
    height=140,
    placeholder="Describe what you want the AI to do — in English, Darija, or any language…",
    label_visibility="collapsed",
)

char_count = len(user_vibe)
col_count, col_limit = st.columns([3, 1])
with col_count:
    color = "#10b981" if char_count <= max_input_chars else "#ef4444"
    st.markdown(
        f'<span class="token-pill" style="border-color:{color};color:{color};">'
        f'{char_count} / {max_input_chars} chars</span>',
        unsafe_allow_html=True,
    )

st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  STYLE → SYSTEM PROMPT MAPPING
# ─────────────────────────────────────────────
STYLE_INSTRUCTIONS = {
    "🎯 Analytical": """
        Output a rigorous analytical prompt using the RTF framework:
        Role · Task · Format. Be precise, logical, and unambiguous.
        Use numbered steps for the Task section.
        Add explicit Constraints and a clear Output Format block.
    """,
    "🎨 Creative": """
        Output an imaginative, open-ended prompt that gives the AI creative freedom.
        Use evocative language in the Role. Allow flexible output formats.
        Encourage exploration and unexpected angles.
    """,
    "⚙️ Technical": """
        Output a prompt optimized for technical/coding tasks.
        Include a Tech Stack section, exact input/output specs,
        edge-case handling instructions, and code style guidelines.
    """,
    "📊 Structured Report": """
        Output a prompt that instructs the AI to produce a structured report.
        Specify section headings, data tables where relevant, executive summary,
        and a recommendations block at the end.
    """,
    "🗣️ Conversational": """
        Output a warm, natural-language prompt suitable for chatbot personas.
        Focus on tone calibration, empathy cues, and concise reply guidelines.
    """,
}

SYSTEM_BASE = """
You are an elite Prompt Engineer. Your ONLY task is to take a raw user idea and
transform it into a single, highly optimized prompt for large language models.

Instructions:
{style_instructions}

Rules:
- Output ONLY the final engineered prompt — no preamble, no commentary, no markdown wrapper.
- If the input is in Darija or Arabic, extract the intent and write the prompt in English.
- Estimate ~{char_limit} chars as the output cap; be thorough but not padded.
"""


# ─────────────────────────────────────────────
#  GENERATE BUTTON
# ─────────────────────────────────────────────
generate = st.button("⚡ Generate Prompt", use_container_width=True)

if generate:
    # Validation
    if not api_key:
        st.error("🔑 Enter your Groq API key in the sidebar.")
    elif not user_vibe.strip():
        st.warning("✏️ Write something in the input box first.")
    elif char_count > max_input_chars:
        st.error(f"⚠️ Input too long ({char_count} chars). Reduce to {max_input_chars} or raise the limit.")
    else:
        try:
            client = Groq(api_key=api_key)

            style_key = prompt_style
            system_prompt = SYSTEM_BASE.format(
                style_instructions=STYLE_INSTRUCTIONS[style_key].strip(),
                char_limit=1200,
            )

            t_start = time.time()
            with st.spinner("Architecting your prompt…"):
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user",   "content": user_vibe.strip()},
                    ],
                    model=model_choice,
                    temperature=temperature,
                    max_tokens=1024,
                )
            elapsed = round(time.time() - t_start, 2)

            final_prompt   = response.choices[0].message.content.strip()
            usage          = response.usage
            tokens_used    = usage.total_tokens if usage else 0

            # Update session stats
            st.session_state.total_tokens += tokens_used
            st.session_state.total_prompts += 1

            # Save to history
            st.session_state.history.insert(0, {
                "input":  user_vibe.strip()[:80] + ("…" if len(user_vibe) > 80 else ""),
                "output": final_prompt,
                "model":  model_choice,
                "style":  style_key,
                "tokens": tokens_used,
                "time":   elapsed,
            })

            # ── Output card ──
            st.markdown("---")
            st.markdown("""
            <div class="card">
                <div class="card-label">// Engineered Prompt &nbsp;<span class="badge-success">READY</span></div>
            """, unsafe_allow_html=True)

            st.markdown('<p class="copy-hint">↑ click the copy icon in the top-right corner</p>', unsafe_allow_html=True)
            st.code(final_prompt, language="text")
            st.markdown('</div>', unsafe_allow_html=True)

            # ── Metrics row ──
            prompt_words = len(final_prompt.split())
            st.markdown(f"""
            <div class="metric-row">
                <div class="metric-box">
                    <div class="metric-value">{tokens_used}</div>
                    <div class="metric-label">Tokens Used</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">{elapsed}s</div>
                    <div class="metric-label">Gen Time</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">{prompt_words}</div>
                    <div class="metric-label">Output Words</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">{st.session_state.total_prompts}</div>
                    <div class="metric-label">Total Prompts</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            err = str(e)
            if "api_key" in err.lower() or "auth" in err.lower():
                st.error("🔑 Invalid API key. Double-check in the sidebar.")
            elif "model" in err.lower():
                st.error(f"🤖 Model error: {err}")
            else:
                st.error(f"⚠️ Error: {err}")


# ─────────────────────────────────────────────
#  HISTORY PANEL
# ─────────────────────────────────────────────
if st.session_state.history:
    st.markdown("---")
    st.markdown('<p class="card-label" style="font-family:\'Space Mono\',monospace;font-size:0.65rem;letter-spacing:0.18em;text-transform:uppercase;color:#7c3aed;">// Recent History</p>', unsafe_allow_html=True)

    for i, item in enumerate(st.session_state.history[:5]):
        with st.expander(f"#{st.session_state.total_prompts - i}  ·  {item['style']}  ·  {item['tokens']} tokens  ·  {item['time']}s"):
            st.markdown(f"**Input:** {item['input']}")
            st.markdown(f"**Model:** `{item['model']}`")
            st.code(item["output"], language="text")


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:3rem;padding-top:1.5rem;border-top:1px solid #1e1e2e;">
    <span style="font-family:'Space Mono',monospace;font-size:0.65rem;color:#334155;letter-spacing:0.15em;">
    PROMPT ARCHITECT PRO  ·  GROQ + LLAMA  ·  BUILT FOR SPEED
    </span>
</div>
""", unsafe_allow_html=True)
