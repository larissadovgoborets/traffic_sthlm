# Data ingestion to Snowflake via dlt

1. Install dlt

    ```bash
    uv pip install "dlt[snowflake]"
    ```

2. Initialize pipeline by running in the extract_load directory

    ```bash
    dlt init extract_from_sl snowflake
    ```

3. Change the credentials in the secrets.toml file in the .dlt directory.
