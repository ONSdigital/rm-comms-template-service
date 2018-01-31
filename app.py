from run import create_app

# This is a duplicate of run.py, with minor modifications to support gunicorn execution.

config_path = "config.Config"

app = create_app()

