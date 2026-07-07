import json
import streamlit as st
import datetime
import random
from utils import call_llm, render_footer
from prompts import get_quiz_prompt, get_feedback_prompt

# --- Fallback Local Quiz Data for all 11 topics ---
OFFLINE_QUIZZES = {
    "What is Machine Learning?": [
        {
            "id": 1,
            "question": "What is the core idea behind Machine Learning?",
            "options": [
                "Writing explicit step-by-step instructions for every possible scenario.",
                "Letting computers learn patterns from data to make their own decisions.",
                "Replacing computer hardware with biological brains.",
                "Writing programs that never need to be updated."
            ],
            "correct_answer": "Letting computers learn patterns from data to make their own decisions.",
            "explanation": "Traditional programming uses explicit rules. Machine Learning enables the computer to find patterns in data and construct its own rules!"
        },
        {
            "id": 2,
            "question": "In the analogy of teaching a child to recognize apples, what does 'showing pictures of apples' represent?",
            "options": [
                "Writing code",
                "Compiling a program",
                "Training Data",
                "An output label"
            ],
            "correct_answer": "Training Data",
            "explanation": "The pictures are the examples (data) we use to train the child's brain (model) to recognize features."
        },
        {
            "id": 3,
            "question": "Which of the following is an example of Machine Learning in daily life?",
            "options": [
                "A digital clock displaying the time.",
                "A calculator adding two numbers.",
                "A streaming service suggesting songs based on your listening history.",
                "A word document saving your text."
            ],
            "correct_answer": "A streaming service suggesting songs based on your listening history.",
            "explanation": "The streaming service analyzes data (your history) to predict what you will like next, which is a classic ML application."
        },
        {
            "id": 4,
            "question": "What is a 'label' in Machine Learning?",
            "options": [
                "The brand name of the computer running the model.",
                "The raw input variables.",
                "The target output or 'correct answer' we want the model to predict.",
                "The name of the programmer."
            ],
            "correct_answer": "The target output or 'correct answer' we want the model to predict.",
            "explanation": "A label is the ground truth output, like 'Spam' or 'Inbox' for an email, or 'Apple' for a picture."
        },
        {
            "id": 5,
            "question": "What happens after an ML model is successfully trained?",
            "options": [
                "It deletes all its previous programming.",
                "It can make predictions or decisions on new, unseen data.",
                "It requires a human to review every single output it makes.",
                "It locks the computer from further use."
            ],
            "correct_answer": "It can make predictions or decisions on new, unseen data.",
            "explanation": "The entire point of training is generalization—using what it learned from training data to make predictions on new data."
        }
    ],
    "Types of Machine Learning": [
        {
            "id": 1,
            "question": "Which type of learning involves training a model on data that has inputs and correct output labels?",
            "options": [
                "Supervised Learning",
                "Unsupervised Learning",
                "Reinforcement Learning",
                "Self-learning"
            ],
            "correct_answer": "Supervised Learning",
            "explanation": "Supervised learning uses labeled data, meaning the correct answers are provided during training."
        },
        {
            "id": 2,
            "question": "If you want to group your customers into groups with similar shopping habits without any pre-defined categories, which type of learning should you use?",
            "options": [
                "Supervised Learning",
                "Unsupervised Learning",
                "Reinforcement Learning",
                "Rule-based Learning"
            ],
            "correct_answer": "Unsupervised Learning",
            "explanation": "Since there are no pre-defined categories (labels), unsupervised learning is used to find hidden patterns and clusters."
        },
        {
            "id": 3,
            "question": "What is the core mechanic of Reinforcement Learning?",
            "options": [
                "Following strict mathematical equations written by engineers.",
                "Learning from labeled pictures of dogs and cats.",
                "Interacting with an environment and learning from rewards and penalties.",
                "Sorting files alphabetically."
            ],
            "correct_answer": "Interacting with an environment and learning from rewards and penalties.",
            "explanation": "Reinforcement learning mimics trial-and-error learning, using rewards for good actions and penalties for bad ones."
        },
        {
            "id": 4,
            "question": "A weather forecasting model predicting the exact temperature tomorrow is an example of what kind of task?",
            "options": [
                "Unsupervised Clustering",
                "Supervised Regression",
                "Supervised Classification",
                "Reinforcement Action"
            ],
            "correct_answer": "Supervised Regression",
            "explanation": "Temperature is a continuous number. Predicting continuous numbers based on labeled historical data is Regression (a Supervised task)."
        },
        {
            "id": 5,
            "question": "Sorting customer emails into 'Complaint', 'Feedback', or 'Inquiry' is what type of task?",
            "options": [
                "Regression",
                "Classification",
                "Clustering",
                "Reinforcement Learning"
            ],
            "correct_answer": "Classification",
            "explanation": "Sorting things into pre-defined categories is Classification (a Supervised task)."
        }
    ]
}

