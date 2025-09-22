#!/bin/bash

# Usage: create_repo myproject
NAME=$1

if [ -z "$NAME" ]; then
  echo "Usage: create_repo <project-name>"
  exit 1
fi

# Create the repo
mkdir "$NAME"
cd "$NAME" || exit

# Initialize git
git init

# Create structure
mkdir src notebooks
touch conda.yml

echo "Repository '$NAME' created with structure:"
tree .
