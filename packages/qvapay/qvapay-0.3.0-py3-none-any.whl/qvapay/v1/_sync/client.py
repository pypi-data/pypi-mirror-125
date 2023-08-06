from dataclasses import dataclass, field
from typing import Union
from uuid import UUID

from httpx._config import DEFAULT_TIMEOUT_CONFIG
from httpx._types import TimeoutTypes

from ..auth import QvaPayAuth
from ..http_clients import SyncClient
from ..models.info import Info
from ..models.invoice import Invoice
from ..models.paginated_transactions import PaginatedTransactions
from ..models.transaction_detail import TransactionDetail
from ..utils import validate_response


@dataclass
class SyncQvaPayClient:
    """
    Creates a QvaPay client.
    * app_id: QvaPay app id.
    * app_secret: QvaPay app secret.
    Get your app credentials at: https://qvapay.com/apps/create
    """

    app_id: str
    app_secret: str
    timeout: TimeoutTypes = field(default=DEFAULT_TIMEOUT_CONFIG)

    def __post_init__(self):
        self.auth_params = {"app_id": self.app_id, "app_secret": self.app_secret}
        self.base_url = "https://qvapay.com/api/v1"
        self.http_client = SyncClient(
            base_url=self.base_url,
            params=self.auth_params,
            timeout=self.timeout,
        )

    def __enter__(self) -> "SyncQvaPayClient":
        return self

    def __exit__(self, exc_t, exc_v, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        self.http_client.aclose()

    @staticmethod
    def from_auth(
        auth: QvaPayAuth,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    ) -> "SyncQvaPayClient":
        return SyncQvaPayClient(auth.qvapay_app_id, auth.qvapay_app_secret, timeout)

    def get_info(self) -> Info:
        """
        Get info relating to your QvaPay app.
        https://qvapay.com/docs/1.0/app_info
        """
        response = self.http_client.get("info")
        validate_response(response)
        return Info.from_json(response.json())

    def get_balance(self) -> float:
        """
        Get your QvaPay balance.
        https://qvapay.com/docs/1.0/balance
        """
        response = self.http_client.get("balance")
        validate_response(response)
        return float(response.json())

    def get_transactions(self, page: int = 1) -> PaginatedTransactions:
        """
        Gets transactions list, paginated by 50 items per request.
        * page: Page to be fetched.
        https://qvapay.com/docs/1.0/transactions
        """
        response = self.http_client.get("transactions", params={"page": page})
        validate_response(response)
        return PaginatedTransactions.from_json(response.json())

    def get_transaction(self, id: Union[str, UUID]) -> TransactionDetail:
        """
        Gets a transaction by its id (uuid).
        * id: Transaction uuid returned by QvaPay when created.
        https://qvapay.com/docs/1.0/transaction
        """
        response = self.http_client.get(f"transaction/{id}")
        validate_response(response)
        return TransactionDetail.from_json(response.json())

    def create_invoice(
        self,
        amount: float,
        description: str,
        remote_id: str,
        signed: bool = False,
    ) -> Invoice:
        """
        Creates an invoice.
        * amount: Amount of money to receive to your wallet, expressed in dollars with
          two decimals.
        * description: Description of the invoice to be created, useful to show info to
          the user who pays. Max 300 chars.
        * remote_id: Invoice ID on your side (example: in your e-commerce store).
          Optional.
        * signed: Generates a signed URL, valid for 30 minutes. Useful to increase
          security, introducing an expiration datetime. Optional.
        https://qvapay.com/docs/1.0/create_invoice
        """
        params = {
            "amount": amount,
            "description": description,
            "remote_id": remote_id,
            "signed": int(signed),
        }
        response = self.http_client.get("create_invoice", params=params)
        validate_response(response)
        return Invoice.from_json(response.json())
