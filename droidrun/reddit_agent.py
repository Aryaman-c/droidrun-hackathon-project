import os
import asyncio
from droidrun import DroidAgent, DroidrunConfig, AgentConfig, AdbTools
# from llama_index.llms.google_genai import GoogleGenAI
# from llama_index.llms.openai import OpenAI
from llama_index.llms.openai_like import OpenAILike

class RedditAutomation:
    def __init__(self):
        # Using OpenRouter as requested
        self.api_key = "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"
        self.api_base = "https://openrouter.ai/api/v1"
        self.model = "google/gemini-2.0-flash-001" 
        
        self.llm = OpenAILike(
            model=self.model,
            api_key=self.api_key,
            api_base=self.api_base,
            is_chat_model=True,
            temperature=0.0
        )
        self.tools = AdbTools()
        self.is_monitoring = False
        self.logs = []

    def log(self, message):
        print(f"[RedditAuto] {message}")
        self.logs.append(message)
        if len(self.logs) > 50:
            self.logs.pop(0)

    async def post_message(self, title: str, body: str, subreddit: str):
        self.log(f"Starting post task: {title} in {subreddit}")
        prompt = (
            f"Open the Reddit app from the home screen. "
            f"Tap on the search bar or search icon and execute a search for '{subreddit}'. "
            f"Tap on the result '{subreddit}' to go to that subreddit. "
            f"Verify you are in {subreddit}. "
            f"Tap the '+' (Create) button to start a new post within this subreddit. "
            f"Enter '{title}' as the Title. "
            f"Enter '{body}' as the body text. "
            f"Tap 'Next' if present, then tap 'Post' to submit. "
            f"Ensure the post is successfully created."
        )
        
        agent = DroidAgent(
            prompt,
            config=DroidrunConfig(agent=AgentConfig(max_steps=30)), # Increased steps for navigation
            llms=self.llm,
            tools=self.tools
        )
        
        try:
            await agent.run()
            self.log("Posting task completed.")
            return True
        except Exception as e:
            self.log(f"Posting failed: {e}")
            return False

    async def reply_to_comments(self):
        self.log("Checking for new comments...")
        prompt = (
            "Open the Reddit app. "
            "Navigate to my profile and open the most recent post. "
            "Scroll through the comments. "
            "If you see a comment that is NOT from me and does NOT have a 'thankyou' reply from me yet, "
            "tap 'Reply', type 'thankyou', and send the reply. "
            "Do this for all such comments visible. "
            "Finally, refresh the page by pulling down."
        )

        agent = DroidAgent(
            prompt,
            config=DroidrunConfig(agent=AgentConfig(max_steps=30)),
            llms=self.llm,
            tools=self.tools
        )

        try:
            await agent.run()
            self.log("Comment check completed.")
        except Exception as e:
            self.log(f"Comment check failed: {e}")

    async def start_monitoring_loop(self):
        self.is_monitoring = True
        self.log("Monitoring started.")
        while self.is_monitoring:
            await self.reply_to_comments()
            # Wait for 1 minute before next check
            for _ in range(60):
                if not self.is_monitoring:
                    break
                await asyncio.sleep(1)
        self.log("Monitoring stopped.")

    def stop_monitoring(self):
        self.is_monitoring = False