def load_default_quiz(topic: str) -> dict:
    """
    Returns a default quiz from our offline database. If the specific topic is not found,
    it returns a generic quiz structure or generates one dynamically.
    Shuffles questions and option order to provide a dynamic testing experience.
    """
    raw_questions = []
    if topic in OFFLINE_QUIZZES:
        raw_questions = OFFLINE_QUIZZES[topic]
    else:
        # Generic backup quiz for remaining topics
        raw_questions = [
            {
                "id": 1,
                "question": f"Which of the following is true about {topic}?",
                "options": [
                    "It is a core concept in Machine Learning.",
                    "It is never used in real-life applications.",
                    "It was invented last week.",
                    "It requires no computer code to run."
                ],
                "correct_answer": "It is a core concept in Machine Learning.",
                "explanation": f"{topic} is an essential tool in data science used for extracting patterns and building models."
            },
            {
                "id": 2,
                "question": f"Why is {topic} taught to beginners in Machine Learning?",
                "options": [
                    "It helps build a foundation for understanding more complex models.",
                    "It is the only algorithm used by major tech companies.",
                    "It is completely unrelated to programming.",
                    "It does not require any data."
                ],
                "correct_answer": "It helps build a foundation for understanding more complex models.",
                "explanation": f"Understanding {topic} gives students intuition on how algorithms make splits, distance-measures, or weights."
            },
            {
                "id": 3,
                "question": f"What is a common challenge when implementing {topic}?",
                "options": [
                    "Selecting the right parameters (tuning).",
                    "It can only run on calculators.",
                    "It is illegal to use in business.",
                    "It deletes the training set automatically."
                ],
                "correct_answer": "Selecting the right parameters (tuning).",
                "explanation": "Tuning hyper-parameters (like 'K' in KNN, tree depth, or number of clusters) is crucial to get good accuracy."
            },
            {
                "id": 4,
                "question": f"What type of problems does {topic} solve?",
                "options": [
                    "Data-driven prediction or classification tasks.",
                    "Solving hard physics gravity questions.",
                    "Designing graphics for websites.",
                    "Checking spellings in text documents."
                ],
                "correct_answer": "Data-driven prediction or classification tasks.",
                "explanation": "In ML, we use these algorithms to classify labels, predict numbers, or cluster patterns."
            },
            {
                "id": 5,
                "question": f"To improve a model using {topic}, you should generally:",
                "options": [
                    "Provide more high-quality clean training data.",
                    "Remove all input features.",
                    "Turn off the computer.",
                    "Write random code."
                ],
                "correct_answer": "Provide more high-quality clean training data.",
                "explanation": "More clean, diverse, and well-labeled data is almost always the best way to improve any machine learning model."
            }
        ]

    # Deep copy raw questions to avoid mutating the source database
    questions_copy = json.loads(json.dumps(raw_questions))
    
    # Shuffle question order
    random.shuffle(questions_copy)
    
    # Shuffle options for each question
    for q in questions_copy:
        options = q["options"]
        random.shuffle(options)
        
    return {"questions": questions_copy}

def generate_quiz(topic: str) -> dict:
    """
    Fetches a quiz. Tries LLM first (returning parsed JSON). If it fails or key is missing,
    loads the pre-made fallback quiz.
    """
    system_prompt = "You are a quiz generator bot. You generate JSON-formatted multiple choice quizzes."
    user_prompt = get_quiz_prompt(topic)
    
    # Try calling the LLM
    response_text = call_llm(system_prompt, user_prompt, temperature=0.7)
    
    if response_text:
        # Strip potential markdown backticks
        clean_text = response_text.replace("```json", "").replace("```", "").strip()
        try:
            quiz_data = json.loads(clean_text)
            # Basic validation
            if "questions" in quiz_data and len(quiz_data["questions"]) == 5:
                return quiz_data
        except Exception:
            pass # Fall back to offline
            
    return load_default_quiz(topic)

