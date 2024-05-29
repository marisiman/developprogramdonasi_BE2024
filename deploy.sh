#!/bin/bash

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
export PATH="/root/.local/bin:$PATH"

# Install dependencies
poetry install

# Run the application using Gunicorn
poetry run gunicorn -w 4 -b 0.0.0.0:$PORT app:app
