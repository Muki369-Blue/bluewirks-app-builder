import os, zipfile, tempfile, shutil
from transformers import pipeline

pipe = pipeline(
    "text-generation",
    model="microsoft/phi-3-mini-128k-instruct",
    torch_dtype="auto",
    device_map="auto"
)

SYSTEM_PROMPT = '''You are an AI app scaffolding generator.
Given a user's idea, produce a concise, functional code scaffold:
- Include a minimal backend (FastAPI or Gradio)
- Include a simple frontend (HTML or React)
- Provide a README.
- Do NOT include placeholder text like <insert>.
Return code as plain text with file names and code blocks.'''

def generate_scaffold(user_prompt: str) -> str:
    result = pipe(f"{SYSTEM_PROMPT}\n\nUser idea: {user_prompt}\n\nCode scaffold:", max_new_tokens=1500)
    return result[0]["generated_text"]

def write_zip(scaffold_text: str) -> str:
    temp_dir = tempfile.mkdtemp()
    scaffold_path = os.path.join(temp_dir, "scaffold.txt")
    with open(scaffold_path, "w") as f:
        f.write(scaffold_text)

    zip_path = os.path.join(temp_dir, "scaffold.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(scaffold_path, arcname="scaffold.txt")
    return zip_path