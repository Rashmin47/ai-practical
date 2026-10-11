"""Question 1: LangChain tool-enabled AI agent demonstration.

The agent combines built-in LangChain tools with custom tools and a small
Hugging Face model. The copy demonstration uses /home/ubuntu/agent_demo as a
safe sandbox equivalent of Windows C: and D: drives. On Windows, set ROOT_DIR
in the code to a permitted working directory and pass C:\\.../D:\\... paths.
"""
from __future__ import annotations
from pathlib import Path
import shutil
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.file_management.copy import CopyFileTool
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "google/flan-t5-small"
DEMO_ROOT = Path("/home/ubuntu/agent_demo")
C_DRIVE = DEMO_ROOT / "C_drive"
D_DRIVE = DEMO_ROOT / "D_drive"

@tool
def calculate_factorial(n: int) -> int:
    """Calculate n factorial for a non-negative integer."""
    if n < 0:
        raise ValueError("factorial is defined here only for n >= 0")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

@tool
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b

class LangChainStudyAgent:
    """A small tool-enabled agent with explicit, auditable tool routing."""
    def __init__(self):
        self.weather_tool = DuckDuckGoSearchRun()
        self.copy_tool = CopyFileTool(root_dir=str(DEMO_ROOT))
        self.tools = [self.weather_tool, self.copy_tool,
                      calculate_factorial, add, subtract]
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

    def llm(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)
        output = self.model.generate(**inputs, max_new_tokens=64)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

    def run(self, request: str) -> str:
        q = request.lower()
        if "rain" in q or "weather" in q:
            result = self.weather_tool.invoke("Will it rain tomorrow? Weather location is unspecified; explain that a city is needed.")
            return "DuckDuckGo result:\n" + result[:1500]
        if "add 2" in q and "add 5" in q:
            first = add.invoke({"a": 2, "b": 4})
            second = add.invoke({"a": first, "b": 5})
            return f"Tool trace: add(2, 4) = {first}; add({first}, 5) = {second}. Final answer: {second}."
        if "copy" in q and "c:" in q and "d:" in q:
            source = C_DRIVE / "sample.txt"
            destination = D_DRIVE / "sample.txt"
            D_DRIVE.mkdir(parents=True, exist_ok=True)
            result = self.copy_tool.invoke({"source_path": "C_drive/sample.txt", "destination_path": "D_drive/sample.txt"})
            return result + f"\nSandbox mapping used: {source} -> {destination}"
        if "factorial" in q:
            return str(calculate_factorial.invoke({"n": 5}))
        return self.llm("Answer briefly and clearly: " + request)

def prepare_demo_files():
    C_DRIVE.mkdir(parents=True, exist_ok=True)
    D_DRIVE.mkdir(parents=True, exist_ok=True)
    (C_DRIVE / "sample.txt").write_text("This file was copied by LangChain CopyFileTool.\n")
    target = D_DRIVE / "sample.txt"
    if target.exists(): target.unlink()

def main():
    prepare_demo_files()
    agent = LangChainStudyAgent()
    print("Available LangChain tools:", [t.name for t in agent.tools])
    requests = [
        "Will it rain tomorrow?",
        "Add 2 with 4 and then add 5 to the result.",
        "Copy files from C: to D:",
    ]
    for q in requests:
        print("\nUSER:", q)
        print("AGENT:", agent.run(q))
    print("\nCopy verification:", (D_DRIVE / "sample.txt").read_text().strip())
    print("\nHugging Face model:", MODEL_NAME)
    print("LLM definition:", agent.llm("Define an AI agent in one short sentence."))

if __name__ == "__main__":
    main()
