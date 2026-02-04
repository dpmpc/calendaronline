# Copilot Instructions for CalendarOnline

## Repository Overview

**CalendarOnline** (pdfcalendar) is a Django-based web application that creates beautiful photo calendars as PDF files for self-printing. Users can customize calendar formats, add photos, and optionally import events from ICS files.

- **Size**: ~163 files, ~1,360 lines of Python code
- **Primary Language**: Python 3.12+ (using Django 6.0)
- **Runtime**: Django with gunicorn (production) or Django development server (local)
- **Key Libraries**: Django 6.0, fpdf2 2.8, Pillow 12, icalevents 0.3, python-dateutil, orjson, uharfbuzz
- **Frontend**: Bootstrap 5.3, jQuery 4.0, Cropper.js 1.6
- **Deployment**: Docker containers (nginx + Django app)

## Development Environment Setup

### Prerequisites
- Python 3.12+ (system uses Python 3.12.3)
- Docker 28.0.4+ (for container builds)

### Setup Steps (ALWAYS follow this exact order)

1. **Navigate to the web directory**: `cd web/`
2. **Create virtual environment**: `python3 -m venv venv` (takes ~10 seconds)
3. **Activate virtual environment**: `source venv/bin/activate`
4. **Install dependencies**: `pip install -r requirements.txt` (takes ~60 seconds)
5. **Set DEBUG mode**: `export DEBUG=1` (required for development)

### Running the Development Server

```bash
cd web
source venv/bin/activate
export DEBUG=1
python manage.py runserver
```

The server runs on http://localhost:8000 by default. IMPORTANT: The server requires DEBUG=1 environment variable for development mode.

## Build and Validation Commands

### Linting with flake8

**ALWAYS exclude venv and node_modules when running flake8.**

```bash
# Install flake8 (if not installed)
pip install flake8

# Critical errors check (syntax errors, undefined names) - MUST pass
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=venv,node_modules

# Style and complexity check (allows warnings)
flake8 . --count --exit-zero --max-complexity=10 --ignore=E501 --max-line-length=127 --statistics --exclude=venv,node_modules
```

**Known linting results**: Project code has 0 critical errors. Minor warnings exist (5 total): 1 complexity warning, 1 comment formatting, 2 trailing whitespace, 1 blank line whitespace - these are acceptable.

### Django Management Commands

```bash
cd web
source venv/bin/activate
export DEBUG=1

# Check Django configuration (ALWAYS run before making changes)
python manage.py check

# Run tests (currently 0 tests, but command works)
python manage.py test
```

### Docker Builds

**Web Application Container**:
```bash
cd web
docker build -t calendaronline .
```

**Nginx Container** (requires static files):
```bash
cd nginx
mv ../web/creator/static .
docker build -t calendaronline-nginx .
```

## Project Structure and Architecture

### Directory Layout

```
/
├── .github/
│   ├── workflows/
│   │   ├── lint.yml        # CI: Runs flake8 on every push
│   │   └── release.yml     # CI: Builds/publishes Docker images on tags
│   └── dependabot.yml      # Auto-updates for pip packages
├── nginx/
│   ├── Dockerfile          # Nginx reverse proxy container
│   ├── nginx.conf          # Main nginx config
│   └── calendaronline.nginx.conf  # App-specific nginx config
├── web/                    # Main Django application
│   ├── calendaronline/     # Django project settings
│   │   ├── settings.py     # Django configuration (DEBUG, ALLOWED_HOSTS, etc.)
│   │   ├── urls.py         # Root URL configuration
│   │   └── wsgi.py         # WSGI application entry point
│   ├── creator/            # Main Django app (calendar creation)
│   │   ├── views.py        # HTTP request handlers
│   │   ├── urls.py         # App URL patterns
│   │   ├── fotocalendar/   # Core calendar generation logic
│   │   │   ├── creator.py  # Factory functions for calendar formats
│   │   │   ├── fotocalendar.py  # Base FotoCalendar class (PDF generation)
│   │   │   ├── icsparser.py     # ICS file parser for events
│   │   │   ├── bo/
│   │   │   │   └── config.py    # CalendarConfig (serialization/deserialization)
│   │   │   └── templates/       # Calendar format implementations
│   │   │       ├── landscape.py, portrait.py, design1.py, vintage.py, etc.
│   │   ├── static/         # Frontend assets (Bootstrap, jQuery, Cropper.js, FontAwesome)
│   │   └── templates/      # Django HTML templates
│   ├── files/
│   │   ├── font/           # Custom fonts (Pacifico, NotoSansDisplay, etc.)
│   │   └── images/         # Example images
│   ├── manage.py           # Django management script
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Multi-stage Docker build
│   └── startup.prod.sh     # Production entrypoint script (gunicorn wrapper)
├── update_preview_images.sh  # Script to generate calendar preview images
└── README.md
```

