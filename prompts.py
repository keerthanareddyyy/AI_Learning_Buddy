import streamlit as st
import random
from utils import render_footer

# Prompts and static fallback content for Machine Learning Fundamentals Learning Buddy

# Dictionary of topics and their descriptions to guide the tutor
ML_TOPICS = {
    "What is Machine Learning?": {
        "description": "Introduction to the concept of computers learning from data instead of explicit programming.",
        "fallback_explanation": (
            "Think of traditional programming like a recipe book. The programmer writes down every single step (instructions), "
            "and the computer follows them exactly. If the ingredients change slightly, the computer gets stuck.\n\n"
            "**Machine Learning (ML)** is like teaching a child how to identify a fruit. Instead of writing rules like 'it must be round, "
            "red, and have a stem to be an apple' (which might fail for green apples!), you show the child hundreds of pictures of apples, "
            "pears, and oranges. Over time, the child's brain automatically learns to spot the features of an apple.\n\n"
            "In ML, we feed a computer **data** (examples) and the **correct answers** (labels). The computer uses an **algorithm** to "
            "figure out the patterns. Once it learns the patterns, it can make predictions on brand-new data it has never seen before!"
        ),
        "fallback_example": (
            "**Real-life Example: Spam Filters in Email**\n\n"
            "How does your inbox know an email is spam? Instead of a human writing rules for every spam email ever created, "
            "the system is trained on millions of emails marked 'Spam' or 'Inbox'. The machine learning model finds patterns—like common "
            "words ('Winner', 'Free Cash'), sender addresses, or links. When a new email arrives, the model calculates the probability "
            "of it being spam based on what it learned. If it's high, it goes straight to your Spam folder!"
        )
    },
    "Types of Machine Learning": {
        "description": "Overview of Supervised, Unsupervised, and Reinforcement Learning.",
        "fallback_explanation": (
            "Machine Learning is generally divided into three main branches, depending on how the model learns:\n\n"
            "1. 🌲 **Supervised Learning**: Learning with a teacher. The computer is given labeled data (inputs and correct outputs).\n"
            "2. 🔍 **Unsupervised Learning**: Learning on your own. The computer is given unlabeled data and must find hidden patterns or structures on its own.\n"
            "3. 🕹️ **Reinforcement Learning**: Learning through trial and error. The computer (an agent) interacts with an environment and gets rewards for good actions or penalties for bad ones."
        ),
        "fallback_example": (
            "**Real-life Example: Teaching a Puppy**\n\n"
            "• **Supervised**: You show your puppy a ball, say the word 'Ball', and reward it when it repeats the sound or retrieves it. You are guiding it.\n"
            "• **Unsupervised**: You leave your puppy in a room with a pile of toys. It automatically groups them: things that squeak, things that roll, and things it can chew. Nobody told it how to group them; it just noticed common features.\n"
            "• **Reinforcement**: The puppy is learning to walk on a leash. When it pulls too hard, it gets a slight tug (penalty). When it walks nicely next to you, it gets a treat (reward). It learns the best behavior by trying to maximize treats!"
        )
    },
    "Supervised Learning": {
        "description": "Learning with labeled training data (inputs mapped to known targets).",
        "fallback_explanation": (
            "**Supervised Learning** is the most common type of ML. You feed the model 'training data' where every example contains "
            "the input features and the corresponding target output (label).\n\n"
            "There are two main types of Supervised Learning tasks:\n"
            "- **Regression**: Predicting a continuous number (e.g., predicting the price of a house, temperature tomorrow, or sales figures).\n"
            "- **Classification**: Predicting a category or label (e.g., classifying an email as Spam or Not Spam, or an image as a Cat or Dog)."
        ),
        "fallback_example": (
            "**Real-life Example: Predicting House Prices**\n\n"
            "Imagine you want to sell your house. You look at sales data for your neighborhood over the past year. Your inputs are: "
            "size (sq ft), number of bedrooms, and location. Your label (target) is the final sale price. A supervised model looks at "
            "these past sales, draws a trend line, and helps you estimate the price of your house based on its specifications."
        )
    },
    "Unsupervised Learning": {
        "description": "Learning patterns from unlabeled data, such as clustering.",
        "fallback_explanation": (
            "In **Unsupervised Learning**, the computer works with unlabeled data. There are no 'correct answers' or 'teachers'. "
            "The goal of the algorithm is to explore the data and find interesting structures, similarities, or groups on its own.\n\n"
            "Common tasks include:\n"
            "- **Clustering**: Grouping similar data points together (e.g., K-Means).\n"
            "- **Association**: Finding rules that link items (e.g., people who buy bread also buy butter)."
        ),
        "fallback_example": (
            "**Real-life Example: Customer Segmentation**\n\n"
            "A streaming service like Netflix has millions of users but doesn't know their exact personality profiles. "
            "An unsupervised clustering algorithm analyzes user watch histories. It automatically groups users into clusters: "
            "one cluster loves Anime, another loves Romantic Comedies, and a third loves true-crime documentaries. Netflix can then "
            "recommend similar shows to everyone in the same cluster!"
        )
    },
    "Reinforcement Learning": {
        "description": "Learning through rewards and penalties in an interactive environment.",
        "fallback_explanation": (
            "**Reinforcement Learning (RL)** is about learning by doing. The algorithm (called the **Agent**) makes choices "
            "in an environment to achieve a goal. For every decision it makes, it receives either a positive reward "
            "(feedback that it did well) or a negative penalty (feedback that it made a mistake).\n\n"
            "Unlike Supervised Learning, it doesn't need to be told the exact 'right' action for every single step. It "
            "simply learns which actions lead to the highest cumulative reward over time."
        ),
        "fallback_example": (
            "**Real-life Example: Self-Driving Cars and Video Games**\n\n"
            "Think of an AI learning to play Super Mario. At first, it moves randomly and dies (penalty). It learns that pressing "
            "'jump' when an obstacle is near helps it survive longer (reward) and collect coins (reward). By playing millions of games, "
            "it develops the perfect sequence of moves to complete the level."
        )
    },
    "Decision Trees": {
        "description": "Flowchart-like structure representing decisions and their consequences.",
        "fallback_explanation": (
            "A **Decision Tree** is a flowchart-like structure that makes decisions by splitting data based on questions.\n\n"
            "You start at the top (the **Root Node**) and ask a yes/no question (e.g., 'Is the temperature above 30°C?'). "
            "Depending on the answer, you follow the branch down to the next node, which asks another question. You repeat this "
            "until you reach a final decision or prediction (called a **Leaf Node**)."
        ),
        "fallback_example": (
            "**Real-life Example: Deciding Whether to Play Tennis**\n\n"
            "Should we play tennis outside today? Let's check a decision tree:\n"
            "1. **Is it raining?** \n"
            "   - Yes -> Don't play tennis (End).\n"
            "   - No -> Go to question 2.\n"
            "2. **Is it extremely windy?**\n"
            "   - Yes -> Don't play tennis (End).\n"
            "   - No -> Play tennis! (End).\n"
            "This simple tree lets you classify any day into 'Play' or 'Don't Play'."
        )
    },
    "Random Forest": {
        "description": "An ensemble of decision trees to improve prediction accuracy.",
        "fallback_explanation": (
            "A single decision tree can be biased or make mistakes if the data is slightly noisy (this is called overfitting). "
            "To fix this, we build a **Random Forest**!\n\n"
            "A Random Forest is an **Ensemble** method. Instead of relying on one tree, it builds a whole forest of different decision trees "
            "on random subsets of the data. When you want to make a prediction, every tree in the forest casts a 'vote'. The option "
            "with the most votes becomes the final prediction. It is a classic example of the 'wisdom of the crowd'!"
        ),
        "fallback_example": (
            "**Real-life Example: Deciding which movie to watch**\n\n"
            "Instead of asking just one friend (one Decision Tree) for a recommendation, you ask a group of 20 friends (a Forest). "
            "Each friend has their own criteria (genre preferences, favorite actors). If 15 out of 20 friends suggest you watch "
            "'Interstellar', you can feel highly confident that you will enjoy it!"
        )
    },
    "KNN": {
        "description": "K-Nearest Neighbors: classifying data points based on proximity to neighbors.",
        "fallback_explanation": (
            "**KNN (K-Nearest Neighbors)** is one of the simplest algorithms in machine learning. Its core philosophy is: "
            "'Birds of a feather flock together.'\n\n"
            "If you want to classify a new data point, you look at its closest neighbors in the dataset. The 'K' is a number "
            "you choose—for example, if K = 3, you look at the 3 nearest points. If 2 of them belong to Group A, and 1 belongs "
            "to Group B, you classify the new point as Group A (majority vote)!"
        ),
        "fallback_example": (
            "**Real-life Example: Guessing a Person's Interests**\n\n"
            "If a new person moves into a neighborhood, you can guess their political views or interests by looking at their 5 "
            "closest neighbors. If 4 of them are avid gardeners, there's a very high chance the new neighbor is also interested "
            "in gardening!"
        )
    },
    "K-Means": {
        "description": "Unsupervised clustering algorithm grouping data into K clusters.",
        "fallback_explanation": (
            "**K-Means** is a clustering algorithm used in Unsupervised Learning. Its goal is to divide data points into "
            "'K' distinct groups (clusters) based on how close they are to each other.\n\n"
            "How it works:\n"
            "1. You choose 'K' (the number of clusters you want, say K=3).\n"
            "2. The algorithm randomly picks 3 points to act as center points (called **Centroids**).\n"
            "3. It assigns every other data point to its nearest centroid.\n"
            "4. It recalculates the centers of these groups and moves the centroids there.\n"
            "5. It repeats steps 3 and 4 until the centroids stop moving!"
        ),
        "fallback_example": (
            "**Real-life Example: Sorting T-Shirts**\n\n"
            "Imagine you run a T-shirt factory and have measurements of heights and weights for 1000 customers. You want to "
            "create 3 sizes (Small, Medium, Large). K-Means (K=3) will group your customers' measurements into three clusters. "
            "The center of each cluster represents the average measurements for Small, Medium, and Large, helping you design "
            "shirts that fit the most people!"
        )
    },
    "ANN": {
        "description": "Artificial Neural Networks inspired by biological brain structures.",
        "fallback_explanation": (
            "An **Artificial Neural Network (ANN)** is an algorithm inspired by how the human brain works. "
            "It consists of interconnected nodes called **Neurons** organized in layers:\n\n"
            "1. **Input Layer**: Receives the data (like pixels of an image).\n"
            "2. **Hidden Layers**: Process the information, extracting features (like finding edges, shapes, and patterns).\n"
            "3. **Output Layer**: Gives the final prediction (like 'It is a dog!').\n\n"
            "Each connection has a **weight** (strength). During training, the network adjusts these weights until it can "
            "accurately make predictions."
        ),
        "fallback_example": (
            "**Real-life Example: Recognizing a Face**\n\n"
            "When you see a face, your eyes see light patterns (Input). The first layer of neurons detects simple lines and borders. "
            "The next layer combines lines to identify eyes, nose, and mouth. The final layer identifies the face as your friend Alex. "
            "An ANN mimics this process layer-by-layer to do image recognition, translation, or voice activation."
        )
    },
    "Model Evaluation": {
        "description": "Metrics like Accuracy, Precision, Recall, and Confusion Matrix.",
        "fallback_explanation": (
            "Once you train an ML model, how do you know it's any good? We use **Evaluation Metrics**!\n\n"
            "- **Accuracy**: Out of all predictions, how many did the model get right? (Great for balanced data).\n"
            "- **Precision**: When the model predicts 'Positive', how often is it actually correct? (Crucial when false positives are expensive, like spam detection).\n"
            "- **Recall**: Out of all actual positives, how many did the model find? (Crucial when false negatives are dangerous, like cancer diagnosis).\n"
            "- **Confusion Matrix**: A table showing correct vs. incorrect predictions for all categories."
        ),
        "fallback_example": (
            "**Real-life Example: COVID-19 Testing**\n\n"
            "Imagine testing 100 people for a virus:\n"
            "- If the test is positive, but the person is healthy, that is a **False Positive**. (High Precision minimizes this).\n"
            "- If the test is negative, but the person is actually sick, that is a **False Negative**. (High Recall minimizes this, ensuring no sick person goes untreated).\n"
            "A good evaluation system checks these metrics, rather than just looking at overall accuracy."
        )
    }
}

