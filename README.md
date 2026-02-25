import datetime
import textwrap
import time
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor

import streamlit as st
import ollama  # NEW: Replacing snowflake-cortex
from htbuilder import div, styles
from htbuilder.units import rem

# -----------------------------------------------------------------------------
# Configuration

MODEL = "gemma"  # Make sure you've run 'ollama pull gemma'
executor = ThreadPoolExecutor(max_workers=5)

HISTORY_LENGTH = 5
SUMMARIZE_OLD_HISTORY = True
MIN_TIME_BETWEEN_REQUESTS = datetime.timedelta(seconds=1)

DEBUG_MODE = st.query_params.get("debug", "false").lower() == "true"

INSTRUCTIONS = textwrap.dedent("""
    - You are a helpful AI chat assistant running locally.
    - You focus on answering questions about Streamlit and general Python.
    - Use markdown (headers, code blocks, bullet points).
    - Assume the user is a newbie.
    - Provide examples.
""")

SUGGESTIONS = {
    ":blue[:material/local_library:] What is Streamlit?": (
        "What is Streamlit, what is it great at, and what can I do with it?"
    ),
    ":green[:material/database:] Help me understand session state": (
        "Help me understand session state. What is it for? "
    ),
    ":orange[:material/multiline_chart:] Interactive charts": (
        "How do I make a chart where, when I click, another chart updates?"
    ),
}

# -----------------------------------------------------------------------------
# Helper Functions (Refactored for Ollama)

def build_prompt(**kwargs):
    """Same as your original: builds a prompt string with tags."""
    prompt = []
    for name, contents in kwargs.items():
        if contents:
            prompt.append(f"<{name}>\n{contents}\n</{name}>")
    return "\n".join(prompt)

def history_to_text(chat_history):
    return "\n".join(f"[{h['role']}]: {h['content']}" for h in chat_history)

# Task containers to keep the original parallel logic structure
TaskInfo = namedtuple("TaskInfo", ["name", "function", "args"])
TaskResult = namedtuple("TaskResult", ["name", "result"])

def generate_chat_summary(messages):
    """Summarizes chat history using Ollama."""
    prompt = build_prompt(
        instructions="Summarize this conversation as concisely as possible.",
        conversation=history_to_text(messages),
    )
    # Simple non-streaming call for summary
    response = ollama.chat(model=MODEL, messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

def search_local_docs(query):
    """
    Placeholder: In the original, this was Snowflake Search.
    You can replace this with a local file read or simple string.
    """
    return "Streamlit documentation: st.chat_message is used to display chat bubbles."

def build_question_prompt(question):
    """Parallel processing for context gathering (kept from original)."""
    old_history = st.session_state.messages[:-HISTORY_LENGTH]
    recent_history = st.session_state.messages[-HISTORY_LENGTH:]
    recent_history_str = history_to_text(recent_history) if recent_history else None

    task_infos = []

    if SUMMARIZE_OLD_HISTORY and old_history:
        task_infos.append(TaskInfo("old_summary", generate_chat_summary, (old_history,)))

    # Kept parallel search structure even if it's local
    task_infos.append(TaskInfo("local_docs", search_local_docs, (question,)))

    results = executor.map(
        lambda t: TaskResult(name=t.name, result=t.function(*t.args)),
        task_infos,
    )

    context = {res.name: res.result for res in results}

    return build_prompt(
        instructions=INSTRUCTIONS,
        **context,
        recent_messages=recent_history_str,
        question=question,
    )

def get_response(prompt):
    """Generator for streaming Ollama responses."""
    stream = ollama.chat(
        model=MODEL,
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )
    for chunk in stream:
        yield chunk['message']['content']

def show_feedback_controls(message_index):
    st.write("")
    with st.popover("How did I do?"):
        with st.form(key=f"feedback-{message_index}", border=False):
            st.feedback(options="stars")
            st.text_area("Details (optional)")
            st.form_submit_button("Send feedback")

# -----------------------------------------------------------------------------
# UI Rendering (Full Original UI)

st.html(div(style=styles(font_size=rem(5), line_height=1))["❉"])

title_row = st.container(horizontal=True, vertical_alignment="bottom")
with title_row:
    st.title("Streamlit AI assistant (Gemma)", anchor=False, width="stretch")

# Initial question logic
user_just_asked_initial = "initial_question" in st.session_state and st.session_state.initial_question
user_just_clicked_sugg = "selected_suggestion" in st.session_state and st.session_state.selected_suggestion
user_first_interaction = user_just_asked_initial or user_just_clicked_sugg
has_history = "messages" in st.session_state and len(st.session_state.messages) > 0

if not user_first_interaction and not has_history:
    st.session_state.messages = []
    with st.container():
        st.chat_input("Ask a question...", key="initial_question")
        st.pills(
            label="Examples",
            options=SUGGESTIONS.keys(),
            key="selected_suggestion",
            label_visibility="collapsed",
        )
    st.stop()

# Chat logic
user_message = st.chat_input("Ask a follow-up...")
if not user_message:
    if user_just_asked_initial: user_message = st.session_state.initial_question
    if user_just_clicked_sugg: user_message = SUGGESTIONS[st.session_state.selected_suggestion]

with title_row:
    if st.button("Restart", icon=":material/refresh:"):
        st.session_state.messages = []
        st.session_state.initial_question = None
        st.session_state.selected_suggestion = None
        st.rerun()

if "prev_ts" not in st.session_state:
    st.session_state.prev_ts = datetime.datetime.fromtimestamp(0)

# Render History
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        if message["role"] == "assistant": st.container() # Ghost bug fix
        st.markdown(message["content"])
        if message["role"] == "assistant": show_feedback_controls(i)

# Process New Message
if user_message:
    user_message = user_message.replace("$", r"\$")
    with st.chat_message("user"):
        st.text(user_message)

    with st.chat_message("assistant"):
        # Rate limit
        now = datetime.datetime.now()
        diff = now - st.session_state.prev_ts
        if diff < MIN_TIME_BETWEEN_REQUESTS:
            time.sleep((MIN_TIME_BETWEEN_REQUESTS - diff).total_seconds())
        st.session_state.prev_ts = now

        # Compute Prompt (with Original Spinners)
        with st.spinner("Researching..."):
            full_prompt = build_question_prompt(user_message)

        with st.spinner("Thinking..."):
            response_gen = get_response(full_prompt)
            with st.container():
                response = st.write_stream(response_gen)
                st.session_state.messages.append({"role": "user", "content": user_message})
                st.session_state.messages.append({"role": "assistant", "content": response})
                show_feedback_controls(len(st.session_state.messages) - 1)
