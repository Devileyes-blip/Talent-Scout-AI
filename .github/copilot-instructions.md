<!-- .github/copilot-instructions.md -->
# GitHub Copilot / AI Agent Instructions for this repo

Purpose: help AI coding assistants (Copilot-style agents) be immediately productive editing, running, and extending this project.

- **Quick summary:** This repository contains a Streamlit-based AI hiring assistant UI in `scripts/streamlit_app.py`, prompt text in `scripts/prompt.py`, and a tiny OpenAI-wrapper in `scripts/functions.py`. There is also a `package.json` (likely leftover/front-end) — prefer working on `scripts/` for Python/Streamlit tasks.

- **Run the app locally (PowerShell)**:

```
# activate venv (if present)
.\venv\Scripts\Activate.ps1
# install minimal deps (if not already)
pip install streamlit openai
# run the UI
streamlit run scripts/streamlit_app.py
```

- **Where the AI prompt lives:** `scripts/prompt.py` exports a single `instruction` string. This is used as the system message and encodes strict behavior, constraints, and style for the assistant — preserve intent when modifying.

- **Core runtime pieces:**
  - `scripts/streamlit_app.py`: UI, session management, CSS, and user interactions. Key session_state keys: `messages`, `conversation_history`, `initialized`, `conversation_ended`, `collected_info`.
  - `scripts/functions.py`: wrapper functions used by the UI: `completion_func(client, message, model_name)`, `get_initial_greeting_prompt()`, `get_exit_prompt()`, `is_exit_intent(user_input)`.
  - The app creates an `OpenAI` client via `get_client(base_url)` and expects an API Base URL (default `http://localhost:11434/v1`) and model names like `llama3.1`, `llama3`, `mistral`, `codellama`.

- **Important integration notes / gotchas (must-read before editing):**
  - Several files in `scripts/` currently include stray Markdown code fences (e.g. leading/trailing ```python and closing ``` ) — these will break Python execution. Remove those fences if you run or edit the files.
  - The OpenAI client is initialized with `api_key="LAMBA"` in the code — this is a placeholder. The UI exposes `API Base URL` as a text input; to test with a hosted OpenAI-compatible endpoint or Ollama, set that field in the sidebar. For local testing consider replacing the hardcoded API key with a proper env var (e.g., `OPENAI_API_KEY`) or edit `get_client`.
  - `completion_func` calls `client.chat.completions.create(...)` which assumes the installed OpenAI SDK/compatibility with your backend. Ensure your client and backend support that method signature.

- **Conventions & patterns used in this repo:**
  - UI and presentation logic live in `streamlit_app.py`; prompt text and behavior rules live in `prompt.py`; minimal API wrapper and small helpers live in `functions.py`. Keep that separation when refactoring.
  - Session state drives conversation flow; `conversation_history` is the canonical message list sent to the model. UI-only messages are kept in `messages` for display.
  - Simple heuristics are used to populate `collected_info` (based on message count). If you need to add structured extraction, update both `is_exit_intent` and the heuristics in `streamlit_app.py`.

- **When editing prompts or behavior:**
  - Preserve the high-level constraints in `scripts/prompt.py` (what to collect, what to refuse, style rules). If you need to change them, explain why in the PR and show before/after prompt snippets.
  - Use short, testable edits to the prompt. Prefer small iterations: change prompt -> manual local run -> validate conversations.

- **Testing & debugging tips:**
  - Run the Streamlit app and use the sidebar `API Base URL` + model selector to iterate quickly.
  - If you see failures calling the model, confirm:
    - the `base_url` is correct, and
    - the client library version matches the server expectations for `.chat.completions.create`.
  - Check the console where Streamlit runs for tracebacks; syntax errors are often caused by the stray code fences noted above.

- **Files to reference when making changes:**
  - `scripts/streamlit_app.py` — main UI and session logic
  - `scripts/prompt.py` — system instruction string (behavior + constraints)
  - `scripts/functions.py` — completions wrapper and helpers
  - `package.json` — appears unrelated to the Streamlit app; do not change unless you know a front-end Next.js app depends on it.

If anything in these notes is unclear or you want me to expand examples (e.g., show exact code edits to remove the triple-backticks or to read `OPENAI_API_KEY` from env), tell me which part and I will update the instructions.
