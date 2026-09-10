from django.urls import path
from .views import TenderListCreateView,TenderDetailView,TenderQuestionView
from .views import TenderIntelligenceView
urlpatterns = [
    path("", TenderListCreateView.as_view(), name="tender-list-create"),
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

]