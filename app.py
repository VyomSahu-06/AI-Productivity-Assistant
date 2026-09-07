"""
Project 5 - AI Productivity Assistant
---------------------------------------
A multi-feature productivity app built with Streamlit + Google's current Gen AI SDK.

IMPORTANT: The old "google-generativeai" package is deprecated (support
ended Nov 30, 2025). This version uses the new unified SDK: "google-genai".

Features (from the project brief):
- Summarize meeting notes
- Generate action items
- Rewrite emails
- Create presentation outlines
- Generate LinkedIn posts
- Brainstorm ideas
- Translate text
- Create study notes

Setup:
1. pip install -r requirements.txt
2. Get a free Gemini API key: https://aistudio.google.com/app/apikey
3. Run: streamlit run app.py
4. Paste your API key in the sidebar (or set GEMINI_API_KEY as an env var)
"""

import os
import streamlit as st
from google import genai

st.set_page_config(page_title="AI Productivity Assistant", page_icon="🧰", layout="wide")

# -----------------------------
# Sidebar: API key + model settings
# -----------------------------
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input(
        "Gemini API Key",
        value=os.environ.get("GEMINI_API_KEY", ""),
        type="password",
        help="Get a free key at https://aistudio.google.com/app/apikey",
    )
    model_name = st.selectbox(
        "Model",
        ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-3.5-flash-lite"],
        index=0,
    )
    st.markdown("---")
    st.caption(
        "Tip: This is where you'd plug in extension ideas like Otter AI "
        "(meeting transcription), Gamma/Canva AI (slide visuals), or n8n "
        "(auto-send summaries) as taught earlier in the course."
    )

st.title("🧰 AI Productivity Assistant")
st.caption("One assistant, many productivity tools — all powered by Gemini.")

if not api_key:
    st.warning("👈 Please enter your Gemini API key in the sidebar to use the tools.")
    st.stop()

# Create (or reuse) a client for this API key.
# Cached in session_state so it survives Streamlit reruns instead of being
# rebuilt on every button click.
if st.session_state.get("client_key") != api_key:
    st.session_state.client = genai.Client(api_key=api_key)
    st.session_state.client_key = api_key
client = st.session_state.client


def generate(prompt: str) -> str:
    """Send a prompt to Gemini and return the text response."""
    response = client.models.generate_content(model=model_name, contents=prompt)
    return response.text


# -----------------------------
# Tabs = the different productivity tools
# -----------------------------
tabs = st.tabs(
    [
        "📝 Meeting Notes",
        "✅ Action Items",
        "✉️ Email Rewriter",
        "📊 Presentation Outline",
        "💼 LinkedIn Post",
        "💡 Brainstorm",
        "🌍 Translate",
        "📚 Study Notes",
    ]
)

# 1. Summarize meeting notes
with tabs[0]:
    st.subheader("Summarize Meeting Notes")
    notes = st.text_area("Paste your raw meeting notes:", height=200, key="notes_input")
    if st.button("Summarize", key="summarize_btn"):
        if notes.strip():
            with st.spinner("Summarizing..."):
                prompt = f"Summarize the following meeting notes into clear, concise bullet points:\n\n{notes}"
                try:
                    st.markdown(generate(prompt))
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
        else:
            st.info("Paste some notes first.")

# 2. Generate action items
with tabs[1]:
    st.subheader("Generate Action Items")
    notes2 = st.text_area("Paste meeting notes or a discussion summary:", height=200, key="action_input")
    if st.button("Generate Action Items", key="action_btn"):
        if notes2.strip():
            with st.spinner("Extracting action items..."):
                prompt = (
                    "Extract clear action items from the text below. For each item, "
                    "include: Task, Owner (if mentioned, else 'Unassigned'), and Deadline "
                    "(if mentioned, else 'Not specified'). Format as a table.\n\n" + notes2
                )
                try:
                    st.markdown(generate(prompt))
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
        else:
            st.info("Paste some notes first.")

