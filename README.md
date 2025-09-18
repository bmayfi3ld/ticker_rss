# Ticker RSS

RSS feed generator and web server for Oklahoma Mesonet Ticker.

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- [just](https://github.com/casey/just)

## Setup

Clone the repository and set up the project:

```bash
just setup
```

## Usage

### Web Server Mode (Default)

Run the application with built-in web server:

```bash
just run
```

This starts:
- Background RSS scraper that updates every hour
- Web server on `http://0.0.0.0:5000` serving the RSS feed

#### Web Server Endpoints

- `/` - Main page with feed information
- `/rss` - RSS feed (XML format)
- `/status` - JSON status endpoint
- `/download` - Download RSS file

#### Custom Host/Port

```bash
FLASK_HOST=127.0.0.1 FLASK_PORT=8080 just run
```

### Environment Variables

- `TICKER_DAYS` - Number of days to scrape (default: 30)
- `RSS_FOLDER` - Output folder for the RSS file (default: "./")
- `FLASK_HOST` - Web server host (default: "0.0.0.0")
- `FLASK_PORT` - Web server port (default: 5000)
- `DISABLE_FLASK` - Set to "true" to run scraper-only mode
- `WAITRESS_THREADS` - Number of worker threads (default: 4)
- `WAITRESS_CONNECTION_LIMIT` - Maximum simultaneous connections (default: 1000)
- `WAITRESS_CLEANUP_INTERVAL` - Connection cleanup interval in seconds (default: 30)
- `WAITRESS_CHANNEL_TIMEOUT` - Channel timeout in seconds (default: 120)

### Available Just Commands

```
build-push-container TAG # Build and push container
clean                    # Clean up generated files
quick-test               # Quick test to verify dependencies are working
run                      # Run the web server (scraper + Flask server)
setup                    # Install dependencies and set up the project with uv
test                     # Test the web server (runs for a short time with limited days)
```


## Docker

Build and run with Docker:

```bash
docker build -t ticker-rss .
docker run -p 5000:5000 ticker-rss
```

Or use the just command for building and pushing:

```bash
just build-push-container v1.0.0
```

## Development

The project uses uv for dependency management. Dependencies are defined in `pyproject.toml` and locked in `uv.lock`.

To add development dependencies:
```bash
uv add --dev package-name
```