# --- Prompt Templates ---

def get_explanation_prompt(topic: str, tone: str) -> str:
    """
    Generates a prompt requesting a simple explanation of an ML topic.
    """
    return (
        f"Explain the Machine Learning concept: '{topic}' to a complete beginner.\n"
        f"The explanation should be in a '{tone}' tone.\n"
        "Remember to:\n"
        "- Explain it clearly in a way a middle-schooler can understand.\n"
        "- Use a creative analogy or daily-life comparison.\n"
        "- Highlight core terminology in bold.\n"
        "- Use bullet points or numbered lists to improve structure.\n"
        "- End with a single friendly, encouraging check-for-understanding question."
    )

def get_example_prompt(topic: str, tone: str) -> str:
    """
    Generates a prompt requesting a real-life example or application of an ML topic.
    """
    return (
        f"Provide a vivid, detailed, and highly relatable real-life example or application of '{topic}'.\n"
        f"The tone should be '{tone}'.\n"
        "Instructions:\n"
        "- Focus on one specific application (e.g., Netflix recommendations, self-driving cars, medical tests).\n"
        "- Walk the student through how it works step-by-step using this example.\n"
        "- Explain the inputs, what the algorithm does, and what the output is in this scenario.\n"
        "- Keep it engaging, fun, and highly visual with markdown formatting."
    )

