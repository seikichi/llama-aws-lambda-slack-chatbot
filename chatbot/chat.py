import os
import subprocess

LLAMA_CPP_MAIN_PATH = os.environ.get("LLAMA_CPP_MAIN_PATH", "./llama.cpp/main")

with open('prompt.txt', encoding='utf-8') as f:
    PROMPT = f.read()

# FIXME
STOP_SEQUENCE = "Human:"

def chat(question: str) -> str:
    prompt = PROMPT.replace('{{question}}', question)

    p = subprocess.run([
        LLAMA_CPP_MAIN_PATH,
        "-m",
        "./model.bin",
        "-p",
        prompt
    ], capture_output=True, encoding="utf-8")

    print(p.stdout)  # debug
    print(p.stderr)  # debug

    index = p.stdout.find(prompt)
    output = p.stdout[index + len(prompt):]
    stop_index = output.find(STOP_SEQUENCE)
    return output[0:stop_index if stop_index >= 0 else len(output)].strip()
