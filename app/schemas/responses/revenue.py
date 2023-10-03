from pydantic import BaseModel
from datetime import date
from typing import Union


class RevenueProduct(BaseModel):
    product: str
    total_revenue: float


class RevenueCategory(BaseModel):
    category: str
    total_revenue: float


class RevenueTimePeriod(BaseModel):
    time_period: str
    total_revenue: Union[float, int]


class RevenueDaily(BaseModel):
    date: date
    total_revenue: float


class RevenueWeekly(BaseModel):
    week: str
    total_revenue: float


class RevenueMonthly(BaseModel):
    month: str
    total_revenue: float


class RevenueAnnual(BaseModel):
    year: str
    total_revenue: float
