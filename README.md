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
