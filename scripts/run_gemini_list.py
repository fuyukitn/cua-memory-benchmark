import asyncio
import os
from dotenv import load_dotenv
from pydantic import SecretStr
import tkinter as tk

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, BrowserConfig
from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContextConfig

# Load the API key from .env
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError('GEMINI_API_KEY is not set')

# Initialize the language model
llm = ChatGoogleGenerativeAI(
    model='gemini-2.5-pro-preview-03-25',
    api_key=SecretStr(api_key)
)

# Initialize the browser
browser = Browser(
    config=BrowserConfig(
        new_context_config=BrowserContextConfig(
            viewport_expansion=0  # only interact with visible elements
        )
    )
)

# GUI to collect multiple tasks (one per line)
def get_tasks_from_gui():
    tasks = []

    def on_submit():
        text = text_box.get("1.0", tk.END).strip()
        if text:
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            tasks.extend(lines)
        root.destroy()

    root = tk.Tk()
    root.title("Enter Tasks")
    root.geometry("900x600")  # Match window to text area size

    tk.Label(root, text="Enter one task per line:").pack(pady=10)

    text_box = tk.Text(root, height=35, width=120)  # Adjust text box size to match window
    text_box.pack(padx=10, pady=5)

    submit_button = tk.Button(root, text="Run", command=on_submit)
    submit_button.pack(pady=10)

    root.mainloop()
    return tasks

# Run the tasks sequentially with the agent
async def run_tasks(task_list):
    agent = Agent(
        task=task_list,
        llm=llm,
        browser=browser,
        max_actions_per_step=4,
    )
    await agent.run(max_steps=30)

# Main entry point
if __name__ == '__main__':
    task_list = get_tasks_from_gui()
    if task_list:
        asyncio.run(run_tasks(task_list))
    else:
        print("No tasks entered. Exiting.")