### Key Architectural Components

1. **Views** (`web/creator/views.py`): HTTP handlers for index, options, month selection, calendar creation
2. **Calendar Factory** (`web/creator/fotocalendar/creator.py`): Creates format-specific calendar instances (L, P, PF, LF, 1, V, 26, LM)
3. **PDF Generation** (`web/creator/fotocalendar/fotocalendar.py`): Base class using fpdf2 and Pillow for PDF rendering
4. **Configuration** (`web/creator/fotocalendar/bo/config.py`): Serializes/deserializes calendar settings (JSON format)
5. **Calendar Templates** (`web/creator/fotocalendar/templates/`): Format-specific implementations (Landscape, Portrait, Design1, Vintage, Design2026, LandscapeModern)

### URL Patterns

- `/` or `/start`: Landing page
- `/options`: Calendar format selection
- `/month`: Month-by-month photo upload
- `/create`: Generate PDF (POST)
- `/preview`: Generate preview PDF
- `/load`: Load saved project file
- `/impressum`, `/faq`: Info pages

### Environment Variables

- `DEBUG`: Set to `1` for development mode (default: 0)
- `SECRET_KEY`: Django secret key (auto-generated if not set)
- `CSRF_TRUSTED_ORIGINS`: Trusted origins for CSRF (default: http://localhost:8000)
- `GUNICORN_PORT`: Gunicorn bind port (default: 8001)
- `GUNICORN_BIND`, `GUNICORN_HOST`, `GUNICORN_WORKERS`, `GUNICORN_ARGS`: Gunicorn configuration

## GitHub Actions CI/CD

### Lint Workflow (`lint.yml`)
**Triggers**: On every push to any branch

**Steps**:
1. Checkout code
2. Set up Python 3.14 with pip caching
3. Install dependencies: `pip install -r web/requirements.txt`
4. Install flake8: `pip install flake8`
5. Run critical checks: `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
6. Run style checks: `flake8 . --count --exit-zero --max-complexity=10 --ignore=E501 --max-line-length=127 --statistics`

**To replicate locally**: Follow the "Linting with flake8" section above.

### Release Workflow (`release.yml`)
**Triggers**: On push of tags matching `v*` (e.g., v1.0.0)

**Steps**:
1. Extract version from tag
2. Build nginx Docker image (copies static files from web/creator/static)
3. Build app Docker image (injects version into web/creator/templates/creator/version.html)
4. Push both images to ghcr.io with `latest` and version tags

## Important Development Notes

### Virtual Environment
- **ALWAYS exclude `venv/` from all operations** (linting, git commits, grep searches)
- The `.gitignore` file includes `venv/` and `**/__pycache__/**`

### Django Settings
- `settings.py` uses environment variables for configuration
- `ALLOWED_HOSTS` includes: localhost, 127.0.0.1, [::1], nginx
- Default language: German (`de-DE`)
- No database is used (stateless application)
- `STATIC_ROOT = BASE_DIR / 'static'` for production static file collection

### Fonts and Static Files
- Custom fonts are stored in `web/files/font/` (TrueType format)
- Static files (CSS, JS, images) are in `web/creator/static/`
- Font files are large (~100MB total), NOT committed to web/creator/static

### Common Pitfalls and Solutions

1. **ImportError**: If you see "Couldn't import Django", activate the virtual environment first
2. **flake8 showing many errors**: Add `--exclude=venv,node_modules` to exclude dependencies
3. **Server won't start**: Ensure `DEBUG=1` is set and you're in the `web/` directory
4. **Static files missing in Docker**: For nginx container, static files must be moved from web/creator/static to nginx/static before build

## Quick Reference Commands

```bash
# Setup (once)
cd web && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Development (every session)
cd web && source venv/bin/activate && export DEBUG=1 && python manage.py runserver

# Lint before commit
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=venv,node_modules

# Django checks
cd web && source venv/bin/activate && export DEBUG=1 && python manage.py check
```

## Trust These Instructions

These instructions have been validated by running all commands in the repository. ONLY search for additional information if:
- You encounter an error not documented here
- The repository structure has changed significantly
- You need to understand specific calendar generation logic not covered here

For all standard tasks (setup, linting, testing, running), trust these instructions and execute them as documented.
