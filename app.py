import os
import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(
    page_title="AI Code Assistant",
    page_icon="💻"
)

client = InferenceClient(token=os.getenv("HF_TOKEN"))

st.title("💻 AI Code Assistant")
st.write("Generate, explain, debug, and improve code with the help of Generative AI.")

st.subheader("📝 Code Assistant")

language = st.selectbox(
    "Select Programming Language",
    ["Python", "Java", "C", "C++", "JavaScript", "SQL"]
)

task = st.selectbox(
    "What do you want the AI to do?",
    ["Generate Code", "Explain Code", "Debug Code", "Improve Code"]
)

user_input = st.text_area(
    "Enter your question or code",
    placeholder="Example: Write a Python program to check whether a number is prime."
)

# Store conversation
if "code_context" not in st.session_state:
    st.session_state.code_context = []

# Store follow-up answer separately
if "follow_up_answer" not in st.session_state:
    st.session_state.follow_up_answer = ""

# Generate first response
if st.button("✨ Ask AI"):

    if not user_input:
        st.warning("Please enter your question or code.")

    else:

        prompt = f"""
You are an AI Code Assistant.

Programming Language: {language}
Task: {task}

User Input:
{user_input}

Provide a clear and useful response.

If generating code, provide working and readable code.
If explaining code, explain it in simple steps.
If debugging code, identify the problem and provide corrected code.
If improving code, explain the important improvements.

Do not invent information.
"""

        with st.spinner("AI is working on your request..."):

            response = client.chat_completion(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful AI Code Assistant. "
                            "Provide accurate, readable and beginner-friendly "
                            "programming assistance."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.7
            )

            answer = response.choices[0].message.content

        st.session_state.code_context = [
            {
                "role": "user",
                "content": prompt
            },
            {
                "role": "assistant",
                "content": answer
            }
        ]

        st.session_state.follow_up_answer = ""

        st.subheader("🤖 AI Response")
        st.write(answer)


# Show previous follow-up answer
if st.session_state.follow_up_answer:

    st.divider()
    st.subheader("🤖 Follow-up Response")
    st.write(st.session_state.follow_up_answer)


# Follow-up section
if st.session_state.code_context:

    st.divider()
    st.subheader("💬 Continue with Your Code")

    follow_up = st.text_input(
        "Give a follow-up instruction",
        placeholder="Example: Explain this code line by line.",
        key="follow_up_input"
    )

    if st.button("✨ Ask Follow-up"):

        if not follow_up:
            st.warning("Please enter a follow-up instruction.")

        else:

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful AI Code Assistant. "
                        "Use the previous programming conversation to answer "
                        "the follow-up question. Keep the original programming "
                        "language and context."
                    )
                }
            ]

            messages.extend(st.session_state.code_context)

            messages.append(
                {
                    "role": "user",
                    "content": follow_up
                }
            )

            with st.spinner("AI is processing your follow-up..."):

                response = client.chat_completion(
                    model="openai/gpt-oss-120b",
                    messages=messages,
                    max_tokens=800,
                    temperature=0.7
                )

                follow_up_answer = response.choices[0].message.content

            st.session_state.code_context.append(
                {
                    "role": "user",
                    "content": follow_up
                }
            )

            st.session_state.code_context.append(
                {
                    "role": "assistant",
                    "content": follow_up_answer
                }
            )

            st.session_state.follow_up_answer = follow_up_answer

            st.rerun()