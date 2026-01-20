import os
import asyncio
from droidrun import DroidAgent, DroidrunConfig, AgentConfig, AdbTools
# from llama_index.llms.openai import OpenAI
from llama_index.llms.openai_like import OpenAILike

async def main():
    api_key = "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"
    api_base = "https://openrouter.ai/api/v1"
    model = "google/gemini-2.0-flash-001"
    
    llm = OpenAILike(
        model=model,
        api_key=api_key,
        api_base=api_base,
        is_chat_model=True,
        temperature=0.0
    )
    
    print("Initializing DroidAgent...")
    agent = DroidAgent(
        "Open the Reddit app. Wait 5 seconds.",
        config=DroidrunConfig(agent=AgentConfig(max_steps=5)),
        llms=llm,
        tools=AdbTools()
    )
    
    print("Running agent...")
    await agent.run()
    print("Agent run complete.")

if __name__ == "__main__":
    asyncio.run(main())
