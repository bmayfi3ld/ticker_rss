# Install dependencies and set up the project with uv
setup:
    @echo "Installing dependencies with uv..."
    uv sync
    @echo "Project setup complete!"

# Run the main application
run:
    uv run python main.py

# Install a new dependency
add PACKAGE:
    uv add {{PACKAGE}}

# Remove a dependency
remove PACKAGE:
    uv remove {{PACKAGE}}

# Show project info
info:
    uv tree

# Test the application (runs for a short time with limited days)
test:
    TICKER_DAYS=3 timeout 30s uv run python main.py || true

# Quick test to verify dependencies are working
quick-test:
    uv run python -c "import requests, bs4, feedgen; print('All dependencies imported successfully!')"

# Build and push container
build-push-container:
    # versions
    # 0.1.0 - initial
    # 0.2.0 - added images
    # 0.2.1 - fixed bad date

    podman build . -t 192.168.10.1:5000/ticker-rss:0.2.1
    podman push 192.168.10.1:5000/ticker-rss:0.2.1

# Clean up generated files
clean:
    rm -f blog_rss.xml
    rm -rf .uv_cache

# Lock dependencies
lock:
    uv lock
