from django.urls import path, include, re_path
from .views import basic


urlpatterns = [
    path("", basic.IndexView.as_view()),
    path(r"<int:pk>/download/", basic.DownloadView.as_view()),
    path("survey/<int:pk>/", basic.SurveyDetailView.as_view(), name="survey_detail")

]
