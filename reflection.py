import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from prompts import ML_TOPICS
from utils import render_footer, render_responsible_ai_disclaimer

def render_reflection_report_page():
    """
    Renders the dedicated professional Reflection Report page with download functionality.
    """
    st.markdown("## Capstone Reflection Report")
    render_responsible_ai_disclaimer()
    
    reflection_text = (
        "Infosys Springboard AI EMPOW(H)ER Week 8 Capstone Reflection\n"
        "==========================================================\n\n"
        "1. What I Learned from Building the AI Learning Buddy:\n"
        "Developing this application demonstrated how to successfully bridge artificial intelligence "
        "and frontend user experience. Building ML Mentor taught me the importance of state management in "
        "interactive web applications, dynamic API integration, and how custom system instructions "
        "determine the persona, tone, and quality of AI outputs. It highlighted how Python and Streamlit "
        "can be used to build modular, responsive prototypes rapidly.\n\n"
        "2. Benefits of Generative AI in Education:\n"
        "Generative AI has the unique capability to offer customized, round-the-clock tutoring. "
        "Unlike static textbooks, it can adapt its explanations to different comprehension speeds, "
        "generate personalized analogies based on user interests, and compile dynamic assessments "
        "on the fly. This levels the playing field, making high-quality, personalized tuition accessible "
        "to any beginner student.\n\n"
        "3. Limitations of AI (Hallucinations, Bias, & Verification):\n"
        "Despite its benefits, Generative AI has key technical limitations. AI models can experience "
        "hallucinations, confidently generating factually incorrect explanations or invalid python code. "
        "They can also perpetuate dataset bias, reflecting stereotypes present in their training corpora. "
        "Therefore, human verification remains critical. Educational AI must be positioned as a supportive "
        "co-pilot rather than an unverified absolute authority.\n\n"
        "4. Responsible AI & Future Improvements:\n"
        "Adhering to Responsible AI principles involves setting strict scope guardrails, protecting student "
        "input privacy, and outlining the clear limitations of the tool. Future iterations of this project "
        "aim to incorporate Retrieval-Augmented Generation (RAG) using verified textbooks to prevent "
        "hallucinations, integrate speech-to-text voice tutoring, and expand diagnostic visualization "
        "dashboards to track cumulative subject mastery."
    )
    
    # Render report inside a structured dashboard layout
    report_html = (
        "<div class=\"content-card\" style=\"border-top: 5px solid #1e3a8a; background-color: #ffffff; line-height: 1.7; padding: 2rem; color: #1f2937;\">"
        "<h3 style=\"color:#1e3a8a; margin-top:0; margin-bottom: 20px; font-family:'Outfit';\">Capstone Reflection Paper</h3>"
        "<p><strong>1. What I Learned from Building the AI Learning Buddy:</strong><br>"
        "Developing this application demonstrated how to successfully bridge artificial intelligence and frontend user experience. "
        "Building ML Mentor taught me the importance of state management in interactive web applications, dynamic API integration, and "
        "how custom system instructions determine the persona, tone, and quality of AI outputs. It highlighted how Python and "
        "Streamlit can be used to build modular, responsive prototypes rapidly.</p>"
        "<p><strong>2. Benefits of Generative AI in Education:</strong><br>"
        "Generative AI has the unique capability to offer customized, round-the-clock tutoring. Unlike static textbooks, it "
        "can adapt its explanations to different comprehension speeds, generate personalized analogies based on user interests, "
        "and compile dynamic assessments on the fly. This levels the playing field, making high-quality, personalized tuition "
        "accessible to any beginner student.</p>"
        "<p><strong>3. Limitations of AI (Hallucinations, Bias, & Verification):</strong><br>"
        "Despite its benefits, Generative AI has key technical limitations. AI models can experience <strong>hallucinations</strong>, "
        "confidently generating factually incorrect explanations or invalid python code. They can also perpetuate dataset <strong>bias</strong>, "
        "reflecting stereotypes present in their training corpora. Therefore, <strong>human verification</strong> remains critical. "
        "Educational AI must be positioned as a supportive co-pilot rather than an unverified absolute authority.</p>"
        "<p><strong>4. Responsible AI & Future Improvements:</strong><br>"
        "Adhering to <strong>Responsible AI</strong> principles involves setting strict scope guardrails, protecting student input privacy, "
        "and outlining the clear limitations of the tool. Future iterations of this project aim to incorporate Retrieval-Augmented "
        "Generation (RAG) using verified textbooks to prevent hallucinations, integrate speech-to-text voice tutoring, and expand "
        "diagnostic visualization dashboards to track cumulative subject mastery.</p>"
        "</div>"
    )
    st.markdown(report_html, unsafe_allow_html=True)
    
    st.markdown("### Export Reflection Report")
    st.markdown("Download this reflection report as a local text file for submission.")
    
    st.download_button(
        label="Download Reflection Report (TXT)",
        data=reflection_text,
        file_name="AI_Learning_Buddy_Reflection_Report.txt",
        mime="text/plain"
    )
    render_footer()

