Legal Agent - Court Case Analyzer

This project simulates a courtroom process using OpenAI's Agent SDK.
It features four AI agents:

ProsecutionAgent: Argues the case for the prosecution
DefenseAgent: Argues for the defense
JudgeAgent: Delivers an impartial verdict
TriageAgent: Organizes the case and categorizes it based on complexity and jurisdiction

Built with Streamlit for a fast and interactive web interface.


Setup Instructions:
Clone or Download this repository.


Create a virtual environment:
python -m venv venv


Activate the virtual environment:
Windows:
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate


Install dependencies:
pip install -r requirements.txt


Create a .env file in the root folder and add your OpenAI API key:
OPENAI_API_KEY=your-openai-api-key-here


Run the Streamlit app:
streamlit run app/run_app.py


Project Structure:
sql
Copy
Edit
LegalAgent/
|
|-- app/
|    |-- __init__.py
|    |-- agents.py
|    |-- prompts.py
|    |-- run_app.py
|
|-- venv/                (virtual environment folder)
|-- .env                 (your OpenAI API key goes here)
|-- requirements.txt
|-- README.md


Technologies Used:
OpenAI Python SDK
OpenAI Agents SDK
Streamlit
Python-dotenv


Features:
Defense Agent simulates legal defenses
Prosecution Agent builds the case for the state
Judge Agent delivers impartial verdicts
Triage Agent categorizes and routes the case
Supports jurisdiction filtering (Federal, State, International)


Disclaimer:
This tool is for educational purposes only.
It does not provide real legal advice.
