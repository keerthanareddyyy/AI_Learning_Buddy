import os
import warnings
import streamlit as st

# Suppress the deprecation FutureWarning from the installed google.generativeai package
with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning)
    import google.generativeai as genai

from dotenv import load_dotenv

# Load local environment variables if present
load_dotenv()

def init_session_state():
    """
    Initializes all necessary session state variables for the application.
    """
    if "api_key_gemini" not in st.session_state:
        st.session_state.api_key_gemini = os.environ.get("GEMINI_API_KEY", "")

    if "current_topic" not in st.session_state:
        st.session_state.current_topic = "What is Machine Learning?"
    if "learning_progress" not in st.session_state:
        st.session_state.learning_progress = {}  # {topic_name: bool}
    if "quiz_scores" not in st.session_state:
        st.session_state.quiz_scores = {}  # {topic_name: score_out_of_5}
    if "quiz_attempts" not in st.session_state:
        st.session_state.quiz_attempts = {}  # {topic_name: [{date: str, score: int}]}
    if "reflection_logs" not in st.session_state:
        st.session_state.reflection_logs = []  # [{date, topic, confidence, summary}]

    # Active learning session states
    if "explanation_content" not in st.session_state:
        st.session_state.explanation_content = None
    if "example_content" not in st.session_state:
        st.session_state.example_content = None
    if "active_quiz" not in st.session_state:
        st.session_state.active_quiz = None
    if "quiz_user_answers" not in st.session_state:
        st.session_state.quiz_user_answers = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "quiz_feedback" not in st.session_state:
        st.session_state.quiz_feedback = {}

    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hi there! I'm ML Mentor, your AI learning buddy. Let's explore the exciting world of Machine Learning together! What would you like to learn first?"}
        ]

