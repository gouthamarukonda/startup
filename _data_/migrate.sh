#!/usr/bin/env bash
rm -rf ../*/migrations
python manage.py makemigrations chapter institute paper question student teacher userprofile program approval attempt
python manage.py migrate
python populateDatabase.py
