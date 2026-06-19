import csv
from io import StringIO

from app.models.transaction import Transaction


class ExportService:
    @staticmethod
    def transactions_to_csv(transactions: list[Transaction]) -> str:
        output = StringIO()

        writer = csv.writer(output)

        writer.writerow(
            [
                "id",
                "title",
                "amount",
                "type",
                "category",
                "created_at",
            ]
        )

        for transaction in transactions:
            writer.writerow(
                [
                    transaction.id,
                    transaction.title,
                    transaction.amount,
                    transaction.type.value,
                    transaction.category,
                    transaction.created_at.isoformat(),
                ]
            )

        return output.getvalue()