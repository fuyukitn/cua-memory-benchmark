import asyncio
from browser_use import Agent
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3")

task="Go to https://www.google.com/, then tell the title."

async def main():
    agent = Agent(
        task = task,
        llm=llm,
        enable_memory=True,   # default memory config is built automatically
    )
    print(await agent.run())

if __name__ == "__main__":
    asyncio.run(main())
