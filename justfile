setup-venv:
    @echo "Creating new Python virtual environment..."
    python3 -m venv venv
    @echo "Installing dependencies..."
    # Using the direct path to pip in the virtual environment
    venv/bin/pip install -r requirements.txt || venv/Scripts/pip install -r requirements.txt
    @echo "Virtual environment setup complete!"

build-push-container:
    # versions
    # 0.1.0 - initial
    # 0.2.0 - added images
    # 0.2.1 - fixed bad date

    podman build . -t 192.168.10.1:5000/ticker-rss:0.2.1
    podman push 192.168.10.1:5000/ticker-rss:0.2.1