# 3. Rewrite emails
with tabs[2]:
    st.subheader("Rewrite an Email")
    email_text = st.text_area("Paste the email you want to rewrite:", height=180, key="email_input")
    tone = st.selectbox("Tone", ["Professional", "Friendly", "Concise", "Persuasive", "Apologetic"])
    if st.button("Rewrite Email", key="email_btn"):
        if email_text.strip():
            with st.spinner("Rewriting..."):
                prompt = f"Rewrite the following email in a {tone.lower()} tone. Keep the core message intact:\n\n{email_text}"
                try:
                    st.markdown(generate(prompt))
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
        else:
            st.info("Paste an email first.")

# 4. Create presentation outlines
with tabs[3]:
    st.subheader("Create a Presentation Outline")
    topic = st.text_input("Presentation topic:", key="pres_topic")
    slides = st.slider("Number of slides", 3, 20, 8)
    if st.button("Generate Outline", key="pres_btn"):
        if topic.strip():
            with st.spinner("Building outline..."):
                prompt = (
                    f"Create a {slides}-slide presentation outline on '{topic}'. "
                    "For each slide, give a title and 2-4 bullet points of content."
                )
                try:
                    st.markdown(generate(prompt))
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
        else:
            st.info("Enter a topic first.")

# 5. Generate LinkedIn posts
with tabs[4]:
    st.subheader("Generate a LinkedIn Post")
    li_topic = st.text_input("What's the post about?", key="li_topic")
    li_tone = st.selectbox("Tone", ["Professional", "Inspirational", "Casual", "Thought Leadership"], key="li_tone")
    if st.button("Generate Post", key="li_btn"):
        if li_topic.strip():
            with st.spinner("Writing post..."):
                prompt = (
                    f"You are a professional LinkedIn content writer. Write an engaging "
                    f"LinkedIn post in a {li_tone.lower()} tone about: {li_topic}. "
                    "Include relevant hashtags at the end."
                )
                try:
                    st.markdown(generate(prompt))
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
        else:
            st.info("Enter a topic first.")

# 6. Brainstorm ideas
with tabs[5]:
    st.subheader("Brainstorm Ideas")
    brainstorm_topic = st.text_input("What do you need ideas for?", key="brainstorm_topic")
    num_ideas = st.slider("Number of ideas", 3, 15, 5)
    if st.button("Brainstorm", key="brainstorm_btn"):
        if brainstorm_topic.strip():
            with st.spinner("Generating ideas..."):
                prompt = f"Brainstorm {num_ideas} creative, distinct ideas for: {brainstorm_topic}. Number them."
                try:
                    st.markdown(generate(prompt))
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
        else:
            st.info("Enter a topic first.")

# 7. Translate text
with tabs[6]:
    st.subheader("Translate Text")
    to_translate = st.text_area("Text to translate:", height=150, key="translate_input")
    target_lang = st.text_input("Target language (e.g., Spanish, Hindi, French):", key="target_lang")
    if st.button("Translate", key="translate_btn"):
        if to_translate.strip() and target_lang.strip():
            with st.spinner("Translating..."):
                prompt = f"Translate the following text into {target_lang}. Only return the translation:\n\n{to_translate}"
                try:
                    st.markdown(generate(prompt))
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
        else:
            st.info("Enter text and a target language.")

# 8. Create study notes
with tabs[7]:
    st.subheader("Create Study Notes")
    study_topic = st.text_area("Paste content or enter a topic to study:", height=180, key="study_input")
    if st.button("Generate Study Notes", key="study_btn"):
        if study_topic.strip():
            with st.spinner("Creating notes..."):
                prompt = (
                    "Turn the following content/topic into clear, well-organized study notes "
                    "with headings, bullet points, and a short summary at the end:\n\n" + study_topic
                )
                try:
                    st.markdown(generate(prompt))
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
        else:
            st.info("Enter a topic or content first.")