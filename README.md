# 🛠️ AI Productivity Assistant

An AI-powered productivity toolkit built with Google Gemini. Comes in two versions:
- A **Jupyter notebook** (`project5_productivity_assistant.ipynb`)
- A **Streamlit web app** (`app.py`) with a tab for each tool

Uses Google's new `google-genai` SDK (the old `google-generativeai` package is deprecated).

## Features

8 productivity tools, all in one place:

| Tool | What it does |
|---|---|
| 📝 Meeting Notes | Summarizes raw meeting notes into bullet points |
| ✅ Action Items | Extracts Task / Owner / Deadline into a table |
| ✉️ Email Rewriter | Rewrites an email in a chosen tone |
| 📊 Presentation Outline | Builds a slide-by-slide outline |
| 💼 LinkedIn Post | Drafts a LinkedIn post with hashtags |
| 💡 Brainstorm | Generates a list of creative ideas |
| 🌍 Translate | Translates text into any language |
| 📚 Study Notes | Turns content into organized study notes |

## Setup

```bash
pip install google-genai streamlit
```

Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey), then either:

```bash
export GEMINI_API_KEY="your-key-here"
```

or just paste it in when prompted.

## Run it

**Notebook:**
Open `project5_productivity_assistant.ipynb` in Jupyter and run the setup cells, then try any function:

```python
print(summarize_meeting_notes("Sarah will lead the redesign. Launch targeted for October."))
```

**Streamlit app:**
```bash
streamlit run app.py
```
Enter your API key in the sidebar, pick a model, then use the tabs at the top to switch between tools.

## Notes

- Default model: `gemini-3.6-flash` (also supports `gemini-3.5-flash` and `gemini-3.5-flash-lite`)
- Never commit your API key to GitHub
