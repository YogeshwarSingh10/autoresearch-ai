from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from agents.planner_agent import planner_agent
from agents.retriever_agent import retriever_agent
from agents.executor_agent import executor_agent
from agents.critic_agent import critic_agent
from memory.memory_manager import MemoryManager

st.set_page_config(
    page_title="AutoResearch AI",
    page_icon="assets/logo.png",
    layout="wide"
)

# ---------------------------
# Session State
# ---------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []

if "memory" not in st.session_state:
    st.session_state.memory = MemoryManager()

# ---------------------------
# Sidebar
# ---------------------------

with st.sidebar:

    col1, col2 = st.columns([1,3])
    with col1:
        st.image("assets/logo.png", width=60)
    with col2:
        st.markdown("### AutoResearch AI")

    if st.button("➕ New Research"):
        st.session_state.messages = []

    st.markdown("---")
    st.subheader("Previous Topics")

    if st.session_state.history:
        for h in reversed(st.session_state.history):
            st.write("•", h)
    else:
        st.caption("No previous topics yet")

# ---------------------------
# Main Page
# ---------------------------

# and for the main page title section
col1, col2 = st.columns([1,10], vertical_alignment="center")

with col1:
    st.image("assets/logo.png", width=70)

with col2:
    st.title("AutoResearch AI")
    st.caption("Multi-Agent Research Assistant")


# ---------------------------
# Show chat history
# ---------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ---------------------------
# Chat input
# ---------------------------

topic = st.chat_input("Enter a research topic...")

if topic:

    st.session_state.history.append(topic)

    # Show user message
    st.session_state.messages.append({"role": "user", "content": topic})

    with st.chat_message("user"):
        st.markdown(topic)

    memory = st.session_state.memory

    # Assistant message container
    with st.chat_message("assistant"):

        status = st.status("Running research agents...", expanded=True)

        # ---------------------------
        # Planner
        # ---------------------------
        status.write("📋 Planning research tasks...")
        plan = planner_agent(topic)

        # ---------------------------
        # Retriever
        # ---------------------------
        status.write("📚 Retrieving relevant papers...")
        papers = retriever_agent(plan, memory)

        # ---------------------------
        # Executor
        # ---------------------------
        status.write("🔎 Analyzing papers...")
        analysis = executor_agent(papers, memory)

        # ---------------------------
        # Critic
        # ---------------------------
        status.write("📝 Generating final research report...")
        final_report = critic_agent(analysis)

        status.update(label="✅ Research complete", state="complete")

        # ---------------------------
        # Display report
        # ---------------------------

        st.markdown(final_report)

        st.download_button(
            label="⬇ Download Report",
            data=final_report,
            file_name="research_report.md",
            mime="text/markdown"
        )

        # ---------------------------
        # Papers section
        # ---------------------------

        with st.expander("📚 Sources"):
            if papers:
                for paper in papers:
                    st.markdown(f"**{paper.get('title','')}**")
                    st.write(paper.get("summary", "")[:300] + "...")
                    st.link_button("Open Paper", paper.get("url",""))
                    st.divider()
            else:
                st.write("No papers retrieved.")

        # ---------------------------
        # Reasoning section
        # ---------------------------

        with st.expander("⚙ Agent Reasoning"):
            st.subheader("Planner Output")
            st.code(plan)

            st.subheader("Executor Analysis")
            st.markdown(analysis)

    # Save assistant response to history
    st.session_state.messages.append(
        {"role": "assistant", "content": final_report}
    )