from dotenv import load_dotenv
import os
import streamlit as st
from agents.planner_agent import planner_agent
from agents.retriever_agent import retriever_agent
from agents.executor_agent import executor_agent
from agents.critic_agent import critic_agent
from memory.memory_manager import MemoryManager

load_dotenv()

st.set_page_config(
    page_title="AutoResearch AI",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 AutoResearch AI")
st.markdown("### Multi-Agent Research Assistant")

# Initialize session state keys
for key in ["plan", "papers", "memory_context", "analysis", "final_report", "last_topic"]:
    if key not in st.session_state:
        st.session_state[key] = None

# Persist memory across reruns but recreate only once
if "memory" not in st.session_state:
    st.session_state.memory = MemoryManager()

topic = st.text_input(
    "Enter Research Topic",
    placeholder="Example: Hallucination detection in Large Language Models"
)

if st.button("🚀 Start Research"):
    if topic.strip() == "":
        st.warning("Please enter a research topic.")
        st.stop()

    progress = st.progress(0)
    memory = st.session_state.memory

    with st.spinner("Agents are working..."):
        # Planner
        plan = planner_agent(topic)
        st.session_state.plan = plan
        progress.progress(20)

        # Retriever
        papers = retriever_agent(plan, memory)
        st.session_state.papers = papers
        progress.progress(40)

        # Memory context
        memory_context = memory.search(topic)
        st.session_state.memory_context = memory_context
        progress.progress(60)

        # Executor
        analysis = executor_agent(papers, memory)
        st.session_state.analysis = analysis
        progress.progress(80)

        # Critic
        final_report = critic_agent(analysis)
        st.session_state.final_report = final_report
        st.session_state.last_topic = topic
        progress.progress(100)

# ===============================
# DISPLAY RESULTS (from session state)
# ===============================
if st.session_state.final_report:
    st.header(f"📄 Final Research Report — *{st.session_state.last_topic}*")
    st.markdown(st.session_state.final_report)
    st.download_button(
        label="⬇ Download Research Report",
        data=st.session_state.final_report,
        file_name=f"research_report_{st.session_state.last_topic[:30]}.txt",
        mime="text/plain"
    )

    with st.expander("🧠 Show Agent Reasoning"):
        st.subheader("Planner Output")
        st.code(st.session_state.plan)

        st.subheader("Retrieved Papers")
        papers = st.session_state.papers
        if papers:
            for paper in papers:
                st.write("Title:", paper.get("title", ""))
                st.write("Summary:", paper.get("summary", "")[:200])
                st.write("URL:", paper.get("url", ""))
                st.divider()
        else:
            st.write("No papers retrieved.")

        st.subheader("Memory Context Used")
        memory_context = st.session_state.memory_context
        if memory_context:
            for item in memory_context:
                st.write("Title:", item.get("title", ""))
                st.write("Snippet:", item.get("content", "")[:200])
                st.write("URL:", item.get("source", ""))
                st.divider()
        else:
            st.write("No relevant memory retrieved.")

        st.subheader("Executor Analysis")
        st.markdown(st.session_state.analysis)