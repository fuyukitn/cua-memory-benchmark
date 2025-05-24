import asyncio
import os
from dotenv import load_dotenv
from pydantic import SecretStr

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, BrowserConfig
from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContextConfig

# Load the API key from the .env file
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')

# Initialize Gemini LLM (use gemini-2.0-pro for vision support)
llm = ChatGoogleGenerativeAI(
	model='gemini-2.5-pro-preview-03-25',
	api_key=SecretStr(api_key)
)

# Create a browser instance with a context that limits visible viewport (to reduce token usage)
browser = Browser(
	config=BrowserConfig(
		new_context_config=BrowserContextConfig(
			viewport_expansion=0  # Include only what's visible on screen
		)
	)
)

# Define the task for the agent to perform
task='Go to amazon.com, search for laptop, sort by best rating, and give me the price of the first result'

# task= "Go to amazon.com, and find 5 books written by Jane Austin and put them into the shopping cart."

#["Go to amazon.com and go to book section and search for a recipe book.",
#        "Do you remember what is on the top page of amazon.com?"]
# 'Go to amazon.com, search for laptop, sort by best rating, and give me the price of the first result'
# "Go to amazon.com, and find 5 books written by Jane Austin and put them into the shopping cart."
# "Go to yahoo.com and find the latest news about Tarrif."

# Main function to run the agent
async def run_task():
	agent = Agent(
		task=task,
		llm=llm,
		browser=browser,
		max_actions_per_step=4,     # Limit the number of actions per step to avoid over-interaction
	)
	await agent.run(max_steps=30)  # Set a maximum number of steps to prevent infinite loops

# Entry point for the script
if __name__ == '__main__':
	asyncio.run(run_task())