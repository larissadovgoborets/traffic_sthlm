USE ROLE useradmin;
CREATE ROLE IF NOT EXISTS traffic_sthlm_dbt_role;

GRANT ROLE traffic_sthlm_dbt_role TO USER transformer;
GRANT ROLE traffic_sthlm_dbt_role TO USER simon;
GRANT ROLE traffic_sthlm_dbt_role TO USER larissa;

USE ROLE securityadmin;

-- Setup Marts layer
GRANT USAGE,
CREATE TABLE,
CREATE VIEW ON SCHEMA traffic_data_sthlm_db.marts TO ROLE traffic_sthlm_dbt_role;

-- grant CRUD and select tables and views
GRANT SELECT,
INSERT,
UPDATE,
DELETE ON ALL TABLES IN SCHEMA traffic_data_sthlm_db.marts TO ROLE traffic_sthlm_dbt_role;
GRANT SELECT ON ALL VIEWS IN SCHEMA traffic_data_sthlm_db.marts TO ROLE traffic_sthlm_dbt_role;

-- grant CRUD and select on future tables and views
GRANT SELECT,
INSERT,
UPDATE,
DELETE ON FUTURE TABLES IN SCHEMA traffic_data_sthlm_db.marts TO ROLE traffic_sthlm_dbt_role;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA traffic_data_sthlm_db.marts TO ROLE traffic_sthlm_dbt_role;
USE ROLE traffic_sthlm_dbt_role;

SHOW GRANTS ON SCHEMA traffic_data_sthlm_db.marts;

-- manual test
USE SCHEMA traffic_data_sthlm_db.marts;
CREATE TABLE test (id INTEGER);
SHOW TABLES;
DROP TABLE TEST;

-- Setup Warehouse layer
USE ROLE securityadmin;

GRANT ROLE traffic_sthlm_dlt_role TO ROLE traffic_sthlm_dbt_role;

SHOW GRANTS TO ROLE traffic_sthlm_dbt_role;

GRANT USAGE,
CREATE TABLE,
CREATE VIEW ON SCHEMA traffic_data_sthlm_db.warehouse TO ROLE traffic_sthlm_dbt_role;

-- grant CRUD and select tables and views
GRANT SELECT,
INSERT,
UPDATE,
DELETE ON ALL TABLES IN SCHEMA traffic_data_sthlm_db.warehouse TO ROLE traffic_sthlm_dbt_role;
GRANT SELECT ON ALL VIEWS IN SCHEMA traffic_data_sthlm_db.warehouse TO ROLE traffic_sthlm_dbt_role;

-- grant CRUD and select on future tables and views
GRANT SELECT,
INSERT,
UPDATE,
DELETE ON FUTURE TABLES IN SCHEMA traffic_data_sthlm_db.warehouse TO ROLE traffic_sthlm_dbt_role;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA traffic_data_sthlm_db.warehouse TO ROLE traffic_sthlm_dbt_role;
USE ROLE traffic_sthlm_dbt_role;


SHOW GRANTS ON SCHEMA traffic_data_sthlm_db.warehouse;

-- manual test
USE SCHEMA traffic_data_sthlm_db.warehouse;
CREATE TABLE test (id INTEGER);
SHOW TABLES;
DROP TABLE TEST;