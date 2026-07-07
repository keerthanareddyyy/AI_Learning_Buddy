import streamlit as st
from utils import call_llm, render_footer
from persona import get_system_instruction, AI_PERSONA
from prompts import ML_TOPICS

# Helper for intelligent keyword-based offline responses
OFFLINE_RESPONSES = {
    "supervised": "Supervised Learning is like learning with a teacher! You feed the model labeled training data (like inputs and correct answers) so it learns to map inputs to the right outputs. It's used for Regression (predicting numbers, like house prices) and Classification (predicting categories, like spam or not spam). What specific supervised algorithm (like Decision Trees or KNN) would you like to explore?",
    "unsupervised": "Unsupervised Learning is when the computer learns on its own without any labels or teacher. It looks at the data and groups similar items together, which is called Clustering (like K-Means). For example, it can group customers based on their buying habits so you can target them with special deals.",
    "reinforcement": "Reinforcement Learning is like training a puppy using treats (rewards) and corrections (penalties)! An agent interacts with an environment and tries to maximize its total reward by trying different things. It's how self-driving cars learn to stay on the road and how AI beats humans at video games.",
    "decision tree": "A Decision Tree is like playing a game of 20 Questions! It makes decisions by asking simple yes/no questions (like 'Is it raining?') and following the branch down to make a prediction. They are easy to read and visualize.",
    "random forest": "A Random Forest is like a committee of Decision Trees. Instead of asking just one tree, it builds a whole forest of different trees. Each tree votes, and the majority vote wins! This makes it way more accurate and less likely to make mistakes than a single tree.",
    "knn": "KNN stands for K-Nearest Neighbors. It operates on the rule: 'Birds of a feather flock together!' To classify a new data point, it looks at its K closest neighbors in the dataset. If the majority of neighbors belong to Group A, then the new point is labeled Group A too! Simple and intuitive.",
    "k-means": "K-Means is a clustering algorithm. It groups data into 'K' clusters. It starts by picking K center points, groups the nearest data points to them, finds the new centers of those groups, and repeats. It's like sorting people by size to design Small, Medium, and Large T-shirts.",
    "ann": "ANN stands for Artificial Neural Network. It is inspired by how the human brain works! It has an input layer, hidden layers that extract patterns step-by-step, and an output layer. It is the building block of Deep Learning and is used for advanced things like face recognition.",
    "evaluation": "Model Evaluation helps us know if our model is actually good. We use metrics like Accuracy (what we got right), Precision (minimizing false positives), Recall (minimizing false negatives), and a Confusion Matrix (a cheat sheet grid of predictions vs. reality) depending on the problem.",
    "hello": "Hello there! I'm ML Mentor. I'm excited to chat about Machine Learning today. What concepts are you currently studying, or would you like to start from the beginning?",
    "hi": "Hi! Great to see you in the study lab. Ready to learn some Machine Learning concepts? Let me know what is on your mind.",
    "help": "I can help you understand ML Fundamentals! Just ask me questions like 'What is Supervised Learning?', 'How does KNN work?', or 'Can you give me an example of Random Forest?'"
}

def get_offline_response(user_msg: str) -> str:
    """
    Scans the user message for keywords and returns a friendly, matching response.
    If no keywords match, returns a supportive general tutor message.
    """
    msg_lower = user_msg.lower()
    
    # Check for direct keyword matches
    for key, response in OFFLINE_RESPONSES.items():
        if key in msg_lower:
            return response
            
    # Check if they are asking about topics in our ML list
    for topic in ML_TOPICS.keys():
        if topic.lower() in msg_lower:
            return f"Ah, you are asking about {topic}! " + ML_TOPICS[topic]["fallback_explanation"]
            
    # Default encouraging response if offline and no keyword found
    return (
        "That's a great question! Since we are currently in offline/sandbox mode (no API Key set), "
        "I can answer best if you ask me about specific topics we have prepared: \n\n"
        "- Supervised vs. Unsupervised Learning\n"
        "- Decision Trees, Random Forest, KNN, or K-Means\n"
        "- Artificial Neural Networks (ANN)\n"
        "- Model Evaluation metrics\n\n"
        "Feel free to type any of these keywords, or enter your API key in the configuration section to activate full conversational AI."
    )

