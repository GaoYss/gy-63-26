from datetime import date

from app.core.store import store
from app.modules.daily_report.models import (
    DailyReport,
    NewMemberItem,
    NewMemberSummary,
    PresaleOrderItem,
    PresaleSummary,
    RecommendationItem,
    RecommendationSummary,
    RedeemItem,
    RedeemSummary,
)
from app.modules.recommendations.service import list_recommendations


def _member_name(member_id: int) -> str:
    member = store.members.get(member_id)
    return member["name"] if member else "未知会员"


def _presale_title(presale_id: int) -> str:
    presale = store.presales.get(presale_id)
    return presale["title"] if presale else "未知预售"


def get_daily_report(report_date: str | None = None) -> DailyReport:
    target_date = report_date or date.today().strftime("%Y-%m-%d")

    new_member_items = []
    for member in store.members.values():
        if member.get("created_at") == target_date:
            new_member_items.append(
                NewMemberItem(
                    id=member["id"],
                    name=member["name"],
                    phone=member["phone"],
                    level_id=member["level_id"],
                    created_at=member["created_at"],
                )
            )

    redeem_items = []
    total_redeem_points = 0
    for record in store.point_records:
        if record["type"] == "redeem" and record["created_at"].startswith(target_date):
            redeem_items.append(
                RedeemItem(
                    id=record["id"],
                    member_id=record["member_id"],
                    member_name=_member_name(record["member_id"]),
                    change=record["change"],
                    note=record["note"],
                    created_at=record["created_at"],
                )
            )
            total_redeem_points += abs(record["change"])

    presale_items = []
    total_presale_quantity = 0
    total_presale_amount = 0.0
    for order in store.presale_orders:
        if order.get("created_at", "").startswith(target_date):
            presale_items.append(
                PresaleOrderItem(
                    id=order["id"],
                    member_id=order["member_id"],
                    member_name=_member_name(order["member_id"]),
                    presale_id=order["presale_id"],
                    presale_title=_presale_title(order["presale_id"]),
                    quantity=order["quantity"],
                    amount=order["amount"],
                    created_at=order.get("created_at", ""),
                )
            )
            total_presale_quantity += order["quantity"]
            total_presale_amount += order["amount"]

    recommendations = list_recommendations()
    recommendation_items = [
        RecommendationItem(
            id=r.id,
            name=r.name,
            category=r.category,
            freshness_score=r.freshness_score,
            origin=r.origin,
            price=r.price,
            reason=r.reason,
        )
        for r in recommendations
    ]

    return DailyReport(
        report_date=target_date,
        new_members=NewMemberSummary(
            count=len(new_member_items),
            items=new_member_items,
        ),
        redeems=RedeemSummary(
            count=len(redeem_items),
            total_points=total_redeem_points,
            items=redeem_items,
        ),
        presales=PresaleSummary(
            order_count=len(presale_items),
            total_quantity=total_presale_quantity,
            total_amount=round(total_presale_amount, 2),
            items=presale_items,
        ),
        recommendations=RecommendationSummary(
            count=len(recommendation_items),
            items=recommendation_items,
        ),
    )
