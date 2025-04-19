from django.urls import path
from .views import RegisterStudentView, LoginStudentView, CandidateListView, VolunteerCandidateView, UserView

urlpatterns = [
    path("register/", RegisterStudentView.as_view(), name="register"),
    path("login/", LoginStudentView.as_view(), name="login"),
    path("candidates/", CandidateListView.as_view(), name="candidates"),
    path("volunteer/", VolunteerCandidateView.as_view(), name="volunteer"),
    path("user/", UserView.as_view(), name="user"),
]