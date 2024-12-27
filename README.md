repos:
  - repo: local
    hooks:
      - id: export-conda-env
        name: Export Conda Environment
        entry: bash -c "
          conda env export --no-builds > conda.yml;
          if git diff --quiet conda.yml; then
            echo 'No changes to conda.yml, not adding to commit.';
          else
            git add conda.yml;
          fi"
        language: system
        always_run: true

      - id: dvc-commands
        name: DVC Add, Commit, Push
        entry: bash -c "
          if dvc add donnees | grep -q 'added\\|modified'; then
            echo 'Changes detected in donnees. Running dvc commit and dvc push...';
            dvc commit && dvc push;
          else
            echo 'No changes detected in donnees. Skipping dvc commit and dvc push.';
          fi"
        language: system
        pass_filenames: false
        always_run: true
