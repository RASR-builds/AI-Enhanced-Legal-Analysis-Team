# app/run_app.py

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from agent_factory import create_agents
from agents import Runner
import asyncio

st.set_page_config(
    page_title="Legal Case Analyzer",
    layout="wide",
    page_icon="⚖️",
    initial_sidebar_state="expanded",
)

st.title("⚖️ AI-Powered Legal Case Analyzer")
st.info("This application uses OpenAI Agents SDK for simulation.")

# Sidebar for case input
st.sidebar.header("Case Information")
case_name  = st.sidebar.text_input("Case Name", "State v. Doe")
case_facts = st.sidebar.text_area(
    "Case Facts", height=150,
    value="A theft occurred at a local electronics store. The defendant was found nearby with electronics."
)
charges    = st.sidebar.text_input("Charges", "Theft under Penal Code 123")

# Sidebar for jurisdiction
st.sidebar.header("Jurisdiction")
jurisdiction = st.sidebar.selectbox(
    "Select Jurisdiction",
    ["Federal", "State", "International"],
    index=1
)

if st.button("Run Legal Analysis", type="primary", use_container_width=True):

    agents            = create_agents(case_name, case_facts, charges, jurisdiction)
    triage_agent      = agents["triage"]
    defense_agent     = agents["defense"]
    prosecution_agent = agents["prosecution"]
    judge_agent       = agents["judge"]

    async def main_run():
        # 1) Triage Agent
        with st.spinner("🔎 Triage Agent is analyzing the case..."):
            triage_result = await Runner.run(
                triage_agent,
                input="Analyze the case details and output Complexity, Confirmed Jurisdiction, and Urgency level."
            )
        # Display triage summary in sidebar
        st.sidebar.subheader("📋 Triage Summary")
        st.sidebar.write(triage_result.final_output)

        # 2) Defense Agent
        with st.spinner("🛡️ Defense Agent is preparing arguments..."):
            defense_result = await Runner.run(
                defense_agent,
                input="Prepare your defense argument based on the case facts and charges."
            )
        defense_text = defense_result.final_output

        # 3) Prosecution Agent
        with st.spinner("⚔️ Prosecution Agent is preparing arguments..."):
            prosecution_prompt = (
                f"The defense argument is as follows:\n{defense_text}\n\n"
                "Now prepare your prosecution argument."
            )
            prosecution_result = await Runner.run(
                prosecution_agent,
                input=prosecution_prompt
            )
        prosecution_text = prosecution_result.final_output

        # 4) Judge Agent
        judge_prompt = (
            f"Defense says:\n{defense_text}\n\n"
            f"Prosecution says:\n{prosecution_text}\n\n"
            f"Under {jurisdiction} jurisdiction, deliver a final verdict (GUILTY or NOT GUILTY) and your reasoning."
        )
        with st.spinner("🧑‍⚖️ Judge Agent is delivering verdict..."):
            judge_result = await Runner.run(
                judge_agent,
                input=judge_prompt
            )

        # Display outputs
        tab1, tab2, tab3 = st.tabs([
            "Defense Argument", "Prosecution Argument", "Final Verdict"
        ])

        with tab1:
            st.subheader("Defense Argument")
            st.markdown(defense_text)

        with tab2:
            st.subheader("Prosecution Argument")
            st.markdown(prosecution_text)

        with tab3:
            st.subheader("Final Verdict by Judge")
            st.success(judge_result.final_output)

        # 5) Download Full Report
        report = f"""
Case Name: {case_name}
Jurisdiction: {jurisdiction}
Charges: {charges}

📋 Triage Summary:
{triage_result.final_output}

🛡️ Defense Argument:
{defense_text}

⚔️ Prosecution Argument:
{prosecution_text}

🧑‍⚖️ Final Verdict:
{judge_result.final_output}
"""
        st.download_button(
            label="📄 Download Full Legal Report",
            data=report,
            file_name=f"{case_name.replace(' ', '_').lower()}_report.txt",
            mime="text/plain"
        )

    asyncio.run(main_run())

else:
    st.info("👈 Fill out the case details and click 'Run Legal Analysis' to begin.")
