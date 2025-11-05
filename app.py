import gradio as gr
from generator import generate_scaffold, write_zip

def build_app(user_prompt):
    scaffold = generate_scaffold(user_prompt)
    zip_path = write_zip(scaffold)
    return scaffold, zip_path

demo = gr.Interface(
    fn=build_app,
    inputs=gr.Textbox(label="Describe your app idea", placeholder="An app that turns voice notes into haikus"),
    outputs=[
        gr.Textbox(label="Generated Scaffold", lines=25),
        gr.File(label="Download Scaffold (.zip)")
    ],
    title="BlueWirks App Builder",
    description="Describe what you want. Get a ready-to-edit full-stack scaffold in seconds."
)

if __name__ == "__main__":
    demo.launch()