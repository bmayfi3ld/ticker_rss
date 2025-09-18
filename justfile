# Install dependencies and set up the project with uv
setup:
    uv sync

# Run the web server (scraper + Flask server)
run:
    uv run python main.py

# Test the web server (runs for a short time with limited days)
test:
    TICKER_DAYS=3 timeout 30s uv run python main.py || true

# Quick test to verify dependencies are working
quick-test:
    @echo "Testing dependencies..."
    uv run python -c "import requests, bs4, feedgen, flask, waitress; print('All dependencies imported successfully!')"

# Build and push container
build-push-container TAG:
    podman build . -t 192.168.10.1:5000/ticker-rss:{{TAG}}
    podman push 192.168.10.1:5000/ticker-rss:{{TAG}}

# Clean up generated files
clean:
    rm -f blog_rss.xml
    rm -rf .uv_cache
