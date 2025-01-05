from pathlib import Path

from dagster_dbt import DbtProject

dbt_code_project = DbtProject(
    project_dir=Path(__file__).joinpath("..", "..", "..").resolve(),
    packaged_project_dir=Path(__file__).joinpath("..", "..", "dbt_project.yml").resolve(),


)
dbt_code_project.prepare_if_dev()