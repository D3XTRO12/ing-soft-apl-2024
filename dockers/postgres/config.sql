DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'pablo') THEN
      CREATE ROLE pablo WITH LOGIN PASSWORD 'pablo001';
   END IF;
END
$do$;

DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'proyect_ing_soft_dev') THEN
      CREATE DATABASE proyect_ing_soft_dev;
      GRANT ALL PRIVILEGES ON DATABASE proyect_ing_soft_dev TO pablo;
   END IF;
END
$do$;