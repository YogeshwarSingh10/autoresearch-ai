import streamlit as st

from agents.planner_agent import planner_agent
from agents.retriever_agent import retriever_agent
from agents.executor_agent import executor_agent
from agents.critic_agent import critic_agent

from memory.memory_manager import MemoryManager


st.set_page_config(
    page_title="AutoResearch AI",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 AutoResearch AI")
st.markdown("### Multi-Agent Research Assistant")

topic = st.text_input(
    "Enter Research Topic",
    placeholder="Example: Hallucination detection in Large Language Models"
)


if st.button("🚀 Start Research"):

    if topic.strip() == "":
        st.warning("Please enter a research topic.")
        st.stop()

    progress = st.progress(0)

    # initialize memory
    memory = MemoryManager()

    # ensure fresh memory each run
    memory.reset()

    with st.spinner("Agents are working..."):

        # ------------------
        # Planner
        # ------------------

        plan = planner_agent(topic)
        progress.progress(20)

        # ------------------
        # Retriever
        # ------------------

        papers = retriever_agent(plan, memory)
        progress.progress(40)

        # ------------------
        # Store in memory
        # ------------------

        if papers:
            memory.store_many(papers)

        # retrieve relevant context
        memory_context = memory.search(topic)

        progress.progress(60)

        # ------------------
        # Executor
        # ------------------

        analysis = executor_agent(papers, memory)

        progress.progress(80)

        # ------------------
        # Critic
        # ------------------

        final_report = critic_agent(analysis)

        progress.progress(100)


    # ===============================
    # FINAL REPORT (MAIN UI)
    # ===============================

    st.header("📄 Final Research Report")
    st.markdown(final_report)

    st.download_button(
        label="⬇ Download Research Report",
        data=final_report,
        file_name="research_report.txt",
        mime="text/plain"
    )


    # ===============================
    # DEBUG / THINKING PANEL
    # ===============================

    with st.expander("🧠 Show Agent Reasoning"):

        st.subheader("Planner Output")
        st.code(plan)

        st.subheader("Retrieved Papers")

        if papers:
            for paper in papers:

                title = paper.get("title", "")
                summary = paper.get("summary", "")
                url = paper.get("url", "")

                st.write("Title:", title)
                st.write("Summary:", summary[:200])
                st.write("URL:", url)

                st.divider()
        else:
            st.write("No papers retrieved.")

        st.subheader("Memory Context Used")
        if memory_context:
            for item in memory_context:
                st.write("Title:", item.get("title", ""))
                st.write("Snippet:", (item.get("content", ""))[:200])
                st.write("URL:", item.get("source", ""))
                st.divider()
        else:
            st.write("No relevant memory retrieved.")

        st.subheader("Executor Analysis")
        st.markdown(analysis)