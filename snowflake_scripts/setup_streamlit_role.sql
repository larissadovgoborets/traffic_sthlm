USE ROLE useradmin;
CREATE ROLE IF NOT EXISTS traffic_sthlm_reporter_role;

USE ROLE securityadmin;

GRANT USAGE ON WAREHOUSE traffic_sthlm_wh TO ROLE traffic_sthlm_reporter_role;

GRANT USAGE ON DATABASE traffic_data_sthlm_db TO ROLE traffic_sthlm_reporter_role;
GRANT USAGE ON SCHEMA traffic_data_sthlm_db.marts TO ROLE traffic_sthlm_reporter_role;
GRANT SELECT ON ALL TABLES IN SCHEMA traffic_data_sthlm_db.marts TO ROLE traffic_sthlm_reporter_role;
GRANT SELECT ON ALL VIEWS IN SCHEMA traffic_data_sthlm_db.marts TO ROLE traffic_sthlm_reporter_role;
GRANT SELECT ON FUTURE TABLES IN SCHEMA traffic_data_sthlm_db.marts TO ROLE traffic_sthlm_reporter_role;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA traffic_data_sthlm_db.marts TO ROLE traffic_sthlm_reporter_role;


GRANT ROLE traffic_sthlm_reporter_role TO USER reporter;
GRANT ROLE traffic_sthlm_reporter_role TO USER simon;
GRANT ROLE traffic_sthlm_reporter_role TO USER larissa;

USE ROLE traffic_sthlm_reporter_role;

SHOW GRANTS TO ROLE traffic_sthlm_reporter_role;

-- test querying a mart
USE WAREHOUSE traffic_sthlm_wh;
-- SELECT * FROM traffic_data_sthlm_db.marts.mart_job_listings;