"""
OpenAI sanity-check with tool-calling support.
Requires OPENAI_API_KEY in .env.
"""
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

# Use GPT-4o mini – supports parallel_tool_calls
llm = ChatOpenAI(model="gpt-4o-mini")

TASK = (
    "Go to amazon.com, search for laptop, sort by best rating, "
    "and give me the price of the first result."
)

async def main():
    agent = Agent(
        task=TASK,
        llm=llm,
        enable_memory=True,
    )
    print(await agent.run(max_steps=10))

if __name__ == "__main__":
    asyncio.run(main())
