import os
import subprocess

LLAMA_CPP_MAIN_PATH = os.environ.get("LLAMA_CPP_MAIN_PATH", "./llama.cpp/main")


prompt_template = """\
The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.

Human: Hello, who are you?
AI: I am an AI. How can I help you today?
Human: {{question}}
AI:"""


def chat(question: str) -> str:
    prompt = prompt_template.replace('{{question}}', question)

    p = subprocess.run([
        LLAMA_CPP_MAIN_PATH,
        "-m",
        "./model.bin",
        "-n",
        "128",
        "-p",
        prompt
    ], capture_output=True, encoding="utf-8")

    print(p.stdout)  # debug
    print(p.stderr)  # debug

    stdout = p.stdout
    index = stdout.find(prompt)
    output = stdout[index + len(prompt):]
    human_index = output.find("Human:")
    ai_message = output[0:human_index if human_index >= 0 else len(output)]

    return ai_message.strip()
