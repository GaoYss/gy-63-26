from pydantic import BaseModel


class NewMemberItem(BaseModel):
    id: int
    name: str
    phone: str
    level_id: int
    created_at: str


class RedeemItem(BaseModel):
    id: int
    member_id: int
    member_name: str
    change: int
    note: str
    created_at: str


class PresaleOrderItem(BaseModel):
    id: int
    member_id: int
    member_name: str
    presale_id: int
    presale_title: str
    quantity: int
    amount: float
    created_at: str


class RecommendationItem(BaseModel):
    id: int
    name: str
    category: str
    freshness_score: int
    origin: str
    price: float
    reason: str


class NewMemberSummary(BaseModel):
    count: int
    items: list[NewMemberItem]


class RedeemSummary(BaseModel):
    count: int
    total_points: int
    items: list[RedeemItem]


class PresaleSummary(BaseModel):
    order_count: int
    total_quantity: int
    total_amount: float
    items: list[PresaleOrderItem]


class RecommendationSummary(BaseModel):
    count: int
    items: list[RecommendationItem]


class DailyReport(BaseModel):
    report_date: str
    new_members: NewMemberSummary
    redeems: RedeemSummary
    presales: PresaleSummary
    recommendations: RecommendationSummary
