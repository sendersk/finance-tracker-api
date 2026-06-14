from pydantic import BaseModel


class BalanceResponse(BaseModel):
    total_income: float
    total_expense: float
    balance: float


class CategorySummary(BaseModel):
    category: str
    total_amount: float


class MonthlySummaryResponse(BaseModel):
    month: int
    year: int
    total_income: float
    total_expense: float
    balance: float