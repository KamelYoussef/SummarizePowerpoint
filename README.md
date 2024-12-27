repos:
  - repo: local
    hooks:
      - id: export-conda-env-myproject
        name: Export Conda Environment for MyProject
        entry: conda env export --no-builds > environment.yml
        language: system
        always_run: true
