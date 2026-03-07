from agents.plannner_agent import planner_agent
from agents.retreiver_agent import retriever_agent
from agents.executor_agent import executor_agent
from agents.critic_agent import critic_agent


def main():

    print("\n==============================")
    print("   AutoResearch Agents")
    print("==============================\n")

    research_goal = input("Enter your research topic:\n> ")

    print("\n----- Planner Agent -----\n")
    plan = planner_agent(research_goal)
    print(plan)

    print("\n----- Retriever Agent -----\n")
    papers = retriever_agent(plan)

    print("\nRetrieved Papers:\n")

    for i, paper in enumerate(papers, 1):
        print(f"{i}. {paper['title']}")
        print(f"   {paper['url']}\n")

    print("\n----- Executor Agent -----\n")
    analysis = executor_agent(papers)
    print(analysis)

    print("\n----- Critic Agent -----\n")
    final_report = critic_agent(analysis)

    print("\n==============================")
    print("      FINAL RESEARCH REPORT")
    print("==============================\n")

    print(final_report)
    # SAVE REPORT TO FILE (ADD HERE)
    with open("research_report.txt", "w", encoding="utf-8") as f:
        f.write(final_report)

    print("\nReport saved as research_report.txt")


if __name__ == "__main__":
    main()