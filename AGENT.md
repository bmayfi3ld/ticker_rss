# AI Agent Instructions for ticker_rss Project

This document provides context and instructions for AI agents working on this project.

## Project Overview

**ticker_rss** is a Python application that scrapes the Oklahoma Mesonet Ticker website and generates RSS feeds. The project has been modernized to use `uv` for dependency management and `just` for task running. It now includes a Flask web server with Waitress as the production WSGI server, providing both RSS generation and web serving capabilities.

## Project Structure

```
ticker_rss/
├── main.py              # Main application script with Flask web server
├── pyproject.toml       # Project configuration and dependencies
├── uv.lock             # Dependency lock file (auto-generated)
├── justfile            # Task runner commands (simplified, no uv wrappers)
├── Dockerfile          # Container configuration
├── README.md           # User documentation
├── AGENT.md            # This file - AI agent instructions
├── .gitignore          # Git ignore rules
├── .venv/              # Virtual environment (auto-generated)
└── blog_rss.xml        # Generated RSS output (runtime)
```

## Technology Stack

- **Python 3.13+** - Main programming language (upgraded from 3.8+)
- **uv** - Fast Python package manager and resolver
- **just** - Command runner for common tasks (simplified to avoid simple wrappers)
- **Flask** - Web framework for serving RSS feeds
- **Waitress** - Production WSGI server
- **Docker/Podman** - Containerization
- **Dependencies:**
  - `beautifulsoup4==4.13.5` - HTML parsing (updated)
  - `feedgen==1.0.0` - RSS generation (updated)
  - `requests==2.32.5.0` - HTTP requests (updated)
  - `lxml==6.0.1` - XML processing (updated)
  - `flask>=3.1.2` - Web framework (new)
  - `waitress>=3.0.2` - WSGI server (new)

## Application Modes

The application now supports two modes:

### Web Server Mode (Default)
- Runs Flask web server with Waitress
- Background thread scrapes data every hour
- Serves RSS feed via HTTP endpoints
- Production-ready with configurable server settings

### Scraper-Only Mode
- Set `DISABLE_FLASK=true` environment variable
- Runs only the scraper without web server
- Useful for cron jobs or containerized scraping

## Common Development Tasks

### Environment Setup
```bash
just setup          # Install dependencies with uv
# OR directly:
uv sync             # Direct uv command (no wrapper in justfile anymore)
```

### Running the Application
```bash
just run            # Run web server mode (scraper + Flask)
just test           # Test run (30 seconds, 3 days data)
just quick-test     # Verify dependencies only
```

### Dependency Management
Use uv directly (no justfile wrappers):
```bash
uv add PACKAGE      # Add new dependency
uv remove PACKAGE   # Remove dependency
uv tree            # Show dependency tree
```

### Project Cleanup
```bash
just clean          # Remove generated files and cache
```

## Important Environment Variables

### Core Configuration
- `TICKER_DAYS` - Number of days to scrape (default: 30)
- `RSS_FOLDER` - Output directory for RSS file (default: "./")
- `DISABLE_FLASK` - Set to "true" for scraper-only mode

### Flask Web Server
- `FLASK_HOST` - Web server host (default: "0.0.0.0")
- `FLASK_PORT` - Web server port (default: 5000)

### Waitress Production Server
- `WAITRESS_THREADS` - Number of worker threads (default: 4)
- `WAITRESS_CONNECTION_LIMIT` - Maximum simultaneous connections (default: 1000)
- `WAITRESS_CLEANUP_INTERVAL` - Connection cleanup interval in seconds (default: 30)
- `WAITRESS_CHANNEL_TIMEOUT` - Channel timeout in seconds (default: 120)

## Web Server Endpoints

When running in web server mode:
- `/` - Main page with feed information
- `/rss` - RSS feed (XML format)
- `/status` - JSON status endpoint with file info
- `/download` - Download RSS file

## Key Files to Understand

### main.py
- Single-file application with web scraping logic AND Flask web server
- Runs in two modes: web server (default) or scraper-only
- Web server uses Waitress for production deployment
- Background thread handles RSS generation every hour
- Scrapes historical data based on TICKER_DAYS
- Uses Central Time timezone for date handling
- Includes comprehensive logging

### pyproject.toml
- Modern Python project configuration
- Contains metadata, dependencies, and build settings
- Uses hatchling as build backend
- Configured for single-script package structure
- Now requires Python 3.13+ with updated dependencies

### justfile
- **SIMPLIFIED** - No longer provides simple wrappers for uv commands
- Contains only complex/composite commands that add value
- Available commands:
  - `setup` - Install dependencies
  - `run` - Run web server mode
  - `test` - Test run with limited time/data
  - `quick-test` - Verify dependencies
  - `build-push-container TAG` - Container operations
  - `clean` - Remove generated files

## Working with This Project

