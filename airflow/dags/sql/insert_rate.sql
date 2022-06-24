INSERT INTO
    exchange_rates
VALUES ('{{ params.base_currency }}', 
{{ ti.xcom_pull(task_ids=params.get_rate_task_id)[0] }}, 
{{ ti.xcom_pull(task_ids=params.get_rate_task_id)[1] }},
{{ ti.xcom_pull(task_ids=params.get_rate_task_id)[2] }},
{{ ti.xcom_pull(task_ids=params.get_rate_task_id)[3] }},
'{{ execution_date.strftime("%Y-%m-%d") }}')
