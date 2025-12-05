TalentScout AI – Streamlit Hiring Assistant

TalentScout AI is an interactive, AI-powered technical interview assistant built with Streamlit.
It conducts structured hiring conversations, collects candidate details, asks tech-stack-specific questions, and tracks interview progress — all through an elegant animated UI.

This project integrates a locally hosted or remote OpenAI-compatible API (e.g., Ollama) to generate conversational responses.

⭐ Features
🎙️ Intelligent Interview Flow

Greets the candidate naturally

Collects essential job-application details:
name, contact info, location, experience, desired role, tech stack

Generates relevant technical questions based on the candidate’s technologies

Tracks progress with real-time metadata updates

🧠 Conversation Logic

Uses a custom system prompt tailored for a hiring assistant

Automatically detects exit intent (e.g., “exit”, “bye”, “done”)

Masks user PII (emails + phone numbers) when sending to the model

Includes conversation caching for faster responses

⚙️ Technical Architecture

streamlit_app.py

Main UI

Queue-based input handling

Conversation management

Sidebar options, session control, and progress tracker

functions.py

Message sanitization

PII masking

Exit intent detection

Cached API calls

Input queue system

styles.py

Full CSS theme

Animated gradient background

Floating nebula-like orbs

Custom message bubbles

Styled sidebar, inputs, buttons, and metrics

prompt.py

Defines the entire behavior of TalentScout AI

Includes internal metadata tracking structure

🚀 Getting Started
1. Install Dependencies
pip install streamlit openai

2. Run Your LLM Backend

TalentScout uses an OpenAI-compatible API endpoint.

Example (Ollama):

ollama serve
ollama run llama3.1

3. Launch the App
streamlit run streamlit_app.py

🔧 Configuration

The sidebar allows you to configure:

API Base URL
Default: http://localhost:11434/v1

Model Selection
Options (as defined in the app):
llama3.1, llama3, mistral, codellama

🛡️ Data Handling

Emails and phone numbers are masked before being sent to the LLM

No data is persisted between sessions

A Delete My Data button fully wipes session state

🎨 UI / UX Highlights

The UI includes:

Animated gradient background

Floating glowing orbs for depth

Glassmorphism-style message bubbles

Sidebar progress indicators

Custom button and input styling

All styling is handled in styles.py.

📁 Project Structure
/project-root
│
├── streamlit_app.py     # Main application
├── functions.py         # Utilities, caching, queues, PII masking
├── styles.py            # Full CSS theme + animations
├── prompt.py            # System instructions + metadata rules
├── logo.png             # Optional logo used in header + sidebar
└── README.md            # (You are here)

🧩 How Metadata Works

Every AI response ends with:

METADATA: {
  "name": bool,
  "contact": bool,
  "location": bool,
  "experience": bool,
  "position": bool,
  "tech_stack": bool,
  "questions": bool
}


The UI parses this silently and updates progress indicators.

This is not shown to the user — it's internal only.

📜 License

This project has no license declared by the author; add one if needed.