def render_conversation_page():
    """
    Renders the interactive chat panel page in Streamlit.
    """
    st.markdown("## Chat Room")
    st.markdown(
        "Ask ML Mentor anything about Machine Learning! They will answer using simple, everyday analogies, "
        "explain definitions, and guide you through your studies."
    )
    
    # API status indicator in chat
    api_key_set = bool(st.session_state.get("api_key_gemini", "").strip())
    if api_key_set:
        st.info("ML Mentor is online with full AI capabilities (Google Gemini).", icon="🤖")
    else:
        st.warning("ML Mentor is in sandbox/offline learning mode. They will respond using pre-trained offline study guides. (Add an API Key in the Configuration page to activate full conversational AI.)", icon="🤖")
        
    # Render chat container
    st.markdown('<div style="margin-bottom: 20px;"></div>', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        role = msg["role"]
        content = msg["content"]
        
        if role == "user":
            st.markdown(
                f"""
                <div class="chat-bubble chat-user">
                    <strong>Student</strong><br>
                    {content}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="chat-bubble chat-agent">
                    <strong>🤖 {AI_PERSONA['name']}</strong><br>
                    {content}
                </div>
                """,
                unsafe_allow_html=True
            )
            
    # Input area for user message
    with st.container():
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input("Type your question for ML Mentor here...", placeholder="e.g., Explain Supervised vs Unsupervised learning using a bakery analogy!")
            submit_chat = st.form_submit_button("Send")
            
        if submit_chat and user_input.strip() != "":
            # Append user message
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Generate assistant response
            with st.spinner("ML Mentor is thinking..."):
                if api_key_set:
                    system_instruction = get_system_instruction()
                    prompt = get_conversation_prompt(st.session_state.chat_history[:-1], user_input)
                    reply = call_llm(system_instruction, prompt, temperature=0.7)
                    if not reply:
                        # Fallback if API fails
                        reply = get_offline_response(user_input)
                else:
                    reply = get_offline_response(user_input)
                    
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()
            
    # Clear conversation history button
    if len(st.session_state.chat_history) > 1:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Clear Chat History"):
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Hi there! I'm ML Mentor, your AI learning buddy. Let's explore the exciting world of Machine Learning together! What would you like to learn first?"}
            ]
            st.rerun()
    render_footer()

def get_conversation_prompt(chat_history: list, user_message: str) -> str:
    """
    Generates a prompt for ongoing conversation with the user in the learning chat.
    """
    history_str = ""
    for msg in chat_history:
        role = "User" if msg["role"] == "user" else "Tutor"
        history_str += f"{role}: {msg['content']}\n"
        
    return (
        f"The following is a chat conversation between a student and you (ML Mentor, the AI ML Tutor).\n\n"
        f"Conversation History:\n{history_str}\n"
        f"Student: {user_message}\n\n"
        "Tutor (ML Mentor): Respond to the student's message. Remember to remain friendly, supportive, "
        "explain ML concepts simply if they ask, and keep the interaction engaging."
    )