def render_reflection_diary_page():
    """
    Renders the Student Reflection Journal Page.
    """
    st.markdown("## Reflection Diary")
    st.markdown("Write down what you learned today. Translating code or math into your own words is key!")
    
    with st.form(key="reflection_form", clear_on_submit=True):
        topic = st.selectbox(
            "Which topic did you study?",
            options=list(ML_TOPICS.keys())
        )
        
        confidence = st.slider(
            "How confident do you feel about this topic?",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = Very confused, 5 = Mastered it, could teach others!"
        )
        
        summary = st.text_area(
            "What did you learn? (Briefly explain in your own words)",
            placeholder="e.g., Today I learned that K-Means is Unsupervised because we have no labels..."
        )
        
        submit_reflection = st.form_submit_button("Save Reflection Entry")
        
    if submit_reflection:
        if not summary.strip():
            st.warning("Please write a short summary before saving!")
        else:
            new_entry = {
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "topic": topic,
                "confidence": confidence,
                "summary": summary.strip()
            }
            st.session_state.reflection_logs.append(new_entry)
            st.success("Reflection entry saved successfully!")
            st.rerun()
            
    # Display past logs
    if st.session_state.reflection_logs:
        st.markdown("---")
        st.markdown("### Reflection History")
        for entry in reversed(st.session_state.reflection_logs):
            st.markdown(
                f"""
                <div style="background-color: #f8fafc; border-left: 4px solid #3b82f6; padding: 12px; border-radius: 6px; margin-bottom: 12px;">
                    <span style="color: #64748b; font-size: 12px;">Date: {entry['date']}</span>
                    <h4 style="color: #1e3a8a; margin: 4px 0 8px 0;">{entry['topic']}</h4>
                    <div style="margin-bottom: 8px;">
                        <strong>Confidence Level:</strong> {entry['confidence']}/5
                    </div>
                    <p style="margin: 0; font-size: 14px; color: #334155; font-style: italic;">
                        "{entry['summary']}"
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("You haven't logged any reflections yet. Start studying a topic and submit your first entry above!")
    render_footer()

def render_progress_analytics_page():
    """
    Renders the Progress Analytics Dashboard.
    """
    st.markdown("## Progress Analytics")
    st.markdown("Check your performance dashboards and receive custom study recommendations.")
    
    # Calculate Syllabus Completion Metrics
    total_topics = len(ML_TOPICS)
    completed_topics = sum(1 for val in st.session_state.learning_progress.values() if val)
    completion_rate = int((completed_topics / total_topics) * 100)
    
    # Gauge / Progress Summary Card
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-val">{completed_topics} / {total_topics}</div>
                <div class="metric-lbl">Topics Completed</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-val">{completion_rate}%</div>
                <div class="metric-lbl">Syllabus Progress</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        # Calculate Average Quiz Score
        quiz_scores = list(st.session_state.quiz_scores.values())
        avg_score = round(sum(quiz_scores) / len(quiz_scores), 1) if quiz_scores else 0.0
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-val">{avg_score} / 5</div>
                <div class="metric-lbl">Avg Quiz Score</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visual charts (using Plotly)
    if st.session_state.quiz_scores or st.session_state.reflection_logs:
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("#### Quiz Scores by Topic")
            if st.session_state.quiz_scores:
                df_quiz = pd.DataFrame({
                    "Topic": list(st.session_state.quiz_scores.keys()),
                    "Score": list(st.session_state.quiz_scores.values())
                })
                fig_quiz = px.bar(
                    df_quiz, 
                    x="Score", 
                    y="Topic", 
                    orientation="h",
                    range_x=[0, 5],
                    color="Score",
                    color_continuous_scale=["#93c5fd", "#3b82f6", "#1d4ed8"],
                    labels={"Score": "Score (out of 5)"}
                )
                fig_quiz.update_layout(
                    margin=dict(l=20, r=20, t=10, b=10),
                    height=250,
                    coloraxis_showscale=False,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig_quiz, use_container_width=True)
            else:
                st.info("Take a quiz to see your quiz analytics here!")
                
        with col_chart2:
            st.markdown("#### Confidence Levels")
            if st.session_state.reflection_logs:
                df_ref = pd.DataFrame(st.session_state.reflection_logs)
                # Group by topic and get last confidence recorded
                df_conf = df_ref.groupby("topic")["confidence"].last().reset_index()
                
                fig_conf = px.line(
                    df_conf, 
                    x="topic", 
                    y="confidence", 
                    markers=True,
                    range_y=[0.5, 5.5],
                    labels={"confidence": "Confidence Rating", "topic": "Topic"}
                )
                fig_conf.update_traces(line_color="#3b82f6", marker=dict(size=8, color="#1e3a8a"))
                fig_conf.update_layout(
                    margin=dict(l=20, r=20, t=10, b=10),
                    height=250,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig_conf, use_container_width=True)
            else:
                st.info("Log a reflection entry to see your confidence graph here!")
                
        # Personalized AI Tutor Recommendations
        st.markdown("---")
        st.markdown("### 🤖 ML Mentor's Recommendations")
        
        recommendations = []
        
        # Check completed vs not started
        for topic in ML_TOPICS:
            best_score = st.session_state.quiz_scores.get(topic, None)
            conf = None
            topic_logs = [log for log in st.session_state.reflection_logs if log["topic"] == topic]
            if topic_logs:
                conf = topic_logs[-1]["confidence"]
            
            # Check criteria
            if best_score is not None and best_score < 3:
                recommendations.append(
                    f"Your best score for **{topic}** is {best_score}/5. "
                    "Try reviewing the explanation card or asking ML Mentor details, and then retake the quiz to pass!"
                )
            elif conf is not None and conf <= 2:
                recommendations.append(
                    f"You rated your confidence on **{topic}** as low ({conf}/5). "
                    "Try reading the real-life examples and explaining the concepts in the study chat with ML Mentor."
                )
                
        if not recommendations:
            if completed_topics == 0:
                st.markdown("Welcome to the academy! Pick a topic, study the explanations, and take your first quiz. ML Mentor is rooting for you!")
            else:
                st.markdown("Superb progress! You're on track and have solid mastery. Pick a brand-new topic to continue your learning journey!")
        else:
            for rec in recommendations[:3]: # Limit to top 3
                st.markdown(rec)
    else:
        st.info("Complete quizzes or log study diaries to unlock interactive progress charts and recommendations!")
    render_footer()
