from rest_framework import serializers

from .models import ProfileFeedItem, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя системы."""

    def create(self, validated_data):
        """Создание пользователя системы."""

        user = UserProfile.objects.create_user(
            # Квадратные скобки для обязательных параметров.
            # Позволяет сразу отловить ошибку не переданных данных.
            email=validated_data["email"],
            name=validated_data["name"],
            password=validated_data["password"],
        )
        return user

    def update(self, instance, validated_data):
        """Обновление пользователя системы."""

        # Перехватывание пароля и замена его на хэш пароля.
        # Для методов PUT и PATCH.
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)

        user = super().update(instance, validated_data)
        return user

    class Meta:
        model = UserProfile
        fields = ("id", "email", "name", "password")
        extra_kwargs = {
            "password": {
                # Поле доступно только при записи или изменении.
                # Пароль не должен возвращаться в ответе сервера.
                "write_only": True,
                "style": {
                    # Закрыть пароль звездочками в интерфейсе
                    "input_type": "password",
                },
            }
        }


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Сериализатор модели статуса пользователя системы."""

    class Meta:
        model = ProfileFeedItem
        fields = ("id", "user_profile", "status_text", "created_on")
        extra_kwargs = {
            "user_profile": {
                # Значение только для чтения. Для записи пользователь
                # берется из данных аутентифицированного запроса.
                "read_only": True,
            }
        }
