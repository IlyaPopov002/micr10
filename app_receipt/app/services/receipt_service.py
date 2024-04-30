# 1. Поменять int на UUID в функциях

from datetime import datetime
from uuid import UUID, uuid4

from fastapi import Depends

from app.models.receipt import Receipt
from app.repositories.db_receipt_repo import ReceiptRepo


#from app.repositories.local_receipt_repo import ReceiptRepo


# from app.repositories.local_deliveryman_repo import DeliverymenRepo


class ReceiptService():
    order_repo: ReceiptRepo

    # deliveryman_repo: DeliverymenRepo

    def __init__(self, receipt_repo: ReceiptRepo = Depends(ReceiptRepo)) -> None:
        self.receipt_repo = receipt_repo
        # self.deliveryman_repo = DeliverymenRepo()

    def get_receipt(self) -> list[Receipt]:
        return self.receipt_repo.get_receipt()
    
    def get_receipt_by_id(self, id: UUID) -> Receipt:
        return self.receipt_repo.get_receipt_by_id(id)

    def create_receipt(self, ord_id: str, type: str, rec: str, customer_info: str) -> Receipt:
        receipt = Receipt(rec_id=uuid4(), ord_id=ord_id, type=type, create_date=str(datetime.now().date()),
                          rec=rec, customer_info=customer_info)

        return self.receipt_repo.create_receipt(receipt)

    def delete_receipt(self, rec_id: UUID) -> None:
        return self.receipt_repo.delete_receipt_by_id(rec_id)
    

