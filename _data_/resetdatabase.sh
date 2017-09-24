#!/usr/bin/env bash
psql -h localhost -p 5432 -U avinash -d portal -c "DROP SCHEMA public CASCADE;"
psql -h localhost -p 5432 -U avinash -d portal -c "CREATE SCHEMA public AUTHORIZATION avinash;"
psql -h localhost -p 5432 -U avinash -d portal -c "GRANT ALL ON SCHEMA public TO avinash;"
psql -h localhost -p 5432 -U avinash -d portal -c "GRANT ALL ON SCHEMA public TO public;"
psql -h localhost -p 5432 -U avinash -d portal -c "COMMENT ON SCHEMA public IS 'standard public schema';"
