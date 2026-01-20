WhatsApp to Alarm Sync Agent 
This project utilizes DroidRun and Google Gemini 2.5 Flash to create an intelligent Android automation agent. The agent autonomously extracts a class schedule from a specific WhatsApp chat and sets corresponding alarms on your Android device using the Gemini App.

Overview
The script initializes a DroidAgent that performs a multi-step workflow:

Extract: Opens WhatsApp, locates a specific contact ("teacher"), and captures a timetable file ("tuesday_only_timetable").

Process: Uses visual context (screenshots) to identify class times.

Action: Opens the Gemini App on the phone and issues natural language commands to set alarms for each identified class time.

Prerequisites
Before running the agent, ensure you have the following:

Python 3.10+ installed.

Android Device: Connected via USB with USB Debugging enabled(may also use mobile run cloud portal instead).

ADB (Android Debug Bridge): Installed and added to your system's PATH.

Google GenAI API Key: You can obtain one from Google AI Studio.

Installation
Clone this repository:

Bash
git clone https://github.com/yourusername/whatsapp-alarm-sync.git
cd whatsapp-alarm-sync
Install the required Python packages:

Bash
pip install droidrun llama-index-llms-google-genai
 Configuration
1. Environment Variables
You must export your Google API key as an environment variable so the script can access the LLM.

Mac/Linux:

Bash
export GOOGLE_API_KEY="your_actual_api_key_here"
Windows (PowerShell):

PowerShell
$env:GOOGLE_API_KEY="your_actual_api_key_here"
2. Device Setup
Ensure WhatsApp is installed and you are logged in.

Ensure the Gemini App (or Google Assistant) is installed and accessible.

Important: For the script to work "out of the box," you need a chat history that matches the prompt logic:

A contact named "teacher".

A message or file inside that chat named "tuesday_only_timetable".

Usage
Run the script using Python:

Bash
python main.py
Note: Keep your device unlocked and connected to your computer while the agent is running.

Code Breakdown
The core logic resides in the DroidAgent initialization:

Python
droid_agent = DroidAgent(
    # The natural language prompt defines the agent's Standard Operating Procedure (SOP)
    "Sync Tuesday's class schedule from WhatsApp to Alarms...",
    config=DroidrunConfig(
        agent=AgentConfig(max_steps=100) # Safety limit for agent actions
    ),
    llms=llm,       # Google Gemini 2.5 Flash
    tools=AdbTools() # Tools to interact with the Android UI
)
Customization
You can modify the prompt string in main.py to adapt the agent for different use cases:

Change the Contact: Replace 'teacher' with your specific contact name (e.g., 'Class Group').

Change the Source: Instead of a file, you could ask it to read the "last 3 messages".

Change the Action: Instead of setting alarms, you could ask it to "add events to Google Calendar".

Disclaimer
This tool uses LLMs to interact with your device's UI. While DroidRun is designed for automation, UI layouts can vary between devices and app updates. Always monitor the agent during execution to ensure it performs actions correctly.
