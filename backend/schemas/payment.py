from pydantic import BaseModel
from decimal import Decimal

class PaymentRequest(BaseModel):
    amount: Decimal
    payment_mode: str
    order_id: int

class PaymentResponse(BaseModel):
    transaction_id: str
    status: str
    message: str
