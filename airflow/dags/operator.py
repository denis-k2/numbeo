from typing import Any

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

from .hook import CurrencyScoopHook


class CurrencyScoopOperator(BaseOperator):

    @apply_defaults
    def __init__(
            self,
            base_currency: str,
            conn_id: str = 'pg_k2',
            **kwargs) -> None:
        super().__init__(**kwargs)
        self.conn_id = conn_id
        self.base_currency = base_currency

    def execute(self, context: Any):
        api = CurrencyScoopHook(self.conn_id)
        return api.get_rate(context['execution_date'].date(), self.base_currency)
