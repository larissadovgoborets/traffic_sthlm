USE ROLE SYSADMIN;

CREATE WAREHOUSE IF NOT EXISTS traffic_sthlm_wh
WITH
WAREHOUSE_SIZE = 'XSMALL'
AUTO_SUSPEND = 60
AUTO_RESUME = TRUE
INITIALLY_SUSPENDED = TRUE
COMMENT = 'Warehouse for analysis of traffic data in Stockholm';    

SHOW WAREHOUSES;

CREATE DATABASE IF NOT EXISTS traffic_data_sthlm_db;

CREATE SCHEMA IF NOT EXISTS traffic_data_sthlm_db.staging;

CREATE SCHEMA IF NOT EXISTS traffic_data_sthlm_db.marts;

CREATE SCHEMA IF NOT EXISTS traffic_data_sthlm_db.warehouse;

SHOW SCHEMAS IN traffic_data_sthlm_db;