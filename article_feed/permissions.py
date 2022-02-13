from rest_framework.permissions import IsAuthenticated
from .models import Article


class OnlyAuthor(IsAuthenticated):
    """
    Разрешает доступ только автору на создание.
    """

    def has_permission(self, request, view):
        if Article.objects.filter(author_id=request.user.id):
            return bool(request.user and request.user.is_authenticated)


class OnlySelfAuthor(IsAuthenticated):
    """
    Разрешает доступ только автору на редактирование и  удаление.
    """

    def has_permission(self, request, view):
        if Article.objects.filter(author_id=request.user.id, id=view.kwargs['pk']):
            return bool(request.user and request.user.is_authenticated)
