from rest_framework import filters, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated  # IsAuthenticatedOrReadOnly
from rest_framework.settings import api_settings

from . import models as mdl
from . import permissions, serializers


class UserProfileViewSet(viewsets.ModelViewSet):
    """Обработка CRUD пользователей системы."""

    serializer_class = serializers.UserProfileSerializer
    queryset = mdl.UserProfile.objects.all()

    # Разрешить аутентификацию по token
    authentication_classes = (TokenAuthentication,)

    # Проверка какие разрешения у пользователя есть.
    permission_classes = (permissions.UpdateOwnProfile,)

    # Разрешаем поиск через query параметр search=....
    filter_backends = (filters.SearchFilter,)
    # Указываем по каким полям можем производить поиск.
    search_fields = ("name", "email")


class UserLoginApiView(ObtainAuthToken):
    """Аутентификация пользователей."""

    # Есть нюанс т.к. подцепляем стандартную систему аутентификации,
    # то на WEB интерфейсе поле для логина будет Username, а не Email.

    # Добавление классов рендера ка нашему классу.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Обработка CRUD для статусов пользователя."""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = mdl.ProfileFeedItem.objects.all()
    permission_classes = (
        # Разрешить обновлять только свой статус
        permissions.UpdateOwnStatus,
        # Разрешить на запись только аутентифицированным пользователям.
        # Чтение доступно всем пользователям. Уход от ошибки 500 для
        # anonymous пользователей.
        # IsAuthenticatedOrReadOnly,
        # Доступ только для аутентифицированных пользователей.
        IsAuthenticated,
    )

    def perform_create(self, serializer):
        """
        Переопределять поведение view на базе класса viewsets
        при создании объектов.
        """
        serializer.save(user_profile=self.request.user)
