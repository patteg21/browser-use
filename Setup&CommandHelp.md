# Browser Use Project Setup & Command Help

This document contains the complete setup process and troubleshooting steps for getting the Browser Use project running with a renamed package structure.

## Project Overview

- **Original Package Name**: `browser_use`
- **Renamed Package Name**: `browser_user`
- **Framework**: AI-powered browser automation using Playwright/Chromium
- **LLM Integration**: Azure OpenAI GPT-4o
- **Python Version**: 3.12
- **Environment**: Virtual environment with uv package manager

## Prerequisites

1. Python 3.12 installed
2. Virtual environment activated
3. Azure OpenAI API credentials
4. Browser Use dependencies installed

## Initial Issues Encountered

### 1. Import Errors Due to Package Rename
**Problem**: The package was renamed from `browser_use` to `browser_user`, but import statements throughout the codebase still referenced the old name.

**Error Messages**:
```
ModuleNotFoundError: No module named 'browser_use'
RuntimeError: Failed to load system prompt template: No module named 'browser_use'
```

### 2. Missing Playwright Browsers
**Problem**: Playwright browser binaries were not installed.

**Error Messages**:
```
FileNotFoundError [Errno 2] No such file or directory: '/home/herschelle/.cache/ms-playwright/chromium-1181/chrome-linux/chrome'
```

### 3. Domain Pattern Configuration
**Problem**: Incorrect domain pattern format for allowed domains.

**Error Messages**:
```
⛔️ Only *.domain style patterns are supported
⛔️ Navigation to non-allowed URL
```

## Setup Steps

### Step 1: Fix Import References

Fixed all references from `browser_use` to `browser_user` in the following files:

#### Main Package Initialization
**File**: `browser_user/__init__.py`
- Updated lazy import mappings in `_LAZY_IMPORTS` dictionary
- Fixed all module paths to use `browser_user` namespace

#### System Prompt Loading
**File**: `browser_user/agent/prompts.py`
- Fixed resource loading path:
```python
# Before:
with importlib.resources.files('browser_use.agent').joinpath(template_filename).open('r', encoding='utf-8') as f:

# After:
with importlib.resources.files('browser_user.agent').joinpath(template_filename).open('r', encoding='utf-8') as f:
```

#### LLM Module Mappings
**File**: `browser_user/llm/__init__.py`
- Updated all lazy import paths in `_LAZY_IMPORTS`
- Fixed module references from `browser_use.llm.*` to `browser_user.llm.*`

#### Telemetry Module
**File**: `browser_user/telemetry/__init__.py`
- Updated lazy import mappings
- Fixed module references to use `browser_user` namespace

### Step 2: Install Playwright Browsers

**Command**:
```bash
playwright install chromium
```

**What this installs**:
- Chromium 139.0.7258.5 (playwright build v1181)
- FFMPEG playwright build v1011
- Chromium Headless Shell 139.0.7258.5

**Installation location**: `/home/herschelle/.cache/ms-playwright/`

### Step 3: Fix Domain Configuration

**File**: `browser_user/__main__.py`

**Before**:
```python
allowed_domains = [
    "https://us.cwcloudpartner.com/das-develop-aqa/e/eng/bp_-b5BDTgOsAmkIzK-f2w/*"
]
```

**After**:
```python
allowed_domains = [
    "*.cwcloudpartner.com"
]
```

## Running the Project

### Basic Command
```bash
python3 -m browser_user
```

### Environment Variables Required
Set these environment variables for Azure OpenAI:
```bash
export AZURE_OPENAI_API_KEY="your-api-key"
export AZURE_OPENAI_API_ENDPOINT="your-endpoint"
export AZURE_OPENAI_API_VERSION="your-api-version"
export DAS_EMAIL="your-email"
export DAS_PASSWORD="your-password"
```

## Project Structure

```
browser_user/
├── __init__.py              # Main package initialization with lazy imports
├── __main__.py              # Main execution script
├── agent/
│   ├── prompts.py          # System prompt template loading
│   └── ...
├── llm/
│   ├── __init__.py         # LLM provider lazy loading
│   └── ...
├── telemetry/
│   ├── __init__.py         # Telemetry module imports
│   └── ...
└── ...
```

## Files Modified During Setup

1. `browser_user/__init__.py` - Fixed lazy import mappings
2. `browser_user/agent/prompts.py` - Fixed resource loading path
3. `browser_user/llm/__init__.py` - Updated module references
4. `browser_user/telemetry/__init__.py` - Fixed module mappings
5. `browser_user/__main__.py` - Corrected domain pattern

## Verification Commands

### Check Package Imports
```bash
python3 -c "from browser_user import Agent, BrowserSession, BrowserProfile; print('Imports successful')"
```

### Check Playwright Installation
```bash
playwright --version
```

### Test Browser Launch
```bash
python3 -m browser_user
```

## Expected Output

When running successfully, you should see:
```
INFO [browser_user.telemetry.service] Anonymized telemetry enabled
INFO [browser_user.agent.service] Starting a browser-use agent 0.5.6
INFO [browser_use.BrowserSession] Launching new local browser playwright:chromium
INFO [browser_user.utils] Extensions ready: 3 extensions loaded
INFO [browser_use.BrowserSession] Connecting to newly spawned browser
```

## Troubleshooting

### Import Errors
- Ensure all `browser_use` references are changed to `browser_user`
- Check lazy import mappings in `__init__.py` files
- Verify module paths in resource loading calls

### Browser Launch Failures
- Run `playwright install chromium` to install browser binaries
- Check that Chromium is installed in `/home/herschelle/.cache/ms-playwright/`

### Domain Access Issues
- Use wildcard domain patterns like `*.domain.com`
- Avoid full URL patterns with protocols and paths

### Module Not Found Errors
- Check that all import statements use the correct package name
- Verify that lazy import dictionaries are updated
- Ensure resource file paths are correct

## Key Features Working

✅ **Browser Automation**: Playwright/Chromium integration
✅ **AI Agent**: GPT-4o integration for intelligent web interactions  
✅ **Extensions**: uBlock Origin, I still don't care about cookies, ClearURLs
✅ **Domain Security**: Allowed domain restrictions
✅ **File System**: Agent can read/write files for data extraction
✅ **Logging**: Comprehensive logging and telemetry
✅ **Cloud Integration**: Browser Use Cloud integration

## Development Notes

- The project uses lazy imports for performance optimization
- Extensions are automatically downloaded and configured
- The agent creates temporary file system directories for each session
- Azure OpenAI integration provides vision capabilities for screenshot analysis
- Domain restrictions prevent unauthorized site access
- Cloud telemetry is enabled by default but can be disabled

## Success Metrics

- ✅ All import errors resolved
- ✅ Playwright browsers installed and functional
- ✅ Browser launches successfully with extensions
- ✅ Agent connects to Azure OpenAI
- ✅ Website navigation works within domain restrictions
- ✅ AI reasoning and task execution functional
- ✅ File system operations working
- ✅ Comprehensive logging enabled