def render_sample_conversation_page():
    """
    Renders the realistic pre-generated Sample Learning Conversation between a Student and ML Mentor.
    """
    st.markdown("## AI Learning Session Example")
    st.markdown(
        "Review this realistic dialogue showing how ML Mentor guides a student from "
        "the basic definition of Machine Learning to a complete concept check."
    )
    
    sample_exchanges = [
        {
            "role": "assistant",
            "speaker": "🤖 ML Mentor (AI Buddy)",
            "content": "Hi there! I'm ML Mentor, your AI learning buddy. Let's explore the exciting world of Machine Learning! To start, do you know what Machine Learning actually means in simple terms?"
        },
        {
            "role": "user",
            "speaker": "Student",
            "content": "Honestly, not really. Is it just teaching computers to think like humans?"
        },
        {
            "role": "assistant",
            "speaker": "🤖 ML Mentor (AI Buddy)",
            "content": "That's a very common way to think about it! In simple terms, traditional programming is like a recipe book where we write down every single rule for the computer to follow. But Machine Learning is different: we give the computer lots of examples (data) and the correct answers, and let the computer figure out the rules itself. How does that sound?"
        },
        {
            "role": "user",
            "speaker": "Student",
            "content": "Ah, I see! So instead of writing code for every rule, it learns from examples. What are the main types of Machine Learning?"
        },
        {
            "role": "assistant",
            "speaker": "🤖 ML Mentor (AI Buddy)",
            "content": "Exactly! Spot on. Machine Learning is generally grouped into three main types:\n\n1. Supervised Learning: Learning with a teacher guiding you (labeled data).\n2. Unsupervised Learning: Finding patterns on your own (unlabeled data).\n3. Reinforcement Learning: Learning through trial and error (rewards/penalties).\n\nWould you like to dive deeper into Supervised Learning?"
        },
        {
            "role": "user",
            "speaker": "Student",
            "content": "Yes, let's do Supervised Learning. How does it actually work?"
        },
        {
            "role": "assistant",
            "speaker": "🤖 ML Mentor (AI Buddy)",
            "content": "Great choice! In Supervised Learning, we give the model 'labeled' training data. This means every example has the input features and the correct output target. For instance, think of predicting house prices based on size and number of bedrooms, where the target is the actual past sale price. The model learns the trend line to predict new prices!"
        },
        {
            "role": "user",
            "speaker": "Student",
            "content": "That makes sense. Can you give me another real-life example of supervised classification?"
        },
        {
            "role": "assistant",
            "speaker": "🤖 ML Mentor (AI Buddy)",
            "content": "Absolutely! A classic example is a spam filter in your email inbox. The inputs are email text, sender addresses, and attachments. The labels are 'Spam' or 'Inbox'. The model looks at millions of labeled emails to learn words like 'Winner' or 'Free Cash' and sender patterns, then classifies incoming new emails!"
        },
        {
            "role": "user",
            "speaker": "Student",
            "content": "Oh, spam filters! That's a perfect example. But wait, what if the email is not spam but contains 'Winner' because of a school contest? Won't the model block it?"
        },
        {
            "role": "assistant",
            "speaker": "🤖 ML Mentor (AI Buddy)",
            "content": "That is a brilliant question! You're pointing out what we call 'false positives'. Yes, a simple model might block it, but a robust model looks at a combination of features (sender reputation, signature, email header) rather than just a single word. That's why we evaluate model precision! Let's test your understanding with a quick question, ready?"
        },
        {
            "role": "user",
            "speaker": "Student",
            "content": "Yes, shoot!"
        },
        {
            "role": "assistant",
            "speaker": "🤖 ML Mentor (AI Buddy)",
            "content": "Here it is: If you train a model to predict whether a customer will click on an ad based on their browsing history (Yes/No), is this a Classification or a Regression task?"
        },
        {
            "role": "user",
            "speaker": "Student",
            "content": "Since we are predicting a Yes/No category, is it classification?"
        },
        {
            "role": "assistant",
            "speaker": "🤖 ML Mentor (AI Buddy)",
            "content": "You got it! Absolutely correct! Because Yes/No are categories, it is a classification task. Regression would be if we wanted to predict the exact number of minutes they spend looking at the ad. Incredible effort, you're grasping these fundamentals super fast!"
        }
    ]
    
    # Styled conversation pane
    st.markdown('<div style="background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; max-height: 600px; overflow-y: auto;">', unsafe_allow_html=True)
    
    for ex in sample_exchanges:
        role = ex["role"]
        speaker = ex["speaker"]
        content = ex["content"]
        
        if role == "user":
            st.markdown(
                f"""
                <div class="chat-bubble chat-user" style="max-width: 85%; margin-left: auto; margin-bottom: 12px;">
                    <strong>{speaker}</strong><br>
                    {content}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="chat-bubble chat-agent" style="max-width: 85%; margin-right: auto; margin-bottom: 12px;">
                    <strong>{speaker}</strong><br>
                    {content}
                </div>
                """,
                unsafe_allow_html=True
            )
            
    st.markdown('</div>', unsafe_allow_html=True)
    render_footer()