def get_quiz_prompt(topic: str) -> str:
    """
    Generates a prompt to build a 5-question multiple choice quiz.
    It instructs the LLM to output a strict JSON format for easy parsing in python.
    """
    seed = random.randint(1000, 9999)
    return (
        f"Generate a unique and fresh multiple-choice quiz about: '{topic}' that is different from previous attempts. (Random Seed: {seed})\n"
        "The quiz must contain exactly 5 questions of varying difficulty (from easy to moderate) suitable for a beginner.\n\n"
        "You must return the quiz ONLY as a valid JSON object. Do not include markdown code block characters like ```json or any introductory text. Just raw JSON.\n\n"
        "The JSON structure must be exactly like this:\n"
        "{\n"
        "  \"questions\": [\n"
        "    {\n"
        "      \"id\": 1,\n"
        "      \"question\": \"The question text?\",\n"
        "      \"options\": [\"Option A\", \"Option B\", \"Option C\", \"Option D\"],\n"
        "      \"correct_answer\": \"Option A\",\n"
        "      \"explanation\": \"Explain why Option A is correct in a friendly, encouraging way.\"\n"
        "    },\n"
        "    ... (repeat for 5 questions with IDs 1 to 5)\n"
        "  ]\n"
        "}\n\n"
        "Ensure the questions and options are clear, accurate, and test key principles of the topic."
    )

