import streamlit as st
from utils import init_session_state, inject_custom_css, call_llm, render_footer, render_responsible_ai_disclaimer, test_gemini_connection
from persona import render_persona_sidebar, AI_PERSONA, get_system_instruction, render_persona_page
from prompts import ML_TOPICS, get_explanation_prompt, get_example_prompt, render_prompt_templates_page
from quiz import render_quiz_section
from conversation import render_conversation_page, render_sample_conversation_page
from reflection import render_reflection_report_page, render_reflection_diary_page, render_progress_analytics_page

# ------------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------------
st.set_page_config(
    page_title="ML Mentor - Machine Learning Fundamentals",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_session_state()
inject_custom_css()

# ------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------
st.sidebar.markdown(f"# 🤖 {AI_PERSONA['name']}")
st.sidebar.markdown("*AI Learning Buddy*")
st.sidebar.markdown("---")

# Core page navigation
core_pages = [
    "🏠 Home",
    "📚 Learning Hub",
    "🤖 AI Buddy Persona",
    "📋 Prompt Templates",
    "💬 Sample Conversation",
    "❓ Quiz",
    "📝 Reflection Report",
]

advanced_pages = [
    "🗨️ Chat Room",
    "⚙️ API Configuration",
    "📓 Reflection Diary",
    "📊 Progress Analytics",
]

if "active_page" not in st.session_state:
    st.session_state.active_page = "🏠 Home"

def on_core_nav_change():
    if "core_nav_radio" in st.session_state:
        st.session_state.active_page = st.session_state.core_nav_radio

# Sidebar radio for core pages
core_default = core_pages.index(st.session_state.active_page) if st.session_state.active_page in core_pages else 0
selected_core = st.sidebar.radio(
    "Navigation",
    options=core_pages,
    index=core_default,
    key="core_nav_radio",
    on_change=on_core_nav_change
)

# Advanced features expander
with st.sidebar.expander("🛠️ Advanced Features", expanded=st.session_state.active_page in advanced_pages):
    for adv_name in advanced_pages:
        label = f"▶ {adv_name}" if st.session_state.active_page == adv_name else adv_name
        if st.button(label, key=f"adv_{adv_name}", use_container_width=True):
            st.session_state.active_page = adv_name
            st.rerun()

# Tutor tone & persona sidebar card
tutor_tone = render_persona_sidebar()

# Syllabus progress bar
total_topics = len(ML_TOPICS)
completed_topics = sum(1 for val in st.session_state.learning_progress.values() if val)
completion_pct = int((completed_topics / total_topics) * 100)
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Syllabus Coverage")
st.sidebar.progress(completion_pct / 100.0)
st.sidebar.caption(f"{completed_topics} / {total_topics} topics completed ({completion_pct}%)")

# Sidebar version label
st.sidebar.markdown("---")
# Live API key status indicator
if st.session_state.get("api_key_gemini", "").strip():
    st.sidebar.markdown(
        "<div style='text-align:center; font-size:11px; color:#22c55e; font-weight:600;'>🟢 Gemini API: Active</div>",
        unsafe_allow_html=True
    )
st.sidebar.markdown(
    "<div style='text-align:center; font-size:11px; color:#94a3b8;'>Version 1.0 &bull; Week 8 Capstone</div>",
    unsafe_allow_html=True
)

# ------------------------------------------------------------------
# LEARN TOPICS LIST for "What You'll Learn"
LEARN_CARDS = [
    ("ML Basics", "What Machine Learning is and how it differs from traditional programming."),
    ("Supervised Learning", "Learning from labeled data to make accurate predictions."),
    ("Unsupervised Learning", "Discovering hidden patterns in data without labels."),
    ("Reinforcement Learning", "Learning through rewards and penalties via trial and error."),
    ("Decision Trees", "Tree-structured models that make decisions using yes/no splits."),
    ("Random Forest", "An ensemble of Decision Trees for higher accuracy."),
    ("KNN", "K-Nearest Neighbors — classifying by similarity to known examples."),
    ("K-Means", "Grouping data into K clusters based on feature similarity."),
    ("Neural Networks", "Brain-inspired models powering deep learning systems."),
    ("Model Evaluation", "Metrics and methods to measure how well a model performs."),
]

# ------------------------------------------------------------------
# PAGE ROUTER
# ------------------------------------------------------------------

# ── HOME ──────────────────────────────────────────────────────────
if st.session_state.active_page == "🏠 Home":
    st.markdown(
        f"""
        <div class="main-header">
            <h1>🤖 {AI_PERSONA['name']}</h1>
            <p>AI Learning Buddy for Machine Learning Fundamentals</p>
            <p style="font-size:0.9rem; opacity:0.8;">Infosys Springboard AI EMPOW(H)ER &bull; Week 8 Capstone</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Short description
    st.markdown(
        f"**{AI_PERSONA['name']}** is an interactive AI tutor that teaches **Machine Learning Fundamentals** "
        "to beginners using simple language, real-life analogies, and guided quizzes. "
        "Study at your own pace and track your progress as you go."
    )

    col_meta1, col_meta2 = st.columns(2)
    col_meta1.markdown(f"**AI Buddy Name:** {AI_PERSONA['name']}")
    col_meta2.markdown("**Topic:** Machine Learning Fundamentals")

    # Responsible AI disclaimer
    render_responsible_ai_disclaimer()

    # Start Learning button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Start Learning", key="btn_home_start", use_container_width=False):
        st.session_state.active_page = "📚 Learning Hub"
        st.rerun()

    # "What You'll Learn" section
    st.markdown("---")
    st.markdown("### What You'll Learn")
    st.markdown("This course covers the following core Machine Learning topics:")

    rows = [LEARN_CARDS[i:i+2] for i in range(0, len(LEARN_CARDS), 2)]
    for row in rows:
        cols = st.columns(2)
        for col, (title, desc) in zip(cols, row):
            col.markdown(
                f"""
                <div class="content-card" style="border-top: 3px solid #3b82f6; padding: 1rem; background:#ffffff; color:#1f2937;">
                    <strong style="color:#1e3a8a; font-size:15px;">{title}</strong>
                    <p style="font-size:13px; color:#475569; margin:6px 0 0 0; line-height:1.5;">{desc}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    render_footer()

# ── LEARNING HUB ──────────────────────────────────────────────────
elif st.session_state.active_page == "📚 Learning Hub":
    st.markdown("## Machine Learning Learning Hub")
    st.markdown("Choose a topic below and generate an AI-powered explanation or a real-life example.")

    selected_topic = st.selectbox(
        "Select a Topic to Study:",
        options=list(ML_TOPICS.keys()),
        index=list(ML_TOPICS.keys()).index(st.session_state.current_topic)
    )
    if selected_topic != st.session_state.current_topic:
        st.session_state.current_topic = selected_topic
        st.session_state.explanation_content = None
        st.session_state.example_content = None
        st.session_state.active_quiz = None
        st.session_state.quiz_submitted = False
        st.rerun()

    tab_explain, tab_example = st.tabs(["Explanation", "Real-life Example"])
    api_key_set = bool(st.session_state.get("api_key_gemini", "").strip())

    with tab_explain:
        st.markdown(f"### Understanding: {selected_topic}")

        col_btn, col_status = st.columns([1, 3])
        with col_btn:
            trigger_exp = st.button("Generate Explanation", key="btn_explain")
        with col_status:
            if api_key_set:
                st.caption(f"Tone: {tutor_tone} · Powered by Google Gemini")
            else:
                st.caption("Offline mode — showing handcrafted lesson content.")

        if trigger_exp or st.session_state.explanation_content is None:
            if api_key_set and trigger_exp:
                with st.spinner("Generating explanation..."):
                    system_prompt = get_system_instruction(f"Explain in a {tutor_tone} tone.")
                    user_prompt = get_explanation_prompt(selected_topic, tutor_tone)
                    explanation = call_llm(system_prompt, user_prompt)
                    st.session_state.explanation_content = (
                        explanation if explanation
                        else ML_TOPICS[selected_topic]["fallback_explanation"]
                    )
            else:
                st.session_state.explanation_content = ML_TOPICS[selected_topic]["fallback_explanation"]

        st.markdown(
            f"""
            <div class="content-card" style="border-left: 5px solid #2563eb; line-height: 1.7; background:#ffffff; color:#1f2937;">
                {st.session_state.explanation_content}
            </div>
            """,
            unsafe_allow_html=True
        )

    with tab_example:
        st.markdown(f"### Real-life Analogy: {selected_topic}")

        col_btn, col_status = st.columns([1, 3])
        with col_btn:
            trigger_ex = st.button("Generate Example", key="btn_example")
        with col_status:
            if api_key_set:
                st.caption(f"Tone: {tutor_tone} · Powered by Google Gemini")
            else:
                st.caption("Offline mode — showing handcrafted lesson content.")

        if trigger_ex or st.session_state.example_content is None:
            if api_key_set and trigger_ex:
                with st.spinner("Preparing real-life example..."):
                    system_prompt = get_system_instruction(
                        f"Use a highly visual and relatable {tutor_tone} comparison."
                    )
                    user_prompt = get_example_prompt(selected_topic, tutor_tone)
                    example = call_llm(system_prompt, user_prompt)
                    st.session_state.example_content = (
                        example if example
                        else ML_TOPICS[selected_topic]["fallback_example"]
                    )
            else:
                st.session_state.example_content = ML_TOPICS[selected_topic]["fallback_example"]

        st.markdown(
            f"""
            <div class="content-card" style="border-left: 5px solid #eab308; line-height: 1.7; background:#ffffff; color:#1f2937;">
                {st.session_state.example_content}
            </div>
            """,
            unsafe_allow_html=True
        )

    # 🎓 Topic Completion Tracker at the bottom of Learning Hub
    st.markdown("---")
    st.markdown("### 🎓 Study Progress Tracker")
    is_completed = st.checkbox(
        "Mark this topic as 'Completed' & save to my student progress",
        value=st.session_state.learning_progress.get(selected_topic, False),
        key=f"complete_checkbox_{selected_topic}"
    )
    if is_completed != st.session_state.learning_progress.get(selected_topic, False):
        st.session_state.learning_progress[selected_topic] = is_completed
        st.rerun()

    render_footer()

# ── AI BUDDY PERSONA ───────────────────────────────────────────────
elif st.session_state.active_page == "🤖 AI Buddy Persona":
    render_persona_page()

# ── PROMPT TEMPLATES ───────────────────────────────────────────────
elif st.session_state.active_page == "📋 Prompt Templates":
    render_prompt_templates_page()

# ── SAMPLE CONVERSATION ────────────────────────────────────────────
elif st.session_state.active_page == "💬 Sample Conversation":
    render_sample_conversation_page()

# ── QUIZ ───────────────────────────────────────────────────────────
elif st.session_state.active_page == "❓ Quiz":
    st.markdown("## Machine Learning Quiz")
    st.markdown("Select a topic and test your understanding with 5 multiple-choice questions.")

    selected_quiz_topic = st.selectbox(
        "Select a Topic:",
        options=list(ML_TOPICS.keys()),
        index=list(ML_TOPICS.keys()).index(st.session_state.current_topic),
        key="quiz_page_topic_select"
    )
    if selected_quiz_topic != st.session_state.current_topic:
        st.session_state.current_topic = selected_quiz_topic
        st.session_state.active_quiz = None
        st.session_state.quiz_submitted = False
        st.rerun()
    render_quiz_section(selected_quiz_topic)

# ── REFLECTION REPORT ──────────────────────────────────────────────
elif st.session_state.active_page == "📝 Reflection Report":
    render_reflection_report_page()

# ── CHAT ROOM (Advanced) ───────────────────────────────────────────
elif st.session_state.active_page == "🗨️ Chat Room":
    render_conversation_page()

# ── GOOGLE GEMINI API CONFIGURATION (Advanced) ─────────────────────
elif st.session_state.active_page == "⚙️ API Configuration":
    st.markdown("## Google Gemini API Configuration")
    st.markdown(
        "Enter your Google Gemini API key to enable AI-powered explanations, "
        "real-life examples, quiz generation, and live chat. "
        "Without a key the application runs in **Offline Learning Mode** using "
        "pre-built educational content."
    )

    # Use st.text_input directly so typing is saved instantly
    entered_key = st.text_input(
        "Gemini API Key",
        value=st.session_state.api_key_gemini,
        type="password",
        placeholder="Paste your Google Gemini API key here",
        key="api_key_input_field"
    )

    if entered_key != st.session_state.api_key_gemini:
        st.session_state.api_key_gemini = entered_key.strip()
        st.rerun()

    col1, col2 = st.columns([1, 2])
    with col1:
        test_clicked = st.button("Test Connection", type="primary")
    with col2:
        if test_clicked:
            if not st.session_state.api_key_gemini:
                st.warning("Please enter an API Key first.")
            else:
                with st.spinner("Testing API connection..."):
                    success, message = test_gemini_connection(st.session_state.api_key_gemini)
                    if success:
                        st.success(message)
                    else:
                        st.error(f"Connection Failed: {message}")

    st.markdown("---")
    if st.session_state.api_key_gemini.strip():
        st.success("Gemini API key is configured. AI-powered content generation is active.")
    else:
        st.warning(
            "Gemini API key not configured.\n\n"
            "Running in Offline Learning Mode. All lessons, quizzes, and examples "
            "will use pre-built educational content."
        )

    st.info("Get a free Gemini API key at: https://aistudio.google.com/app/apikey")
    render_footer()

# ── REFLECTION DIARY (Advanced) ────────────────────────────────────
elif st.session_state.active_page == "📓 Reflection Diary":
    render_reflection_diary_page()

# ── PROGRESS ANALYTICS (Advanced) ─────────────────────────────────
elif st.session_state.active_page == "📊 Progress Analytics":
    render_progress_analytics_page()
