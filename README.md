import ipywidgets as widgets
from IPython.display import display, Markdown

def dvc_add(file_path):
    run_dvc_command(f"dvc add {file_path}")

def dvc_pull():
    run_dvc_command("dvc pull")

def dvc_push():
    run_dvc_command("dvc push")

# Widgets
file_input = widgets.Text(description="File Path:")
button_add = widgets.Button(description="DVC Add")
button_add.on_click(lambda _: dvc_add(file_input.value))

button_pull = widgets.Button(description="DVC Pull")
button_pull.on_click(lambda _: dvc_pull())

button_push = widgets.Button(description="DVC Push")
button_push.on_click(lambda _: dvc_push())

# Display widgets
display(widgets.VBox([file_input, button_add, button_pull, button_push]))
