-- Platform smoke model. `dbt run --select hyhome_dbt_connectivity` proves the
-- connection and the CREATE VIEW privilege in the target schema without
-- reading application data. Business models declare their own sources.
select
    current_database() as database_name,
    current_user as dbt_user,
    current_schema() as target_schema
