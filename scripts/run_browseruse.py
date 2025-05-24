import asyncio
import os
from dotenv import load_dotenv
from pydantic import SecretStr
import tkinter as tk
from tkinter import messagebox

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from browser_use import Agent, BrowserConfig
from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContextConfig

# Load .env
load_dotenv()

# GUI to collect tasks and model selection
def get_tasks_and_model_from_gui():
    tasks = []

    root = tk.Tk()
    root.title("Enter Tasks")
    root.geometry("900x600")

    selected_model = tk.StringVar(master=root, value="gemini")

    def on_submit():
        text = text_box.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("No Tasks", "Please enter at least one task.")
            return
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        tasks.extend(lines)
        root.destroy()

    tk.Label(root, text="Choose a model:").pack(pady=5)
    tk.Radiobutton(root, text="Gemini", variable=selected_model, value="gemini").pack()
    tk.Radiobutton(root, text="OpenAI", variable=selected_model, value="openai").pack()

    tk.Label(root, text="Enter one task per line:").pack(pady=10)
    text_box = tk.Text(root, height=30, width=120)
    text_box.pack(padx=10, pady=5)

    submit_button = tk.Button(root, text="Run", command=on_submit)
    submit_button.pack(pady=10)

    root.mainloop()
    return tasks, selected_model.get()

# Initialize LLM based on user selection
def initialize_llm(model_choice):
    if model_choice == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")
        return ChatGoogleGenerativeAI(model='gemini-2.5-pro-preview-03-25', api_key=SecretStr(api_key))
    elif model_choice == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set")
        return ChatOpenAI(model='gpt-4o', api_key=api_key)
    else:
        raise ValueError("Invalid model choice")

# Run the tasks
async def run_tasks(task_list, llm):
    browser = Browser(
        config=BrowserConfig(
            new_context_config=BrowserContextConfig(viewport_expansion=0)
        )
    )
    agent = Agent(
        task=task_list,
        llm=llm,
        browser=browser,
        max_actions_per_step=4,
    )
    await agent.run(max_steps=30)

# Main
if __name__ == '__main__':
    tasks, model = get_tasks_and_model_from_gui()
    if tasks:
        llm = initialize_llm(model)
        asyncio.run(run_tasks(tasks, llm))
    else:
        print("No tasks entered. Exiting.")