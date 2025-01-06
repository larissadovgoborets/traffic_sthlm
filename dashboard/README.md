# Dashboard

To run the dashboard in docker, be sure to have docker installed, navigate into the dashboard directory and run the following command:

```bash
docker build -t traffic_sthlm_dashboard .

docker run --env-file .env -p 8056:8056 traffic_sthlm_dashboard
```

You can also use following command to pull the latest image from docker hub and run it:

```bash
docker pull larissadovgoborets/traffic_sthlm_dashboard:latest

docker run --env-file .env -p 8056:8056 larissadovgoborets/traffic_sthlm_dashboard:latest
```

[!NOTE] you need to have a .env file in the dashboard directory with the following content:

```bash
SNOWFLAKE_DATABASE=<snowflake_database>
SNOWFLAKE_ACCOUNT=<snowflake_account>
SNOWFLAKE_USER=<snowflake_user>
SNOWFLAKE_PASSWORD=<snowflake_password>
SNOWFLAKE_WAREHOUSE=<snowflake_warehouse>
SNOWFLAKE_SCHEMA=<snowflake_schema>
SNOWFLAKE_ROLE=<snowflake_role>
```

Be sure not to have any spaces in the .env file.

The dashboard will be available at ```http://localhost:8056```.
