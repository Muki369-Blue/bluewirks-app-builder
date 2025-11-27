# app.py
import gradio as gr
from generator import generate_scaffold, write_zip, deploy_to_hf

def build_app(user_prompt, template, tags):
    scaffold = generate_scaffold(user_prompt, template=template, tags=tags)
    zip_path = write_zip(scaffold, tags=tags)
    return scaffold, zip_path

def handle_deploy(scaffold, space_name, hf_token, username):
    # In a real app you would unpack the scaffold zip and call deploy_to_hf()
    # Here we simply return a placeholder link
    try:
        # deploy_path = unzip scaffold and call deploy_to_hf(...)
        return deploy_to_hf(scaffold, space_name, hf_token, username)
    except Exception as e:
        return f"Deployment failed: {e}"

with gr.Blocks(title="BlueWirks App Builder") as demo:
    gr.Markdown("## Describe, choose a template, and build!")
    prompt = gr.Textbox(label="Describe your app idea",
                        placeholder="An app that turns voice notes into haikus")
    template = gr.Dropdown(label="Choose a template",
                           choices=["Streamlit", "React", "FastAPI"],
                           value="Streamlit")
    tags = gr.Textbox(label="Tags / metadata (optional)",
                      placeholder="e.g. productivity, voice")
    generate_btn = gr.Button("Generate Scaffold")
    scaffold_out = gr.Textbox(label="Generated Scaffold", lines=25)
    download_out = gr.File(label="Download Scaffold (.zip)")
    generate_btn.click(fn=build_app,
                       inputs=[prompt, template, tags],
                       outputs=[scaffold_out, download_out])

    # Deployment section
    gr.Markdown("## Deploy your backend to Hugging Face")
    space_name = gr.Textbox(label="Space name", placeholder="my-cool-app")
    hf_token = gr.Textbox(label="HF Access Token",
                          type="password",
                          placeholder="hf_...")
    username = gr.Textbox(label="HF Username")
    deploy_btn = gr.Button("Deploy to HF")
    deploy_link = gr.Textbox(label="Deployment Link")
    deploy_btn.click(fn=handle_deploy,
                     inputs=[scaffold_out, space_name, hf_token, username],
                     outputs=[deploy_link])

if __name__ == "__main__":
    demo.launch()
