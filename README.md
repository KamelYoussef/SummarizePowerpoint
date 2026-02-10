import os
import hashlib
import mlflow
import stat

def smart_log_data(local_path, artifact_name="training_dataset"):
    """
    DVC-like versioning inside MLflow.
    Uses Hard Links to save space and sets files to Read-Only for security.
    """
    if not mlflow.active_run():
        raise Exception("No active MLflow run found! Start a run first.")

    # 1. Get the MLflow destination folder for this specific run
    run_id = mlflow.active_run().info.run_id
    dest_dir = os.path.join(mlflow.get_artifact_uri().replace("file://", ""), artifact_name)
    os.makedirs(dest_dir, exist_ok=True)
    
    filename = os.path.basename(local_path)
    dest_path = os.path.join(dest_dir, filename)

    # 2. Link the data (Deduplication)
    try:
        if os.path.exists(dest_path):
            os.remove(dest_path)
        
        # This is the "Magic": Link points to the same disk space
        os.link(local_path, dest_path)
        
        # 3. Security: Set the logged file to READ-ONLY (444)
        # This ensures the 'historical record' in MLflow cannot be changed
        os.chmod(dest_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        
        print(f"Successfully versioned: {filename}")
        print(f"Run ID: {run_id} | Storage: No extra space used.")
        
    except Exception as e:
        print(f"Hard Link failed (maybe different disks?). Falling back to copy: {e}")
        mlflow.log_artifact(local_path, artifact_name)

# --- HOW TO USE IN JUPYTER ---
with mlflow.start_run(run_name="Secure_Model_v1"):
    # Just point to your data, the function handles the rest
    smart_log_data("/home/jovyan/data/confidential_v1.csv")
    
    # Your training code here...