### When Adding Features
1. Update dependencies in `pyproject.toml` if needed
2. Run `uv sync` directly to install new dependencies
3. Test changes with `just quick-test` or `just test`
4. Consider both web server and scraper-only modes
5. Update README.md if adding new functionality

### When Fixing Issues
1. Check current dependencies with `uv tree` (not `just info`)
2. Look at error logs from `just run` output
3. Use `just test` for faster iteration during debugging
4. Remember the app scrapes live websites with delays
5. Test both Flask endpoints and RSS generation

### When Updating Dependencies
1. Modify `pyproject.toml` dependencies section
2. Run `uv sync` directly to update lockfile
3. Test with `just quick-test`
4. Commit both `pyproject.toml` and `uv.lock`

### Container Work
- Dockerfile uses multi-stage build with uv
- Uses `uv run` for execution
- Build/push with `just build-push-container TAG`
- Container registry: `192.168.10.1:5000/ticker-rss`

## Common Patterns in This Codebase

### Web Server Architecture
- Flask application with Waitress WSGI server
- Background threading for RSS generation
- Graceful handling of missing RSS files
- JSON status endpoints for monitoring

### Error Handling
- Uses try/except for web requests and server operations
- Implements retry logic with sleep delays
- Graceful handling of missing data
- Comprehensive logging throughout

### Data Processing
- BeautifulSoup for HTML parsing
- Regex for date/title extraction
- Central Time timezone handling
- RSS generation with feedgen
- Image tag conversion for better RSS display

### Configuration
- Environment variables for runtime config
- Defaults provided for all settings
- No hardcoded paths or credentials
- Separate configuration for Flask and Waitress

## Debugging Tips

1. **Import Issues**: Use `just quick-test` to verify all dependencies
2. **Runtime Issues**: Check environment variables (TICKER_DAYS, RSS_FOLDER, DISABLE_FLASK)
3. **Network Issues**: The app makes real HTTP requests with delays
4. **Date Issues**: App uses Central Time (-6 hours from UTC)
5. **Container Issues**: Verify uv.lock is up to date
6. **Web Server Issues**: Check Flask/Waitress logs and status endpoint
7. **Threading Issues**: Background scraper runs in daemon thread

## Best Practices for AI Agents

1. **Always run `just setup`** before making changes
2. **Use `uv` commands directly** for dependency management (no justfile wrappers)
3. **Use `just quick-test`** to verify changes don't break imports
4. **Respect the existing code style** and patterns
5. **Test both web server and scraper-only modes** when making changes
6. **Update documentation** when making significant changes
7. **Test container builds** if modifying dependencies
8. **Don't remove the sleep delays** - they prevent rate limiting
9. **Preserve timezone handling** - it's specific to the data source
10. **Consider Flask endpoints** when modifying RSS generation

## File Modification Guidelines

- **pyproject.toml**: Only modify for dependency changes, version updates
- **main.py**: Main application logic, be careful with scraping patterns and Flask routes
- **justfile**: Add new composite commands, don't add simple uv wrappers
- **Dockerfile**: Only modify if changing Python version or uv usage
- **README.md**: Keep user-focused, technical details go here

## Testing Strategy

- **Unit Testing**: Not currently implemented (single script)
- **Integration Testing**: Use `just test` for real data testing
- **Dependency Testing**: Use `just quick-test`
- **Container Testing**: Build and run container locally
- **Web Server Testing**: Test all Flask endpoints manually
- **Threading Testing**: Verify background scraper works correctly

## Known Limitations

1. **Single Script**: No modular structure, everything in main.py
2. **No Tests**: Relies on manual testing and live data
3. **Network Dependent**: Requires internet access to function
4. **Time Sensitive**: Scrapes based on current date calculations
5. **Rate Limited**: Uses sleep delays to avoid overwhelming target site
6. **Threading Model**: Simple daemon thread, no sophisticated coordination
7. **No Graceful Shutdown**: Background thread terminates abruptly

## Recent Changes (For Context)

1. **Justfile Simplified**: Removed simple uv command wrappers (`add`, `remove`, `info`)
2. **Flask Integration**: Added full web server with multiple endpoints
3. **Waitress Server**: Production WSGI server for better performance
4. **Dual Mode Operation**: Web server (default) vs scraper-only modes
5. **Dependency Updates**: All dependencies updated to latest versions
6. **Python 3.13**: Minimum Python version raised from 3.8+
7. **Enhanced Logging**: Better logging throughout application
8. **Status Endpoints**: JSON API for monitoring RSS generation

## Future Improvement Ideas

- Add proper logging configuration file
- Implement graceful shutdown for background threads
- Add unit tests for date parsing and RSS generation logic
- Modularize the single script into functions/classes
- Add health check endpoints for container orchestration
- Implement retry logic with exponential backoff
- Add metrics/monitoring capabilities
- Consider async/await for better concurrency
- Add configuration file support beyond environment variables
- Implement RSS feed validation

---

This document should be updated whenever significant changes are made to the project structure, dependencies, development workflow, or application architecture.