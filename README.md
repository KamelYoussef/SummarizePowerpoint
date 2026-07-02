import logging
import sys
import mlflow

# 1. Clear any existing handlers to prevent duplicate lines
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# 2. Configure logging to point directly to Jupyter's output stream
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# 3. Attach the handler to the root logger and the HTTP loggers
root_logger = logging.getLogger()
root_logger.addHandler(handler)
root_logger.setLevel(logging.INFO)

# 4. Crank HTTP libraries and MLflow up to DEBUG to catch the URLs
logging.getLogger("urllib3").setLevel(logging.DEBUG)
logging.getLogger("requests").setLevel(logging.DEBUG)
logging.getLogger("mlflow").setLevel(logging.DEBUG)
