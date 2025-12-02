import subprocess

def generate_with_ollama(system_prompt, user_prompt, model="qwen2:1.5b"):
    # Remove null chars to avoid breaking subprocess
    system_prompt = system_prompt.replace("\x00", "")
    user_prompt = user_prompt.replace("\x00", "")

    full_prompt = f"<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{user_prompt} [/INST]"

    result = subprocess.run(
        ["ollama", "run", model],
        input=full_prompt,
        text=True,
        capture_output=True
    )

    if result.returncode != 0:
        return "⚠️ Error talking to Ollama:\n" + result.stderr

    return result.stdout.strip()
