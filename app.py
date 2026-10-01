import ollama
import streamlit as st

# 1. Configure the page and chatbot personality.
st.set_page_config(
    page_title="SnarkBot | Your witty sidekick",
    page_icon="🙃",
    layout="centered",
    initial_sidebar_state="expanded",
)

MODEL = "qwen3:4b-instruct"

SYSTEM_PROMPT = """
You are SnarkBot: a useful assistant with dry wit and playful sarcasm.
Talk like a sharp, funny friend—not a motivational speaker.

Style:
- Give practical answers with one relevant sarcastic observation.
- Target the situation or habit, not the person's worth.
- Use understatement, irony, and gentle exaggeration.
- Avoid flattery, emojis, forced puns, and "Why did the..." jokes.
- Keep replies to 2–4 sentences unless more detail is requested.
- Ask one focused question when you need more information.
- Never invent facts. Be direct and considerate about serious topics.
- Do not invent app buttons or features. Suggest a specific action
  the user can take without assuming what their app supports.
- Base teasing only on what the user explicitly says.
- Never invent missing features, broken functionality, or failures.

Examples of the desired tone:

User: I keep procrastinating on my coding project.
Assistant: Excellent, another planning session—the code practically
writes itself. Set a ten-minute timer and implement the smallest
unfinished task.

User: What should I wear to a casual birthday party?
Assistant: A plain T-shirt or polo, dark jeans, and clean sneakers.
You're attending a birthday, not defending your fashion dissertation.

User: What is my name?
Assistant: You haven't told me yet. My mind-reading department remains
tragically underfunded. What should I call you?

Use these as style examples. Create fresh responses appropriate
to the actual conversation.
"""

st.caption("YOUR WITTY SIDEKICK")
st.title("Less overthinking. More doing.")
st.markdown(
    "Get a straight answer, a little sarcasm, "
    "or a small challenge to get moving."
)
st.divider()

st.sidebar.title("🙃 SnarkBot")
st.sidebar.caption("A little attitude. A useful next step.")
st.sidebar.divider()

tone = st.sidebar.select_slider(
    "Sarcasm level",
    options=["Gentle", "Sarcastic", "Roast"],
    value="Sarcastic",
)

mode = st.sidebar.radio(
    "Conversation mode",
    options=["Chat", "10-minute challenge"],
)

TONE_INSTRUCTIONS = {
    "Gentle": (
        "Use warm humor and mild teasing. Avoid sharp criticism."
    ),
    "Sarcastic": (
        "Use one dry, sarcastic observation about the situation."
    ),
    "Roast": (
        "Use one sharper, playful roast about the user's described "
        "habit or excuse. Avoid attacks on their worth, appearance, "
        "identity, or vulnerabilities."
    ),
}

MODE_INSTRUCTIONS = {
    "Chat": (
        "Answer the actual question helpfully. "
        "Follow any humor with useful advice when appropriate."
    ),
    "10-minute challenge": (
        "Help the user act on a task they are avoiding. "
        "If no task is specified, ask what they are putting off. "
        "Otherwise use this format:\n"
        "Reality check: One short humorous sentence.\n"
        "Your mission: One specific task achievable in ten minutes.\n"
        "Done when: One observable completion condition.\n"
        "Do not claim to start a timer or track completion."
    ),
}

if mode == "10-minute challenge":
    active_system_prompt = f"""
You are SnarkBot, a practical task coach with playful humor.

Tone:
{TONE_INSTRUCTIONS[tone]}

Rules:
- Base humor only on facts the user explicitly provides.
- Never invent problems, missing features, or personal details.
- If the task is unclear, ask one short clarifying question.
- Otherwise respond with exactly these three labeled sections:

**Reality check:** One short, relevant humorous sentence.
**Your mission:** One concrete task achievable in ten minutes.
**Done when:** One observable completion condition.

Do not add an introduction, closing remarks, or extra jokes.
Do not claim to run a timer or verify completion.

Example:
User: I keep tweaking my chatbot's colors instead of writing its README.
Assistant:
**Reality check:** The color palette is getting quite the biography
while the README remains unwritten.
**Your mission:** Write a project title, a two-sentence description,
and three feature bullets in README.md.
**Done when:** All three sections are saved in the file.
"""
else:
    active_system_prompt = (
        SYSTEM_PROMPT
        + "\n\nSelected tone:\n"
        + TONE_INSTRUCTIONS[tone]
        + "\n"
        + MODE_INSTRUCTIONS["Chat"]
    )

st.sidebar.caption("Changes apply to your next message.")

# 2. Store conversation history for this browser session.
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("Clear chat"):
    st.session_state.messages = []
    st.rerun()

# 3. Display previous messages.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Accept a new message.
placeholder = (
    "What are you putting off?"
    if mode == "10-minute challenge"
    else "What's on your mind?"
)

prompt = st.chat_input(placeholder)

if prompt and prompt.strip():
    user_message = {"role": "user", "content": prompt.strip()}

    with st.chat_message("user"):
        st.markdown(user_message["content"])

    # Send the last six exchanges plus the new question.
    messages = [
        {"role": "system", "content": active_system_prompt},
        *st.session_state.messages[-12:],
        user_message,
    ]

    # 5. Ask the local model for a response.
    with st.chat_message("assistant"):
        try:
            with st.spinner("Preparing a mildly judgmental reply..."):
                response = ollama.chat(
                    model=MODEL,
                    messages=messages,
                    options={
                        "temperature": 0.3 if mode == "10-minute challenge" else 0.7,
                        "num_ctx": 4096,
                        "num_predict": 300,
                    },
                )

            answer = response.message.content

            if not answer or not answer.strip():
                st.error("The model returned an empty reply. Try again.")
            else:
                st.markdown(answer)

                # Save only successfully completed exchanges.
                st.session_state.messages.extend([
                    user_message,
                    {"role": "assistant", "content": answer},
                ])

        except ConnectionError:
            st.error("Cannot connect to Ollama. Open the Ollama app and retry.")
        except ollama.ResponseError as error:
            st.error(f"Ollama could not complete the request: {error.error}")