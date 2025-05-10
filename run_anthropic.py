import asyncio
from dotenv import load_dotenv
from browser_use import Agent
from langchain_anthropic import ChatAnthropic

load_dotenv()
llm = ChatAnthropic(model_name="claude-3-opus-20240229")

TASK = (
    "Open https://mock-amazon-shop.onrender.com/, "
    "toggle student discount, report cart total."
)

async def main():
    agent = Agent(
        task=TASK,
        llm=llm,
        enable_memory=True,
    )
    print(await agent.run())

if __name__ == "__main__":
    asyncio.run(main())
