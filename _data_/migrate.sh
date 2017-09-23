rm -rf ../*/migrations
python manage.py makemigrations answer chapter institute paper question student teacher userprofile program approval attempt
python manage.py migrate
python populateDatabase.py
