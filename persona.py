import streamlit as st
from utils import render_footer

# Define the AI tutor persona settings
AI_PERSONA = {
    "name": "ML Mentor",
    "avatar": "🤖",
    "tagline": "Your Friendly ML Learning Guide",
    "description": (
        "ML Mentor is a patient, highly encouraging, and creative AI tutor. "
        "They specialize in breaking down complex Machine Learning concepts into simple, "
        "digestible, and clear explanations using real-life analogies."
    ),
    "traits": [
        "Patient & Encouraging: Celebrates small wins and treats mistakes as learning opportunities.",
        "Analogy Master: Connects mathematical algorithms to daily life scenarios.",
        "Interactive: Frequently asks follow-up questions to keep students engaged.",
        "Jargon Buster: Avoids unnecessary math formulas unless fully explained step-by-step."
    ],
    "encouraging_phrases": [
        "That's a fantastic question! Let's break it down together.",
        "Great effort! You're getting closer to mastering this.",
        "Spot on! See, you're already thinking like a data scientist!",
        "Don't worry if it feels tricky at first—even top ML researchers started exactly here.",
        "Let's tackle this step-by-step. You've got this!"
    ]
}

def get_system_instruction(custom_persona_instructions=None):
    """
    Returns the core system prompt that dictates how ML Mentor behaves when interacting with the user.
    """
    base_instruction = (
        f"You are {AI_PERSONA['name']}, a friendly, enthusiastic, and patient AI learning tutor. "
        f"Your goal is to teach Machine Learning Fundamentals to beginners. "
        "Always adhere to these guidelines:\n"
        "1. EXPLAIN IN SIMPLE LANGUAGE: Avoid academic jargon. If you must use a technical term (like 'gradient descent' or 'overfitting'), "
        "explain it immediately using an intuitive, real-world comparison.\n"
        "2. USE REAL-LIFE EXAMPLES & ANALOGIES: Always connect concepts to relatable everyday experiences (e.g., predicting house prices, "
        "sorting laundry, training a dog).\n"
        "3. BE SUPPORTIVE & ENCOURAGING: Use a friendly, warm, and positive tone. Use exclamation marks occasionally to express excitement. "
        "Validate the user's responses, even if they are partially incorrect, and steer them gently toward the correct answer.\n"
        "4. KEEP IT INTERACTIVE: Don't just dump text. Conclude your responses with an engaging question, a mini-challenge, or a quick prompt "
        "to check their understanding.\n"
        "5. VISUAL & STRUCTURAL CLARITY: Use markdown formatting, bullet points, and bold text to make explanations easy to scan.\n"
    )
    if custom_persona_instructions:
        base_instruction += f"\nCustom User Request: {custom_persona_instructions}"
    
    return base_instruction

def render_persona_sidebar():
    """
    Renders the AI Persona card and details inside the Streamlit sidebar.
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### {AI_PERSONA['avatar']} About Your AI Buddy")
    
    # Styled card for the persona
    st.sidebar.markdown(
        f"""
        <div style="background-color: #f0f7ff; padding: 15px; border-radius: 10px; border-left: 5px solid #1e3a8a; margin-bottom: 15px;">
            <h4 style="color: #1e3a8a; margin: 0 0 5px 0;">{AI_PERSONA['name']}</h4>
            <small style="color: #4b5563; font-style: italic; font-weight: 600;">{AI_PERSONA['tagline']}</small>
            <p style="color: #1f2937; font-size: 14px; margin-top: 8px; margin-bottom: 0;">
                {AI_PERSONA['description']}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    with st.sidebar.expander("ML Mentor's Superpowers", expanded=False):
        for trait in AI_PERSONA["traits"]:
            st.markdown(f"• **{trait.split(':')[0]}**: {trait.split(':')[1]}")
            
    # Allow customization of the learning tone
    st.sidebar.markdown("### ⚙️ Tutor Settings")
    tone = st.sidebar.select_slider(
        "Tutor Tone",
        options=["Casual & Fun", "Balanced", "Detail-Oriented"],
        value="Balanced"
    )
    return tone

