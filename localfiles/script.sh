psql -h localhost -U avinash -d portal -c "DROP SCHEMA public CASCADE;"
psql -h localhost -U avinash -d portal -c "CREATE SCHEMA public AUTHORIZATION avinash;"
psql -h localhost -U avinash -d portal -c "GRANT ALL ON SCHEMA public TO avinash;"
psql -h localhost -U avinash -d portal -c "GRANT ALL ON SCHEMA public TO public;"
psql -h localhost -U avinash -d portal -c "COMMENT ON SCHEMA public IS 'standard public schema';"
rm -rf ../src/*/migrations
python ../src/manage.py makemigrations answer chapter institute paper question student teacher userprofile program approval attempt
python ../src/manage.py migrate
python ../src/populateDatabase.py