import subprocess
from IPython.display import display, Markdown

def run_dvc_command(command):
    """
    Run a DVC command and display the output.
    """
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True, check=True)
        display(Markdown(f"**Command:** `{command}`\n\n**Output:**\n\n```\n{result.stdout}\n```"))
    except subprocess.CalledProcessError as e:
        display(Markdown(f"**Command:** `{command}`\n\n**Error:**\n\n```\n{e.stderr}\n```"))

# Example usage
run_dvc_command("dvc --version")
