from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(
    prefix="profiles",
    viewset=views.UserProfileViewSet,
    # Имя данному маршруту. Для автоматической генерации ссылок на
    # views в нашем API, если определи QuerySet, то не обязательно.
    # Позволяет не описывать вручную endpoints, это делает роутер.
    # basename="profiles"
)
router.register(
    prefix="feed",
    viewset=views.UserProfileFeedViewSet,
)


urlpatterns = [
    path("", include(router.urls)),
    path("login/", views.UserLoginApiView.as_view()),
]