def render_quiz_section(topic: str):
    """
    Renders the interactive quiz page in Streamlit.
    """
    st.markdown(f"## 📝 Test Your Knowledge: {topic}")
    
    # Check if a new quiz needs to be loaded
    if st.session_state.active_quiz is None or st.session_state.get("active_quiz_topic") != topic:
        with st.spinner("Creating quiz questions..."):
            st.session_state.active_quiz = generate_quiz(topic)
            st.session_state.active_quiz_topic = topic
            st.session_state.quiz_user_answers = {}
            st.session_state.quiz_submitted = False
            st.session_state.quiz_feedback = {}
            
    quiz = st.session_state.active_quiz
    questions = quiz.get("questions", [])
    
    # Render form for the quiz
    with st.form(key=f"quiz_form_{topic}"):
        for idx, q in enumerate(questions):
            q_id = q["id"]
            st.markdown(f"**Q{idx+1}: {q['question']}**")
            
            # Default to no selection by prepending a dummy value or using an index
            options = q["options"]
            
            # Get previous selection if exists
            prev_sel = st.session_state.quiz_user_answers.get(q_id, None)
            
            sel_idx = None
            if prev_sel in options:
                sel_idx = options.index(prev_sel)
                
            choice = st.radio(
                f"Select your answer for Q{idx+1}:",
                options,
                index=sel_idx,
                key=f"radio_{topic}_{q_id}",
                label_visibility="collapsed"
            )
            st.session_state.quiz_user_answers[q_id] = choice
            st.markdown("<br>", unsafe_allow_html=True)
            
        submit_button = st.form_submit_button(label="Submit Quiz")
        
    # Validation logic: Ensure all questions are answered before submitting
    all_answered = all(st.session_state.quiz_user_answers.get(q["id"]) is not None for q in questions)
    
    if submit_button:
        if not all_answered:
            st.warning("⚠️ Please select an answer for all questions before submitting the quiz!")
            st.session_state.quiz_submitted = False
        else:
            st.session_state.quiz_submitted = True
            st.rerun() # Refresh to show evaluation immediately
            
    if st.session_state.quiz_submitted:
        
        # Calculate score
        score = 0
        correct_count = 0
        
        st.markdown("---")
        st.markdown("### Evaluation")
        
        for q in questions:
            q_id = q["id"]
            user_ans = st.session_state.quiz_user_answers.get(q_id)
            corr_ans = q["correct_answer"]
            
            is_correct = (user_ans == corr_ans)
            if is_correct:
                correct_count += 1
                
            # Render styled feedback box
            if is_correct:
                st.success(f"**Question {q_id}: Correct!**")
                st.markdown(f"*Your Answer: {user_ans}*")
                st.markdown(f"**Explanation**: {q['explanation']}")
            else:
                st.error(f"**Question {q_id}: Incorrect**")
                st.markdown(f"*Your Answer: {user_ans}*")
                st.markdown(f"**Correct Answer**: **{corr_ans}**")
                st.markdown(f"**Explanation**: {q['explanation']}")
            st.markdown("<br>", unsafe_allow_html=True)
            
        # Display Final Score Card
        score_percent = int((correct_count / len(questions)) * 100)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-val">{correct_count}/{len(questions)}</div>
                    <div class="metric-lbl">Total Score</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col2:
            if correct_count == 5:
                st.balloons()
                msg = "Perfect Score! You are an ML Superstar!"
            elif correct_count >= 3:
                msg = "Great job! You have a solid grasp of this topic. Keep it up!"
            else:
                msg = "📚 Good effort! Review the explanations above and try again. Practice makes perfect!"
                
            st.markdown(f"### {msg}")
            st.markdown("Your score has been saved to your student profile reflection record.")
            
        # Save score in session state if not already recorded for this specific attempt
        # To avoid double saving on refresh, we only update progress if it is higher or first attempt
        current_best = st.session_state.quiz_scores.get(topic, 0)
        if correct_count > current_best:
            st.session_state.quiz_scores[topic] = correct_count
            
        # Mark topic as completed if score is >= 3 (passing grade)
        if correct_count >= 3:
            st.session_state.learning_progress[topic] = True
            
        # Add to history attempts
        if topic not in st.session_state.quiz_attempts:
            st.session_state.quiz_attempts[topic] = []
            
        # Add timestamped record
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        # Prevent duplicate entries for the exact same score on double clicks
        attempts = st.session_state.quiz_attempts[topic]
        if not attempts or attempts[-1]["score"] != correct_count or (datetime.datetime.now() - datetime.datetime.strptime(attempts[-1]["date"], "%Y-%m-%d %H:%M")).seconds > 10:
            st.session_state.quiz_attempts[topic].append({"date": now_str, "score": correct_count})
            
        # Button to retry/reset quiz
        if st.button("Try a New Quiz"):
            st.session_state.active_quiz = None
            st.session_state.quiz_submitted = False
            st.rerun()
    render_footer()
