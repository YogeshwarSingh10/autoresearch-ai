# AutoResearch AI 🔬

### Multi-Agent AI System for Automated Literature Review

AutoResearch AI is a **multi-agent research assistant** that automatically searches academic papers, analyzes them, and generates a structured research report.

The system uses **LLM-based agents** working together to simulate a real research workflow:

1. **Planner Agent** → Creates research strategy and search queries
2. **Retriever Agent** → Searches academic papers from arXiv
3. **Executor Agent** → Analyzes papers and builds literature review
4. **Critic Agent** → Evaluates and improves the final report

The project demonstrates how **AI agents can collaborate to perform complex tasks such as academic research automation.**

---

## Features

* Automated **research planning**
* **arXiv paper retrieval**
* **AI-powered literature review**
* **Research gap detection**
* **Structured research reports**
* **Multi-agent architecture**
* **Groq LLM integration**
* Optional **Streamlit web interface**

---

## System Architecture

User Research Topic
↓
Planner Agent (Generate research plan + search queries)
↓
Retriever Agent (Search arXiv papers)
↓
Executor Agent (Analyze papers and build literature review)
↓
Critic Agent (Evaluate and improve report)
↓
Final Research Report

Each agent performs a **specialized role**, making the system modular and extensible.

---

## Project Structure

autoresearch/

agents/
    planner_agent.py
    retriever_agent.py
    executor_agent.py
    critic_agent.py

app.py
main.py
requirements.txt
README.md

### Folder Description

agents/ – Contains all AI agent implementations
planner_agent.py – Generates research plan and search queries
retriever_agent.py – Searches arXiv papers
executor_agent.py – Analyzes retrieved papers
critic_agent.py – Evaluates and improves the research report
main.py – CLI entry point for running the system
app.py – Optional Streamlit web interface

---

## Agent Descriptions

### Planner Agent

The planner agent converts the user’s research topic into a structured research plan.

Responsibilities:

* Understand research topic
* Break topic into subtopics
* Generate academic search queries
* Output structured research strategy

Example output:

{
"queries": [
"LLM hallucination detection methods",
"evaluation of hallucinations in large language models",
"benchmark datasets for hallucination detection",
"techniques to reduce hallucinations in LLMs"
]
}

---

### Retriever Agent

The retriever agent searches **arXiv** for relevant academic papers using generated queries.

Responsibilities:

* Extract search queries
* Query arXiv API
* Collect relevant research papers

Output includes:

* Title
* Authors
* Publication date
* Summary
* Paper URL

Example:

Paper: Detecting Hallucinations in Large Language Models
Authors: Smith et al.
Published: 2023
URL: https://arxiv.org/abs/xxxx.xxxxx

---

### Executor Agent

The executor agent reads the retrieved papers and generates a **literature review**.

Responsibilities:

* Analyze paper summaries
* Compare methodologies
* Extract key contributions
* Build research comparison table
* Identify insights and trends

Output includes:

* Literature review
* Comparison of approaches
* Key insights
* Research gaps

---

### Critic Agent

The critic agent acts as a **reviewer** for the generated research report.

Responsibilities:

* Evaluate completeness
* Check logical consistency
* Identify missing information
* Suggest improvements
* Produce refined final report

This step improves the **quality and reliability** of the research output.

---

## Technologies Used

Python – Core implementation
Groq API – LLM inference
LLaMA 3 – Language model
arXiv API – Academic paper retrieval
Streamlit – Optional web interface

---

## Installation

### 1 Clone Repository

git clone https://github.com/yourusername/autoresearch-ai.git
cd autoresearch-ai

---

### 2 Install Dependencies

pip install -r requirements.txt

Example requirements:

groq
arxiv
streamlit
python-dotenv

---

### 3 Setup API Key

Create a `.env` file:

GROQ_API_KEY=your_api_key_here

---

## Running the Project

### CLI Mode

Run the system using:

python main.py

Example input:

Enter research topic:
Hallucination detection in large language models

Output flow:

Planner Agent → Research plan generated
Retriever Agent → Papers retrieved
Executor Agent → Literature review created
Critic Agent → Final report generated

---

## Web Interface (Optional)

Run the Streamlit UI:

streamlit run app.py

Open in browser:

http://localhost:8501

Features include:

* Interactive research input
* Agent workflow visualization
* Paper preview cards
* Downloadable research report

---

## Example Output

### Literature Review

This report reviews recent research on hallucination detection in large language models. Several approaches have been proposed including uncertainty estimation, retrieval augmentation, and benchmark evaluation methods.

### Comparison Table

Paper | Method | Dataset | Key Contribution
Paper 1 | Uncertainty estimation | TruthfulQA | Detect hallucinations
Paper 2 | Retrieval augmented generation | NaturalQuestions | Reduce hallucinations

---

## Future Improvements

Possible extensions:

* Add Semantic Scholar or Google Scholar retrieval
* Add PDF paper parsing
* Implement RAG with vector databases
* Add citation extraction
* Generate research diagrams
* Support multiple LLM providers

---

## Educational Value

This project demonstrates concepts such as:

* Multi-agent AI systems
* LLM orchestration
* Research automation
* Tool-augmented language models
* Retrieval-augmented workflows

It is useful for learning:

* AI agent design
* LLM integration
* Academic research automation

---

## License

MIT License

---

## Author

Developed as an experimental **AI research automation system**.
