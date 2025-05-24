import asyncio, sys

CMDS = [
    "python run_ollama.py",
    "python run_anthropic.py",
    "python run_openai.py",
]

async def spawn(cmd):
    proc = await asyncio.create_subprocess_shell(cmd)
    await proc.wait()
    if proc.returncode != 0:
        sys.exit(f"{cmd} failed")

asyncio.run(asyncio.gather(*(spawn(c) for c in CMDS)))
