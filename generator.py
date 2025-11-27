# generator.py
import os
import zipfile
import tempfile
from transformers import pipeline
import json

pipe = pipeline(
    "text-generation",
    model="microsoft/phi-3-mini-128k-instruct",
    torch_dtype="auto",
    device_map="auto",
)

SYSTEM_PROMPT = """You are an AI app scaffolding generator.
Given a user's idea and preferred template, produce a concise, functional code scaffold:
- Support templates: Streamlit (Python), React (JS), or FastAPI (Python)
- Provide a README and minimal working code.
- Do NOT include placeholder text like <insert>.
Return code as plain text with file names and code blocks."""

def generate_scaffold(user_prompt: str, template: str, tags: str = "") -> str:
    result = pipe(
        f"{SYSTEM_PROMPT}\n\nUser idea: {user_prompt}\n\nTemplate: {template}\n\nTags: {tags}\n\nCode scaffold:",
        max_new_tokens=1500,
    )
    return result[0]["generated_text"]

def write_zip(scaffold_text: str, tags: str = "") -> str:
    temp_dir = tempfile.mkdtemp()
    scaffold_path = os.path.join(temp_dir, "scaffold.txt")
    with open(scaffold_path, "w") as f:
        f.write(scaffold_text)
    # persist tags as metadata.json
    if tags:
        meta_path = os.path.join(temp_dir, "metadata.json")
        with open(meta_path, "w") as f:
            json.dump({"tags": [t.strip() for t in tags.split(",") if t]}, f)
    zip_path = os.path.join(temp_dir, "scaffold.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(scaffold_path, arcname="scaffold.txt")
        if tags:
            zipf.write(meta_path, arcname="metadata.json")
    return zip_path

# placeholder for deployment
def deploy_to_hf(scaffold_dir: str, space_name: str, hf_token: str, username: str):
    """Push the generated scaffold to a new HF Space. Requires hf_token and username."""
    from huggingface_hub import HfApi

    api = HfApi(token=hf_token)
    repo_id = f"spaces/{username}/{space_name}"
    api.create_repo(repo_id, repo_type="space", space_sdk="gradio")
    api.upload_folder(folder_path=scaffold_dir, repo_id=repo_id, repo_type="space")
    return f"https://huggingface.co/spaces/{username}/{space_name}"
