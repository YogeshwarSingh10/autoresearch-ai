# AutoResearch Agents

AutoResearch Agents is a tool that helps automate the research process.  
Given a topic, it finds relevant papers, analyzes them, and produces a structured research report.

---

## What it does

1. **Planner Agent**  
   Breaks the research topic into subtopics and search queries.

2. **Retriever Agent**  
   Finds relevant academic papers (from arXiv) and checks previously stored results.

3. **Executor Agent**  
   Reads the papers and generates a literature review and key insights.

4. **Critic Agent**  
   Reviews the generated report and improves clarity and completeness.

---

## Project Structure


research-agent-hackathon
│
├── app.py # Main entry point (UI)
├── main.py # Old CLI entry (not used)
│
├── agents # Agent implementations
│ ├── planner_agent.py
│ ├── retriever_agent.py
│ ├── executor_agent.py
│ └── critic_agent.py
│
├── memory # Stores previously retrieved papers
│ ├── memory_manager.py
│ ├── embeddings.py
│ └── vector_store.py
│
├── tools # Paper search and scraping
│ ├── search.py
│ ├── scrape.py
│ └── summarize.py


---

## Setup

### 1. Clone the repo

```bash
git clone <repo-url>
cd research-agent-hackathon
```
### 2. Create environment
```bash
conda create -n research-agent python=3.10
conda activate research-agent
```

### 3. Install dependencies
```bash
pip install -e .
```

## Environment Variables

Create a .env file:

```
AZURE_SEARCH_ENDPOINT=your_endpoint
AZURE_SEARCH_API_KEY=your_api_key
AZURE_SEARCH_INDEX_NAME=research-papers
```

## Run the app
```
python app.py
```

Enter a research topic in the UI and the system will generate a research report.

Example topics
vehicle dynamics
reinforcement learning robotics
autonomous driving
multi-robot navigation

## Output

The system produces a report containing:

literature review

summary of papers

key insights

research gaps

Example output is saved in research_report.txt.
