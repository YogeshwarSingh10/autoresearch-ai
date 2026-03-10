# AutoResearch Agents

**AutoResearch Agents** is a multi-agent system that automates the academic research workflow.  
Given a research topic, the system searches for relevant papers, analyzes them, and generates a structured research report.

It combines multiple AI agents to plan, retrieve, analyze, and refine research findings.

---

# Overview

The system follows a multi-agent pipeline that converts a **research topic → structured research report**.

Workflow:

1. **Planner Agent**
   - Breaks the research topic into smaller subtopics and search queries.

2. **Retriever Agent**
   - Searches for relevant academic papers (primarily from arXiv).
   - Checks previously stored results in memory to avoid repeated searches.

3. **Executor Agent**
   - Reads the retrieved papers.
   - Generates summaries, key insights, and a literature review.

4. **Critic Agent**
   - Reviews the generated report.
   - Improves clarity, structure, and completeness.

This pipeline enables automated literature exploration and faster research synthesis.

---

# Features

- Automated research planning
- Academic paper retrieval
- Paper summarization
- Literature review generation
- Research insight extraction
- Memory system to avoid repeated searches
- Modular multi-agent architecture

---

# System Architecture

The system processes a research query through the following pipeline:

```
User Topic
   │
   ▼
Planner Agent
   │
   ▼
Retriever Agent ───► Memory Store
   │
   ▼
Executor Agent
   │
   ▼
Critic Agent
   │
   ▼
Final Research Report
```

---

# Project Structure

```
research-agent-hackathon
│
├── app.py                  # Main UI entry point
├── main.py                 # Legacy CLI entry (not used)
│
├── agents                  # Agent implementations
│   ├── planner_agent.py
│   ├── retriever_agent.py
│   ├── executor_agent.py
│   └── critic_agent.py
│
├── memory                  # Paper storage and retrieval
│   ├── memory_manager.py
│   ├── embeddings.py
│   └── vector_store.py
│
├── tools                   # Research utilities
│   ├── search.py           # Paper search (arXiv)
│   ├── scrape.py           # Paper content extraction
│   └── summarize.py        # Paper summarization
│
└── research_report.txt     # Example generated report
```

---

# Installation

## 1. Clone the Repository

```bash
git clone <repo-url>
cd research-agent-hackathon
```

---

## 2. Create Environment

Using Conda:

```bash
conda create -n research-agent python=3.10
conda activate research-agent
```

---

## 3. Install Dependencies

```bash
pip install -e .
```

---

# Environment Variables

Create a `.env` file in the project root and add:

```
AZURE_SEARCH_ENDPOINT=your_endpoint
AZURE_SEARCH_API_KEY=your_api_key
AZURE_SEARCH_INDEX_NAME=research-papers
```

These variables are required for the vector search system used to store and retrieve research papers.

---

# Running the Application

Start the application:

```bash
python app.py
```

A UI will open where you can enter a research topic.

The system will automatically generate a research report.

---

# Example Topics

You can try the system with topics such as:

- Vehicle dynamics
- Reinforcement learning in robotics
- Autonomous driving
- Multi-robot navigation
- Large language model agents
- AI for healthcare

---

# Output

The system produces a structured research report containing:

- Literature review
- Summaries of relevant papers
- Key insights
- Identified research gaps
- Suggested future research directions

An example output is saved in:

```
research_report.txt
```

---

# Use Cases

- Rapid literature review
- Research project exploration
- Hackathon idea generation
- Academic topic understanding
- AI-assisted research workflows

---

# Future Improvements

- Support for more research databases (Semantic Scholar, Google Scholar)
- Improved citation tracking
- Automatic PDF parsing
- Visualization of research clusters
- Interactive report generation

---

# License

This project is licensed under the MIT License.

Copyright (c) 2026

Permission is granted to use, copy, modify, and distribute this software for any purpose, with or without modification, provided that the original copyright notice is included.

The software is provided "as is", without warranty of any kind.