def render_persona_page():
    """
    Renders the dedicated AI Buddy Persona page.
    """
    st.markdown("## 🤖 AI Buddy Persona Profile")
    st.markdown(
        "Discover the pedagogical design, learning goals, and guiding parameters of your virtual tutor, ML Mentor."
    )
    
    # Hero Motivation Banner
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 2rem; border-radius: 12px; margin-bottom: 2rem; text-align: center; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.15);">
            <div style="font-size: 3rem; margin-bottom: 10px;">🤖</div>
            <h2 style="color: white; margin: 0 0 10px 0; font-family: 'Outfit', sans-serif;">Meet ML Mentor</h2>
            <p style="font-style: italic; font-size: 1.2rem; margin: 0; opacity: 0.9;">
                "Remember, every expert was once a beginner. Let's make mistakes, learn from them, and build the future together!"
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 2-column grid layout for core details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div class="content-card" style="border-top: 4px solid #3b82f6; height: 100%;">
                <h3 style="margin-top:0; color:#1e3a8a;">📝 Core Identity</h3>
                <table style="width:100%; border-collapse: collapse; font-size: 14px;">
                    <tr style="border-bottom: 1px solid #e5e7eb;">
                        <td style="padding: 8px 0; font-weight: 600; color:#4b5563; width:35%;">Name</td>
                        <td style="padding: 8px 0; color:#1f2937;">ML Mentor</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e5e7eb;">
                        <td style="padding: 8px 0; font-weight: 600; color:#4b5563;">Role</td>
                        <td style="padding: 8px 0; color:#1f2937;">Virtual ML Learning Buddy & AI Tutor</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e5e7eb;">
                        <td style="padding: 8px 0; font-weight: 600; color:#4b5563;">Audience</td>
                        <td style="padding: 8px 0; color:#1f2937;">Beginners, Freshmen, & Curious Minds</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; font-weight: 600; color:#4b5563;">Focus Area</td>
                        <td style="padding: 8px 0; color:#1f2937;">Machine Learning Fundamentals</td>
                    </tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div class="content-card" style="border-top: 4px solid #2563eb; margin-top: 1.5rem;">
                <h3 style="margin-top:0; color:#1e3a8a;">Teaching Style</h3>
                <ul style="font-size: 14px; padding-left: 20px; color:#1f2937; line-height: 1.6;">
                    <li><strong>Socratic Checkpoints</strong>: Periodically tests understanding through contextual questions rather than lecturing.</li>
                    <li><strong>Analogy-First Explanations</strong>: Breaks down abstract concepts (like KNN or Decision Trees) into simple, everyday comparisons.</li>
                    <li><strong>Jargon-Busting Definitions</strong>: Highlights technical terms and unpacks their definitions immediately.</li>
                    <li><strong>Patience-Driven Scaffolding</strong>: Adapts difficulty dynamically and celebrates progress.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col2:
        st.markdown(
            """
            <div class="content-card" style="border-top: 4px solid #3b82f6; height: 100%;">
                <h3 style="margin-top:0; color:#1e3a8a;">Personality & Traits</h3>
                <ul style="font-size: 14px; padding-left: 20px; color:#1f2937; line-height: 1.6;">
                    <li><strong>Patient & Supportive</strong>: Views mistakes as milestones and encourages repetitive practice.</li>
                    <li><strong>Enthusiastic</strong>: Expresses excitement about model training, algorithms, and predictions.</li>
                    <li><strong>Empathetic</strong>: Understands 'math anxiety' and lowers barriers to entry.</li>
                    <li><strong>Structured</strong>: Uses clear Markdown, listicle formats, and highlights.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div class="content-card" style="border-top: 4px solid #2563eb; margin-top: 1.5rem;">
                <h3 style="margin-top:0; color:#1e3a8a;">Core Strengths & Learning Goals</h3>
                <ul style="font-size: 14px; padding-left: 20px; color:#1f2937; line-height: 1.6;">
                    <li><strong>Intuitive Concept Mapping</strong>: Maps code/math algorithms into real-world business models.</li>
                    <li><strong>Fear-Free Assessment</strong>: Provides supportive, diagnostic quiz feedback.</li>
                    <li><strong>Self-Directed Mastery</strong>: Boosts student retention using systematic reflection logs.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    render_footer()
