USE ROLE USERADMIN;

CREATE ROLE IF NOT EXISTS traffic_sthlm_dlt_role;
-- design: one user for EL and several roles for 
-- loading to several databases
GRANT ROLE traffic_sthlm_dlt_role TO USER simon;
GRANT ROLE traffic_sthlm_dlt_role TO USER larissa;

USE ROLE SECURITYADMIN;

-- can have different ingestions tools e.g. dlt, airbyte, fivetran, ...
GRANT ROLE traffic_sthlm_dlt_role TO USER extract_loader;

GRANT USAGE ON WAREHOUSE traffic_sthlm_wh TO ROLE traffic_sthlm_dlt_role;
GRANT USAGE ON DATABASE traffic_data_sthlm_db TO ROLE traffic_sthlm_dlt_role;
GRANT USAGE ON SCHEMA traffic_data_sthlm_db.staging TO ROLE traffic_sthlm_dlt_role;
GRANT CREATE TABLE ON SCHEMA traffic_data_sthlm_db.staging TO ROLE traffic_sthlm_dlt_role;

GRANT SELECT, INSERT,
UPDATE,
DELETE ON ALL TABLES IN SCHEMA traffic_data_sthlm_db.staging TO ROLE traffic_sthlm_dlt_role;
GRANT SELECT, INSERT,
UPDATE,
DELETE ON FUTURE TABLES IN SCHEMA traffic_data_sthlm_db.staging TO ROLE traffic_sthlm_dlt_role;

-- check grants
SHOW GRANTS ON SCHEMA traffic_data_sthlm_db.staging;
SHOW FUTURE GRANTS IN SCHEMA traffic_data_sthlm_db.staging;

SHOW GRANTS TO ROLE traffic_sthlm_dlt_role;

SHOW GRANTS TO USER extract_loader;

