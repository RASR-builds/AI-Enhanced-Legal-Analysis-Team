# app/agent_factory.py

from agents import Agent
from prompts import (
    get_defense_prompt,
    get_prosecution_prompt,
    get_judge_prompt,
    get_triage_prompt,
)

def create_agents(case_name, case_facts, charges, jurisdiction):
    defense_agent = Agent(
        name="DefenseAgent",
        instructions=get_defense_prompt(case_name, case_facts, charges, jurisdiction),
        model="gpt-4o-mini",
    )

    prosecution_agent = Agent(
        name="ProsecutionAgent",
        instructions=get_prosecution_prompt(case_name, case_facts, charges, jurisdiction),
        model="gpt-4o-mini",
    )

    judge_agent = Agent(
        name="JudgeAgent",
        instructions=get_judge_prompt(case_name, case_facts, charges, jurisdiction),
        model="gpt-4o",
    )

    triage_agent = Agent(
        name="TriageAgent",
        instructions=get_triage_prompt(case_name, case_facts, charges, jurisdiction),
        handoffs=[defense_agent, prosecution_agent],
        model="gpt-4o-mini",
    )

    return {
        "defense": defense_agent,
        "prosecution": prosecution_agent,
        "judge": judge_agent,
        "triage": triage_agent,
    }