def get_feedback_prompt(question: str, options: list, correct_answer: str, user_answer: str) -> str:
    """
    Generates a prompt to evaluate the user's answer and provide supportive feedback.
    """
    return (
        f"Evaluate the student's answer for the following question:\n"
        f"Question: {question}\n"
        f"Options: {', '.join(options)}\n"
        f"Correct Answer: {correct_answer}\n"
        f"Student's Answer: {user_answer}\n\n"
        "Please provide feedback following these rules:\n"
        "1. Start by telling them if they are correct or incorrect in a highly encouraging way.\n"
        "2. If they are correct, celebrate their achievement and briefly reinforce why they are right.\n"
        "3. If they are incorrect, do not discourage them. Validate their attempt, explain why their choice was not correct, "
        "and explain the correct answer clearly using a simple illustration or tip to remember it next time."
    )

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

def render_prompt_templates_page():
    """
    Renders the Prompt Templates page displaying five reusable prompts with titles,
    purposes, example inputs, and outputs.
    """
    st.markdown("## Prompt Engineering Templates")
    st.markdown(
        "Here are the engineering prompts used by ML Mentor to control explanation structures, "
        "quizzes, and dialogue. You can copy these to use in your own LLM applications."
    )
    
    templates = [
        {
            "id": 1,
            "title": "Template 1: Explanation Prompt",
            "purpose": "Instructs the AI to explain a machine learning concept in simple language, using a creative analogy, and ending with an interactive question.",
            "prompt": (
                "Explain the Machine Learning concept: '{topic}' to a complete beginner.\n"
                "The explanation should be in a '{tone}' tone.\n"
                "Remember to:\n"
                "- Explain it clearly in a way a middle-schooler can understand.\n"
                "- Use a creative analogy or daily-life comparison.\n"
                "- Highlight core terminology in bold.\n"
                "- Use bullet points or numbered lists to improve structure.\n"
                "- End with a single friendly, encouraging check-for-understanding question."
            ),
            "input": "topic=\"K-Means Clustering\", tone=\"Balanced\"",
            "output": (
                "Think of K-Means like sorting a pile of laundry into K separate laundry baskets without any tags! "
                "First, you guess K center spots, group clothes closest to them (like putting socks together), "
                "recalculate the middle of each group, and repeat. \n\n"
                "Key terms: **Centroids** (center points), **Clustering** (grouping). \n\n"
                "Question: If you want to sort your books into 3 genres, what is the value of K?"
            )
        },
        {
            "id": 2,
            "title": "Template 2: Real-Life Example Prompt",
            "purpose": "Asks the AI to write a step-by-step everyday application of an ML algorithm to demonstrate real-world usage.",
            "prompt": (
                "Provide a vivid, detailed, and highly relatable real-life example or application of '{topic}'.\n"
                "The tone should be '{tone}'.\n"
                "Instructions:\n"
                "- Focus on one specific application (e.g., Netflix recommendations, self-driving cars, medical tests).\n"
                "- Walk the student through how it works step-by-step using this example.\n"
                "- Explain the inputs, what the algorithm does, and what the output is in this scenario.\n"
                "- Keep it engaging, fun, and highly visual with markdown formatting."
            ),
            "input": "topic=\"Decision Trees\", tone=\"Casual & Fun\"",
            "output": (
                "**Real-life Example: Netflix choosing what to suggest next!**\n"
                "- **Input**: Have you watched a Sci-Fi movie? Yes/No. Have you rated it 5 stars? Yes/No.\n"
                "- **Algorithm Decision Node**: If Yes, split down to 'Suggest Interstellar'. If No, split to 'Suggest Friends'.\n"
                "- **Output**: The movie recommendation on your home screen!"
            )
        },
        {
            "id": 3,
            "title": "Template 3: Quiz Generation Prompt",
            "purpose": "Guides the LLM to output exactly 5 multiple choice questions in a strict JSON format for parsing in python code.",
            "prompt": (
                "Generate a multiple-choice quiz about: '{topic}'.\n"
                "The quiz must contain exactly 5 questions of varying difficulty (from easy to moderate) suitable for a beginner.\n\n"
                "You must return the quiz ONLY as a valid JSON object. Do not include markdown code block characters like ```json or any introductory text. Just raw JSON.\n\n"
                "The JSON structure must be exactly like this:\n"
                "{\n"
                "  \"questions\": [\n"
                "    {\n"
                "      \"id\": 1,\n"
                "      \"question\": \"The question text?\",\n"
                "      \"options\": [\"Option A\", \"Option B\", \"Option C\", \"Option D\"],\n"
                "      \"correct_answer\": \"Option A\",\n"
                "      \"explanation\": \"Explain why Option A is correct in a friendly, encouraging way.\"\n"
                "    },\n"
                "    ... (repeat for 5 questions)\n"
                "  ]\n"
                "}"
            ),
            "input": "topic=\"Supervised Learning\"",
            "output": (
                "{\n"
                "  \"questions\": [\n"
                "    {\n"
                "      \"id\": 1,\n"
                "      \"question\": \"What type of learning utilizes labeled data?\",\n"
                "      \"options\": [\"Supervised\", \"Unsupervised\", \"Reinforcement\", \"Manual\"],\n"
                "      \"correct_answer\": \"Supervised\",\n"
                "      \"explanation\": \"Supervised learning uses labeled training data, meaning the correct answers are provided to the model during training.\"\n"
                "    }\n"
                "  ]\n"
                "}"
            )
        },
        {
            "id": 4,
            "title": "Template 4: Feedback Prompt",
            "purpose": "Instructs the AI to evaluate a student's answer constructively, explaining corrections and validating efforts.",
            "prompt": (
                "Evaluate the student's answer for the following question:\n"
                "Question: {question}\n"
                "Options: {options}\n"
                "Correct Answer: {correct_answer}\n"
                "Student's Answer: {user_answer}\n\n"
                "Please provide feedback following these rules:\n"
                "1. Start by telling them if they are correct or incorrect in a highly encouraging way.\n"
                "2. If they are correct, celebrate their achievement and briefly reinforce why they are right.\n"
                "3. If they are incorrect, do not discourage them. Validate their attempt, explain why their choice was not correct, "
                "and explain the correct answer clearly using a simple illustration or tip to remember it next time."
            ),
            "input": "question=\"What is accuracy?\", correct_answer=\"Correct predictions / total predictions\", user_answer=\"Total incorrect predictions\"",
            "output": (
                "Good try! You actually defined the error rate, which is the opposite of accuracy. Accuracy measures the proportion of "
                "correct predictions out of all predictions made. Think of it like scoring 8 out of 10 on a spelling quiz—your accuracy is 80%! "
                "Let's review this concept and try another one, you are doing great!"
            )
        },
        {
            "id": 5,
            "title": "Template 5: Complete Learning Session Prompt",
            "purpose": "Sets up a structured multi-turn conversation dialogue between ML Mentor and a student, checking for understanding at each milestone.",
            "prompt": (
                "You are ML Mentor, an AI Learning Buddy teaching {topic} to a student.\n"
                "Walk the student through the concept step-by-step. Do not explain everything at once.\n"
                "Follow this curriculum path:\n"
                "1. Ask the student what they already know about {topic}.\n"
                "2. Explain the fundamental definition using a simple, real-life analogy.\n"
                "3. Ask a brief check-for-understanding question and wait for their response.\n"
                "4. Give constructive feedback, explain a real-world example, and ask another question.\n"
                "5. Provide a 3-question MCQ quiz to end the session.\n\n"
                "Do not dump all steps at once. Start with Step 1 and wait for their reply. Keep the tone friendly, patient, and highly motivational!"
            ),
            "input": "topic=\"Random Forest\"",
            "output": (
                "Hi! I'm ML Mentor, your AI learning buddy. Today, we are going to learn about Random Forest! Before we dive into the details, "
                "tell me: have you ever heard of this concept, or is it completely new to you?"
            )
        }
    ]
    
    # Render prompt tabs
    tab_names = [f"📄 Prompt {t['id']}" for t in templates]
    tabs = st.tabs(tab_names)
    
    for idx, tab in enumerate(tabs):
        t = templates[idx]
        with tab:
            st.markdown(f"### {t['title']}")
            
            # Purpose Card
            st.markdown(
                f"""
                <div style="background-color: #f8fafc; border-left: 4px solid #3b82f6; padding: 12px; border-radius: 6px; margin-bottom: 15px;">
                    <strong>Purpose:</strong> {t['purpose']}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("**Prompt Template:**")
            st.code(t["prompt"], language="text")

            col_in, col_out = st.columns(2)
            with col_in:
                st.markdown("**Example Input Parameters:**")
                st.code(t["input"], language="python")
            with col_out:
                st.markdown("**Example Output Response:**")
                st.code(t["output"], language="text")

    render_footer()

