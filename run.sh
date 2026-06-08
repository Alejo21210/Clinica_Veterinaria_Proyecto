#!/bin/bash
cd "$(dirname "$0")"
.venv/bin/python manage.py runserver 0.0.0.0:8000 --noreload
