from datetime import datetime
from uuid import UUID
from uuid import UUID

from pydantic import ConfigDict, BaseModel


#from typing import Optional


class Receipt(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    rec_id: UUID
    ord_id: str
    type: str
    customer_info: str
    create_date: str
    rec: str


class CreateReceiptRequest(BaseModel):
    ord_id: str
    type: str
    rec: str
    customer_info: str
