from rest_framework import status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, ArticleSerializer
from rest_framework import viewsets
from .models import User, Article
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from .permissions import OnlyAuthor, OnlySelfAuthor


class UserRegistrationView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'success': 'True', 'user': f'{serializer.data["email"]}'}, status=status.HTTP_201_CREATED,
                        headers=headers)


class ArticleView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes_by_action = {'create': (OnlyAuthor,),
                                    'list': (IsAuthenticatedOrReadOnly,)}

    def list(self, request, *args, **kwargs):
        if self.request.user.id:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            queryset = Article.objects.filter(is_locked='False')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'success': 'True', 'article': f'{serializer.data["title"]}'},
                        status=status.HTTP_201_CREATED, headers=headers)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class ArticleDetailView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes_by_action = {
        'retrieve': (IsAuthenticatedOrReadOnly,),
        'partial_update': (OnlySelfAuthor,),
        'update': (OnlySelfAuthor,),
        'destroy': (OnlySelfAuthor,),
    }

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not self.request.user.id and Article.objects.get(id=kwargs['pk']).is_locked:
            return Response({'error': 'Закрытая статья'})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
