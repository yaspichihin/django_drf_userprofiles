from django.conf import settings
# Для переопределения стандартной модели пользователя
from django.contrib.auth import models as auth_models
from django.db import models


class UserManagerManager(auth_models.BaseUserManager):
    """Менеджер для пользователей системы."""

    def create_user(
        self,
        email: str,
        name: str,
        password=None,
    ) -> "UserProfile":
        """
        Создание нового пользователя.

        Поле password опциональное т.к. есть случаи когда требуется
        задать пароль при первом входе в систему. Или используется
        автоматическая аутентификация через OAuth.
        """

        if not email:
            raise ValueError("Не указан email для пользователя.")

        if not name:
            raise ValueError("Не указано имя для пользователя.")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        # Задать хэш переданного пароля
        user.set_password(password)

        # Сохраняем пользователя и указываем в какой БД его сохранить.
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        email: str,
        name: str,
        password: str,
    ) -> "UserProfile":
        """
        Создание нового супер пользователя системы.
        """

        if not email:
            raise ValueError("Не указан email для супер пользователя.")

        if not name:
            raise ValueError("Не указано имя для супер пользователя.")

        if not name:
            raise ValueError("Не указан пароль для супер пользователя.")

        user = self.create_user(
            email=email,
            name=name,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    """Модель пользователя системы."""

    email = models.EmailField(
        verbose_name="Email Пользователя",
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        verbose_name="Имя пользователя",
        max_length=255,
    )
    is_active = models.BooleanField(
        verbose_name="Активен ли пользователь",
        default=True,
    )
    is_staff = models.BooleanField(
        verbose_name="Является ли пользователь администратором",
        default=False,
    )

    # Создание собственного менеджера. Чтобы приложение понимало как
    # работать с нашей моделью. А именно создание пользователей и
    # суперпользователей с логином в поле mail.
    objects = UserManagerManager()

    # Переопределим поле для аутентификации
    USERNAME_FIELD = "email"

    # Определим поля при создании createsuperuser
    REQUIRED_FIELDS = ["name"]

    # Дополнительные методы для удобства
    def get_full_name(self):
        """Обычно тут закладывается логика Фамилия + Имя + Отчество."""
        return self.name

    def get_short_name(self):
        """Обычно тут закладывается логика Фамилия + И. + О.."""
        return self.name

    def __str__(self):
        """Для корректного отображения в консоли и админки."""
        return self.email


class ProfileFeedItem(models.Model):
    """Хранение статусов профилей и их изменение."""

    user_profile = models.ForeignKey(
        # Связь с settings.AUTH_USER_MODEL.
        # Если сменится модель пользователя не потребуется менять привязку.
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    status_text = models.CharField(
        verbose_name="Текст статуса",
        max_length=255,
    )
    created_on = models.DateTimeField(
        verbose_name="Дата создания статуса",
        auto_now_add=True,
    )

    def __str__(self):
        return self.status_text
