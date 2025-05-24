import asyncio
import os
from dotenv import load_dotenv
from pydantic import SecretStr
import tkinter as tk

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, BrowserConfig
from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContextConfig

# Load the API key
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError('GEMINI_API_KEY is not set')

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model='gemini-2.5-pro-preview-03-25',
    api_key=SecretStr(api_key)
)

# Initialize browser
browser = Browser(
    config=BrowserConfig(
        new_context_config=BrowserContextConfig(
            viewport_expansion=0  # only what's visible on screen
        )
    )
)

# 🧾 GUI: multiline task input
def get_task_from_gui():
    task = []

    def on_submit():
        text = text_box.get("1.0", tk.END).strip()
        if text:
            task.append(text)
        root.destroy()

    root = tk.Tk()
    root.title("Enter Task")
    root.geometry("700x500")

    tk.Label(root, text="Enter your task below (you can use multiple lines):").pack(pady=10)

    text_box = tk.Text(root, height=25, width=100)
    text_box.pack(padx=10, pady=5)

    submit_button = tk.Button(root, text="Run", command=on_submit)
    submit_button.pack(pady=10)

    root.mainloop()
    return task[0] if task else None

# 🔄 Main task runner
async def run_task(task):
    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
        max_actions_per_step=4,
    )
    await agent.run(max_steps=30)

# 🚀 Entry point
if __name__ == '__main__':
    task = get_task_from_gui()
    if task:
        asyncio.run(run_task(task))
    else:
        print("No task entered. Exiting.")