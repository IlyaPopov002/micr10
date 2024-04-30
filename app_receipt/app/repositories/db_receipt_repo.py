import traceback
from uuid import UUID

from sqlalchemy.orm import Session

from app.database import get_db_rec
from app.models.receipt import Receipt
from app.schemas.receipt import Receipt as DBReceipt


class ReceiptRepo():
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db_rec())

    def _map_to_model(self, receipt: DBReceipt) -> Receipt:
        result = Receipt.from_orm(receipt)

        return result

    def _map_to_schema(self, receipt: Receipt) -> DBReceipt:
        data = dict(receipt)
        result = DBReceipt(**data)

        return result

    def get_receipt(self) -> list[Receipt]:
        receipts = []
        for d in self.db.query(DBReceipt).all():
            receipts.append(self._map_to_model(d))

        return receipts

    def get_receipt_by_id(self, id: UUID) -> Receipt:
        receipt = self.db \
            .query(DBReceipt) \
            .filter(DBReceipt.rec_id == id) \
            .first()

        if receipt == None:
            raise KeyError
        return self._map_to_model(receipt)

    def create_receipt(self, receipt: Receipt) -> Receipt:
        try:
            db_receipt = self._map_to_schema(receipt)
            self.db.add(db_receipt)
            self.db.commit()
            return self._map_to_model(db_receipt)
        except:
            traceback.print_exc()
            raise KeyError

    def delete_all_receipt(self) -> None:
        try:
            # Delete all orders from the database
            self.db.query(DBReceipt).delete()
            self.db.commit()
        except Exception as e:
            print(f"An error occurred while deleting all receipt: {e}")
            self.db.rollback()
            raise

    def delete_receipt_by_id(self, id: UUID) -> Receipt:
        try:
            # Find the order by its ord_id
            receipt = self.db.query(DBReceipt).filter(DBReceipt.rec_id == id).one()

            # If the order is found, map it to the model and commit the deletion
            if receipt:
                deleted_receipt = self._map_to_model(receipt)
                self.db.delete(receipt)
                self.db.commit()
                return deleted_receipt
            else:
                # Handle the case where no order is found
                raise ValueError(f"No order found with ord_id {id}")
        except Exception as e:
            # Rollback any changes if there's an error
            self.db.rollback()
            # Re-raise the exception so it can be handled elsewhere
            raise e
