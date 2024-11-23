from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Разрешить редактировать только собственные профайлы пользователей."""

    def has_object_permission(self, request, view, obj):
        """Проверка, что пользователь редактирует свой профайл."""

        # Если метод безопасный GET или POST, то проверка не нужна.
        # Мы разрешаем пользователя просматривать аккаунты друг друга.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверка, что ID объекта равен ID пользователя.
        # Если совпадает, то разрешаем, иначе запрещаем.
        # Т.к. пользователь пытается изменить не свой профайл.
        return obj.id == request.user.id


class UpdateOwnStatus(permissions.BasePermission):
    """Разрешить редактировать только собственные статусы пользователя."""

    def has_object_permission(self, request, view, obj):
        """Проверка, что пользователь редактирует свой статус."""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id
