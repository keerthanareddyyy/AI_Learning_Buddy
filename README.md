# 🤖 ML Mentor: AI Learning Buddy for Machine Learning

This project is a complete, interactive, and modern AI-powered tutoring application designed to teach Machine Learning fundamentals to beginners. It has been developed as a Capstone Project for the Infosys Springboard AI EMPOW(H)ER Week 8 Program.

The application is built using **Python** and **Streamlit**, with **Google Gemini API** as the AI engine — as required by the Infosys Springboard Week 8 Capstone. An offline learning mode is available as a fallback for demonstration purposes when an API key is unavailable.

---

## 🎯 Project Overview & Objectives

The primary objective of ML Mentor is to make Machine Learning Fundamentals accessible, engaging, and fear-free for absolute beginners.
- Explain complex concepts in simple language using a Socratic teaching style.
- Connect mathematical abstractions to everyday real-life examples.
- Test retention with interactive quizzes and diagnose strengths and weaknesses.
- Encourage students through constructive feedback.
- Provide metacognitive reinforcement through systematic reflection logs and analytics.

---

## 🤖 AI Integration — Google Gemini API

This project integrates the **Google Gemini API** (`gemini-1.5-flash`) as the primary AI engine:

| Feature | Powered By |
|---|---|
| Concept Explanations | Google Gemini API |
| Real-life Analogies | Google Gemini API |
| Quiz Generation | Google Gemini API |
| Live Chat (Chat Room) | Google Gemini API |
| Feedback Generation | Google Gemini API |

**Offline Learning Mode** is available as a fallback when no API key is provided. All lessons, quizzes, and examples fall back to pre-built educational content so the application never crashes.

---

## 🧭 Page Navigation & Features

### Core Capstone Pages
1. 🏠 **Home Page**: Introduces ML Mentor, lists the learning topics, and displays a start button.
2. 📚 **Learning Hub**: Learn 11 core concepts using the Explanation Generator and Real-Life Example Generator, both powered by Gemini.
3. 🤖 **AI Buddy Persona**: Profiles ML Mentor's personality traits, teaching style, target audience, and strengths.
4. 📋 **Prompt Templates**: Displays the five system prompt templates with input/output cases in copyable blocks.
5. 💬 **Sample Conversation**: A pre-generated 15-turn educational dialogue between ML Mentor and a student.
6. ❓ **Quiz**: Provides a 5-question MCQ test on any topic with immediate grading and explanations.
7. 📝 **Reflection Report**: Features an academic Reflection Paper with a TXT file export option.

### Advanced Features (Optional Enhancements)
- **Chat Room**: A live, multi-turn chat portal using Google Gemini for responses.
- **Google Gemini API Configuration**: A settings panel to enter the Gemini API key securely, with connection status indicator.
- **Reflection Diary**: An interactive form to log daily study summaries and confidence ratings.
- **Progress Analytics**: A Plotly dashboard visualizing syllabus completion rates and quiz score histories.

---

## 🎓 Capstone Week 8 Rubric Mapping

| Week 8 Capstone Requirement | Implemented Feature | Module |
|:---|:---|:---|
| **Project Title & Topic** | ML Mentor - Machine Learning Fundamentals | `app.py` |
| **Tutor Description & Start Button** | Home page introduction and navigation trigger | `app.py` |
| **Explain ML Concepts Simply** | Learning Hub with customizable tones (Gemini-powered) | `app.py`, `prompts.py` |
| **Real-life Examples & Analogies** | Real-world Analogy generator (Gemini-powered) | `app.py`, `prompts.py` |
| **Generate Quizzes** | Quiz page with 5 MCQ questions per topic (Gemini-powered) | `quiz.py` |
| **Evaluate Answers & Feedback** | Score metric, colour-coded feedback cards, explanations | `quiz.py` |
| **Encouraging Tutor Persona Page** | Profile with personality, teaching style, and role | `persona.py` |
| **System Prompt Templates** | 5 prompt templates with arguments and example responses | `prompts.py` |
| **Sample Dialogue Log** | Pre-generated 15-turn educational chat transcript | `conversation.py` |
| **Professional Reflection Report** | 350-word paper with .txt download option | `reflection.py` |
| **Google Gemini API Integration** | All AI features call `gemini-1.5-flash` via `google-generativeai` | `utils.py` |

---

## 🛠️ Technologies Used

- **Core Language**: Python
- **Frontend Framework**: Streamlit
- **AI Engine**: Google Gemini API (`google-generativeai`, model: `gemini-1.5-flash`)
- **Data Analytics & Visuals**: Plotly Express, Pandas
- **Styling**: HTML5/CSS3 (Glassmorphic card containers, HSL colors, Google Fonts)
- **Environment Management**: python-dotenv

---

## 📁 Project Structure

```text
AI_Learning_Buddy/
│
├── app.py              # Main Streamlit orchestration and page layout router
├── prompts.py          # LLM prompt templates, render_prompt_templates_page, fallback data
├── persona.py          # AI Tutor configuration, render_persona_page, sidebar components
├── quiz.py             # MCQ Quiz rendering engine, state managers, and question bank
├── conversation.py     # Live chat room, sample conversation transcripts, offline responses
├── reflection.py       # Reflection report, diary manager, and Plotly analytics dashboard
├── utils.py            # CSS themes, Google Gemini API wrapper, state initialization
├── requirements.txt    # Python package dependencies
└── README.md           # Documentation guide (this file)
```

---

## ⚙️ How to Install and Run Locally

### 1. Navigate to the Directory
```bash
cd AI_Learning_Buddy
```

### 2. Set Up a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Set Your Gemini API Key
```bash
echo "GEMINI_API_KEY=your_key_here" > .env
```
Or enter it directly in the app via the **Advanced Features → Google Gemini API Configuration** page.

### 5. Start the Application
```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**.

> **No API key?** The app automatically runs in **Offline Learning Mode** using pre-built educational content. All pages remain fully functional.
