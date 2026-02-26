# Django Boilerplate

A Django boilerplate with REST framework, JWT authentication, and CORS support. Uses **Poetry** for dependency management.

---

## Requirements

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation)

---

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/sujit-dhakal/django-boilerplate-code.git
cd django-boilerplate-code

# 2. Install dependencies
poetry install

# 3. Activate the virtual environment
poetry shell

# 4. Copy env file and configure it
cp .env.example .env

# 5. Run migrations
python manage.py migrate

# 6. Start the dev server
python manage.py runserver
```

---

## Managing Packages with Poetry

### Add a package

```bash
poetry add package-name
```

Examples:

```bash
poetry add celery
poetry add pillow
poetry add django-filter
```

### Add a dev-only package

```bash
poetry add --group dev package-name
```

Examples:

```bash
poetry add --group dev black
poetry add --group dev pytest-django
```

### Remove a package

```bash
poetry remove package-name
```

### Update a package

```bash
poetry update package-name
```

### Update all packages

```bash
poetry update
```

### Show installed packages

```bash
poetry show
```

---

## Docker

```bash
# Development
docker-compose up --build

# Production
docker-compose -f docker-compose.prod.yml up --build
```

---

## Pre-commit Hooks

```bash
poetry run pre-commit install
```