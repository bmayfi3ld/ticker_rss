# Ticker RSS

RSS feed generator for Oklahoma Mesonet Ticker.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) - Fast Python package installer and resolver
- [just](https://github.com/casey/just) - Command runner (optional but recommended)

## Installation

Install uv if you haven't already:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Setup

Clone the repository and set up the project:

```bash
git clone <repository-url>
cd ticker_rss
just setup
```

Or without just:

```bash
uv sync
```

## Usage

### Running the application

With just:
```bash
just run
```

Or directly with uv:
```bash
uv run python main.py
```

### Managing dependencies

Add a new dependency:
```bash
just add package-name
# or
uv add package-name
```

Remove a dependency:
```bash
just remove package-name
# or
uv remove package-name
```

### Environment Variables

- `TICKER_DAYS` - Number of days to scrape (default: 30)
- `RSS_FOLDER` - Output folder for the RSS file (default: "./")

### Available Just Commands

- `just setup` - Install dependencies and set up the project
- `just run` - Run the main application
- `just test` - Test the application (runs for 30 seconds with 3 days of data)
- `just quick-test` - Quick test to verify dependencies are working
- `just add PACKAGE` - Add a new dependency
- `just remove PACKAGE` - Remove a dependency
- `just info` - Show dependency tree
- `just clean` - Clean up generated files
- `just lock` - Update dependency lock file
- `just build-push-container` - Build and push Docker container

## Docker

Build and run with Docker:

```bash
docker build -t ticker-rss .
docker run ticker-rss
```

Or use the just command for building and pushing:

```bash
just build-push-container
```

## Development

The project uses uv for dependency management. Dependencies are defined in `pyproject.toml` and locked in `uv.lock`.

To add development dependencies:
```bash
uv add --dev package-name
```
