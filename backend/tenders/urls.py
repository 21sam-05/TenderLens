from django.urls import path
from .views import TenderListCreateView,TenderDetailView

urlpatterns = [
    path("", TenderListCreateView.as_view(), name="tender-list-create"),
    path("<int:pk>/",TenderDetailView.as_view(),name="tender-detail"),
]