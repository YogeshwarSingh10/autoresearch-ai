import streamlit as st

from agents.plannner_agent import planner_agent
from agents.retreiver_agent import retriever_agent
from agents.executor_agent import executor_agent
from agents.critic_agent import critic_agent


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

    with st.spinner("Agents are working..."):

        # ------------------
        # Planner
        # ------------------

        st.subheader("🧠 Planner Agent")

        plan = planner_agent(topic)

        st.code(plan)

        progress.progress(25)


        # ------------------
        # Retriever
        # ------------------

        st.subheader("📚 Retriever Agent")

        papers = retriever_agent(plan)

        progress.progress(50)

        if len(papers) == 0:
            st.warning("No papers found.")
        else:
            for paper in papers:

                with st.container():

                    st.markdown(f"### {paper['title']}")

                    if "authors" in paper:
                        st.write("**Authors:**", ", ".join(paper["authors"]))

                    if "published" in paper:
                        st.write("Published:", paper["published"])

                    st.write(paper["summary"][:300] + "...")

                    st.markdown(f"[📄 Read Paper]({paper['url']})")

                    st.divider()


        # ------------------
        # Executor
        # ------------------

        st.subheader("⚙ Executor Agent")

        analysis = executor_agent(papers)

        st.write(analysis)

        progress.progress(75)


        # ------------------
        # Critic
        # ------------------

        st.subheader("🧾 Critic Agent")

        final_report = critic_agent(analysis)

        st.write(final_report)

        progress.progress(100)


        # ------------------
        # Download Button
        # ------------------

        st.download_button(
            label="⬇ Download Research Report",
            data=final_report,
            file_name="research_report.txt",
            mime="text/plain"
        )