def inject_custom_css():
    """
    Injects custom CSS to style the Streamlit app with a modern, responsive,
    and premium blue/white color theme.
    """
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        
        <style>
            /* =============================================
               GLOBAL TYPOGRAPHY
            ============================================= */
            html, body, [class*="css"] {
                font-family: 'Inter', sans-serif;
            }

            h1, h2, h3, h4, h5, h6 {
                font-family: 'Outfit', sans-serif;
                font-weight: 700;
                color: #1e3a8a;
                margin-top: 1rem;
            }

            /* =============================================
               HERO HEADER — dark bg, white text
            ============================================= */
            .main-header {
                background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
                color: #ffffff !important;
                padding: 2.5rem 2rem;
                border-radius: 16px;
                margin-bottom: 2rem;
                box-shadow: 0 4px 20px rgba(59, 130, 246, 0.15);
                text-align: center;
            }
            .main-header h1,
            .main-header h2,
            .main-header h3,
            .main-header p,
            .main-header span,
            .main-header * {
                color: #ffffff !important;
            }

            /* =============================================
               WHITE CONTENT CARDS — always dark text
            ============================================= */
            .content-card {
                background-color: #ffffff !important;
                color: #1f2937 !important;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                padding: 1.5rem;
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
                margin-bottom: 1.5rem;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            .content-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05), 0 4px 6px -2px rgba(0,0,0,0.05);
                border-color: #bfdbfe;
            }
            /* Force ALL children of a content card to be dark */
            .content-card * {
                color: #1f2937 !important;
            }
            /* Allow accent strong/headings inside cards to use their own colors */
            .content-card strong { font-weight: 700; }

            /* =============================================
               OUTPUT TEXT CONTAINER — generic output divs
            ============================================= */
            .output-container {
                background: #ffffff !important;
                color: #1f2937 !important;
                padding: 18px;
                border-radius: 10px;
                line-height: 1.8;
                font-size: 16px;
            }
            .output-container * { color: #1f2937 !important; }

            /* =============================================
               CUSTOM SIDEBAR
            ============================================= */
            .sidebar .sidebar-content {
                background-color: #f8fafc;
            }

            /* =============================================
               PROGRESS BADGE
            ============================================= */
            .progress-badge {
                display: inline-block;
                background-color: #d1fae5;
                color: #065f46 !important;
                padding: 0.25rem 0.75rem;
                border-radius: 9999px;
                font-size: 0.75rem;
                font-weight: 600;
                margin-bottom: 10px;
            }

            /* =============================================
               PROMPT TEMPLATE BOX
            ============================================= */
            .prompt-template-box {
                background-color: #f8fafc;
                border: 1px dashed #cbd5e1;
                border-radius: 8px;
                padding: 1rem;
                font-family: monospace;
                font-size: 0.875rem;
                color: #334155 !important;
                margin-bottom: 1rem;
            }

            /* =============================================
               CHAT BUBBLES — explicit colors both sides
            ============================================= */
            .chat-bubble {
                padding: 1rem;
                border-radius: 12px;
                margin-bottom: 1rem;
                max-width: 85%;
                line-height: 1.5;
            }
            /* Student bubble — light blue tint, dark text */
            .chat-user {
                background-color: #eff6ff !important;
                border: 1px solid #bfdbfe;
                color: #1e3a8a !important;
                margin-left: auto;
                border-bottom-right-radius: 2px;
            }
            .chat-user * { color: #1e3a8a !important; }
            /* ML Mentor bubble — light grey tint, dark text */
            .chat-agent {
                background-color: #f1f5f9 !important;
                border: 1px solid #e2e8f0;
                color: #1f2937 !important;
                margin-right: auto;
                border-bottom-left-radius: 2px;
            }
            .chat-agent * { color: #1f2937 !important; }

            /* =============================================
               BUTTONS
            ============================================= */
            div.stButton > button {
                background-color: #3b82f6 !important;
                color: white !important;
                border-radius: 8px !important;
                border: none !important;
                padding: 0.5rem 1.5rem !important;
                font-weight: 600 !important;
                transition: background-color 0.2s ease, transform 0.1s ease !important;
            }
            div.stButton > button:hover {
                background-color: #1d4ed8 !important;
                transform: translateY(-1px);
            }
            div.stButton > button:active {
                transform: translateY(1px);
            }

            /* =============================================
               METRIC BOXES
            ============================================= */
            .metric-box {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 1rem;
                text-align: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }
            .metric-val {
                font-size: 1.8rem;
                font-weight: 800;
                color: #2563eb !important;
            }
            .metric-lbl {
                font-size: 0.85rem;
                color: #64748b !important;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.6) -> str:
    """
    Calls Google Gemini API with an automatic model fallback chain.

    Model priority order:
        1. gemini-2.5-flash
        2. gemini-2.0-flash
        3. gemini-1.5-flash
        4. gemini-1.5-pro

    Each model is attempted up to 2 times (1 retry) before moving to the next.
    Returns the first successful non-empty response text.
    Returns "" (triggering caller's offline fallback) only if:
        - no API key is configured, OR
        - all four models fail after retries.
    All failures are reported transparently via st.error() / st.warning().
    """
    api_key = st.session_state.get("api_key_gemini", "").strip()
    if not api_key:
        return ""   # No key — caller uses offline fallback silently

    MODELS = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
    ]
    MAX_RETRIES = 2   # attempts per model (1 initial + 1 retry)

    genai.configure(api_key=api_key)
    last_error = None

    for model_name in MODELS:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system_prompt
                )
                response = model.generate_content(
                    user_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature
                    )
                )
                # response.text raises ValueError if blocked by safety filters
                text = response.text
                if text:
                    return text
                # Empty but not blocked — treat as soft failure, try next model
                last_error = f"{model_name}: empty response (possible safety filter)"
                break   # No point retrying the same model for an empty response

            except ValueError as e:
                # Safety filter block — no point retrying
                last_error = f"{model_name}: blocked by safety filter — {str(e)}"
                break

            except Exception as e:
                last_error = f"{model_name} (attempt {attempt}): {str(e)}"
                # Retry once for transient errors; if second attempt also fails, move on
                if attempt == MAX_RETRIES:
                    break
                # else: loop continues to next attempt

    # All models exhausted
    st.error(
        f"Gemini API: All models failed. Last error — {last_error}. "
        "Showing offline content instead."
    )
    return ""

def test_gemini_connection(api_key: str) -> tuple[bool, str]:
    """
    Tests connection to the Gemini API with the given API key.
    Returns (True, message) if successful, (False, error_message) otherwise.
    """
    if not api_key.strip():
        return False, "API Key is empty."
    try:
        genai.configure(api_key=api_key.strip())
        # List all available models to diagnose compatibility
        models = [m.name for m in genai.list_models()]
        return True, f"Connection successful! Supported models on this key: {models}"
    except Exception as e:
        return False, str(e)


def render_footer():
    """
    Renders a professional, subtle footer at the bottom of the page.
    """
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #64748b; font-size: 13px; margin-top: 2.5rem; margin-bottom: 1rem; line-height: 1.6;">
            <strong style="color: #1e3a8a;">ML Mentor</strong><br>
            AI Learning Buddy<br>
            <span style="font-size: 12px; font-weight: 500;">Infosys Springboard AI EMPOW(H)ER Week 8 Capstone</span><br>
            <span style="font-size: 11px; color: #94a3b8;">Developed using Python &bull; Streamlit &bull; Google Gemini API</span><br>
            <span style="font-size: 11px; color: #cbd5e1; display: block; margin-top: 6px; font-weight: 600;">Version 1.0 &bull; Week 8 Capstone</span>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_responsible_ai_disclaimer():
    """
    Renders a professional Responsible AI disclaimer box.
    """
    st.markdown(
        """
        <div style="background-color: #f8fafc; border-left: 4px solid #94a3b8; padding: 12px; border-radius: 6px; margin: 1.5rem 0; font-size: 13px; color: #475569; line-height: 1.5;">
            <strong>Responsible AI Disclaimer:</strong> This AI Learning Buddy is designed for educational purposes only.
            AI-generated responses may occasionally contain inaccuracies.
            Always verify important information using trusted learning resources.
        </div>
        """,
        unsafe_allow_html=True
    )
