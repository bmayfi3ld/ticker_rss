# AI Agent Instructions for ticker_rss Project

This document provides context and instructions for AI agents (particularly Claude) working on this project.

## Project Overview

**ticker_rss** is a Python application that scrapes the Oklahoma Mesonet Ticker website and generates RSS feeds. The project has been modernized to use `uv` for dependency management and `just` for task running.

## Project Structure

```
ticker_rss/
├── main.py              # Main application script
├── pyproject.toml       # Project configuration and dependencies
├── uv.lock             # Dependency lock file (auto-generated)
├── justfile            # Task runner commands
├── Dockerfile          # Container configuration
├── README.md           # User documentation
├── .gitignore          # Git ignore rules
├── .venv/              # Virtual environment (auto-generated)
└── blog_rss.xml        # Generated RSS output (runtime)
```

## Technology Stack

- **Python 3.8+** - Main programming language
- **uv** - Fast Python package manager and resolver
- **just** - Command runner for common tasks
- **Docker/Podman** - Containerization
- **Dependencies:**
  - `beautifulsoup4==4.10.0` - HTML parsing
  - `feedgen==0.9.0` - RSS generation
  - `requests==2.26.0` - HTTP requests
  - `lxml` - XML processing

## Common Development Tasks

### Environment Setup
```bash
just setup          # Install dependencies with uv
uv sync             # Alternative direct command
```

### Running the Application
```bash
just run            # Run main application
just test           # Test run (30 seconds, 3 days data)
just quick-test     # Verify dependencies only
```

### Dependency Management
```bash
just add PACKAGE    # Add new dependency
just remove PACKAGE # Remove dependency
uv add PACKAGE      # Direct uv command
uv remove PACKAGE   # Direct uv removal
```

### Project Information
```bash
just info           # Show dependency tree
uv tree            # Direct command
```

## Important Environment Variables

- `TICKER_DAYS` - Number of days to scrape (default: 30)
- `RSS_FOLDER` - Output directory for RSS file (default: "./")

## Key Files to Understand

### main.py
- Single-file application with web scraping logic
- Runs continuously with 1-hour intervals
- Scrapes historical data based on TICKER_DAYS
- Generates RSS feed in specified folder
- Uses Central Time timezone for date handling

### pyproject.toml
- Modern Python project configuration
- Contains metadata, dependencies, and build settings
- Uses hatchling as build backend
- Configured for single-script package structure

### justfile
- Contains all common development commands
- Provides consistent interface across different environments
- Includes Docker build/push commands
- Has test commands for development

## Working with This Project

### When Adding Features
1. Update dependencies in `pyproject.toml` if needed
2. Run `uv sync` to install new dependencies
3. Test changes with `just quick-test` or `just test`
4. Update README.md if adding new functionality

### When Fixing Issues
1. Check current dependencies with `just info`
2. Look at error logs from `just run` output
3. Use `just test` for faster iteration during debugging
4. Remember the app scrapes live websites with delays

### When Updating Dependencies
1. Modify `pyproject.toml` dependencies section
2. Run `uv sync` to update lockfile
3. Test with `just quick-test`
4. Commit both `pyproject.toml` and `uv.lock`

### Container Work
- Dockerfile uses multi-stage build with uv
- Uses `uv run` for execution
- Build/push with `just build-push-container`
- Container registry: `192.168.10.1:5000/ticker-rss`

## Common Patterns in This Codebase

### Error Handling
- Uses try/except for web requests
- Implements retry logic with sleep delays
- Graceful handling of missing data

### Data Processing
- BeautifulSoup for HTML parsing
- Regex for date/title extraction
- Central Time timezone handling
- RSS generation with feedgen

### Configuration
- Environment variables for runtime config
- Defaults provided for all settings
- No hardcoded paths or credentials

## Debugging Tips

1. **Import Issues**: Use `just quick-test` to verify all dependencies
2. **Runtime Issues**: Check `TICKER_DAYS` and `RSS_FOLDER` env vars
3. **Network Issues**: The app makes real HTTP requests with delays
4. **Date Issues**: App uses Central Time (-6 hours from UTC)
5. **Container Issues**: Verify uv.lock is up to date

## Best Practices for AI Agents

1. **Always run `just setup`** before making changes
2. **Use `just quick-test`** to verify changes don't break imports
3. **Respect the existing code style** and patterns
4. **Update documentation** when making significant changes
5. **Test container builds** if modifying dependencies
6. **Don't remove the sleep delays** - they prevent rate limiting
7. **Preserve timezone handling** - it's specific to the data source

## File Modification Guidelines

- **pyproject.toml**: Only modify for dependency changes
- **main.py**: Main application logic, be careful with scraping patterns
- **justfile**: Add new commands, don't remove existing ones
- **Dockerfile**: Only modify if changing Python version or uv usage
- **README.md**: Keep user-focused, technical details go here

## Testing Strategy

- **Unit Testing**: Not currently implemented (single script)
- **Integration Testing**: Use `just test` for real data testing
- **Dependency Testing**: Use `just quick-test`
- **Container Testing**: Build and run container locally

## Known Limitations

1. **Single Script**: No modular structure, everything in main.py
2. **No Tests**: Relies on manual testing and live data
3. **Network Dependent**: Requires internet access to function
4. **Time Sensitive**: Scrapes based on current date calculations
5. **Rate Limited**: Uses sleep delays to avoid overwhelming target site

## Future Improvement Ideas

- Add proper logging instead of print statements
- Implement configuration file support
- Add unit tests for date parsing logic
- Modularize the single script into functions/classes
- Add health check endpoints
- Implement retry logic for failed requests
- Add metrics/monitoring capabilities

---

This document should be updated whenever significant changes are made to the project structure, dependencies, or development workflow.