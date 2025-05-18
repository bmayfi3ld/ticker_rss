setup-venv:
    @echo "Creating new Python virtual environment..."
    python3 -m venv venv
    @echo "Installing dependencies..."
    # Using the direct path to pip in the virtual environment
    venv/bin/pip install -r requirements.txt || venv/Scripts/pip install -r requirements.txt
    @echo "Virtual environment setup complete!"