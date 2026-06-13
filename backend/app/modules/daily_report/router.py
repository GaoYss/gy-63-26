from fastapi import APIRouter, Query

from app.modules.daily_report.models import DailyReport
from app.modules.daily_report.service import get_daily_report

router = APIRouter()


@router.get("", response_model=DailyReport)
def get_report(report_date: str | None = Query(default=None, description="报告日期，格式 YYYY-MM-DD，默认今天")) -> DailyReport:
    return get_daily_report(report_date)
