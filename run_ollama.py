from browser_use import Agent
from langchain_ollama import ChatOllama
import asyncio

llm = ChatOllama(model="llama3")

async def main():
    agent = Agent(
        task = "Go to https://www.google.com/, then tell the title.",
        llm=llm,
        enable_memory=True,
    )
    result = await agent.run()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())