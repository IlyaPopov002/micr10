from typing import Optional
from uuid import UUID

from app.models.receipt import Receipt

# receipts: list[Receipt] = [
#     Receipt(rec_id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'), ord_id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'),
#              type='test_rec_type_1', create_date=datetime.datetime.now(), rec='test_rec_rec_1',
#              customer_info='test_customer_info_0'),
#     Receipt(rec_id=UUID('45309954-8e3c-4635-8066-b342f634252c'), ord_id=UUID('45309954-8e3c-4635-8066-b342f634252c'),
#              type='test_rec_type_2', create_date=datetime.datetime.now(), rec='test_rec_rec_2',
#              customer_info='test_customer_info_1'),
# ]

receipts = []


class ReceiptRepo():
    def __init__(self, clear: bool = False) -> None:
        if clear:
            receipts.clear()

    def get_receipt(self) -> list[Receipt]:
        return receipts

    # def get_rec_by_id(self, id: UUID) -> Receipt:
    #     for d in receipts:
    #         if d.id == id:
    #             return d
    #
    #     raise KeyError

    def get_receipt_by_id(self, id: UUID) -> Receipt:
        for d in receipts:
            if d.rec_id == id:
                return d

        raise KeyError

    def create_receipt(self, rec: Receipt) -> Receipt:
        if len([d for d in receipts if d.rec_id == rec.rec_id]) > 0:
            raise KeyError

        receipts.append(rec)
        return rec

    def delete_rec(self, id: UUID) -> Optional[Receipt]:
        for i, receipt in enumerate(receipts):
            if receipt.rec_id == id:
                deleted_receipt = receipts.pop(i)
                return deleted_receipt

        return None


