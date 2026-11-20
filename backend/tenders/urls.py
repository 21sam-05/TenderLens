from django.urls import path
from .views import (
    TenderListCreateView,
    TenderDetailView,
    TenderQuestionView,
    TenderIntelligenceView,
    BidReadinessView,
    BidAnalysisView,
    TenderOverView,TenderDashboardStatsView,
    TenderRiskView 
)
urlpatterns = [
    path("", TenderListCreateView.as_view(), name="tender-list-create"),

    path(
        "dashboard-stats/",
        TenderDashboardStatsView.as_view(),
        name="tender-dashboard-stats",
    ),
    path("<int:pk>/",TenderDetailView.as_view(),name="tender-detail"),
    path(
    "<int:tender_id>/ask/",
    TenderQuestionView.as_view(),
    name="tender-question"),
    path(
    "<int:tender_id>/intelligence/",
    TenderIntelligenceView.as_view(),
    name="tender-intelligence"
    ),
    path(
    "<int:tender_id>/readiness/",
    BidReadinessView.as_view(),
    name="bid-readiness"
    ),
    path(
        "<int:tender_id>/bid-analysis/",
        BidAnalysisView.as_view(),
        name="bid-analysis"
    ),
    path("<int:tender_id>/overview/",
         TenderOverView.as_view(),
         name="tender-overview"),

    path(
    "<int:tender_id>/risk/",
    TenderRiskView.as_view(),
    name="tender-risk"
),

    

]