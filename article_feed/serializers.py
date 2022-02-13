from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, Article
import re


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'role')

    def validate(self, attrs):
        if len(self.initial_data['password']) < 8:
            raise serializers.ValidationError({'error': 'Пароль должен быть не короче 8 символов'})
        if not re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z!@#$%^&*]{8,}$').match(
                self.initial_data['password']):
            raise serializers.ValidationError({
                'error': 'Пароль должен содержать хотя бы одну цифру и букву любого регистра'})
        return attrs

    def create(self, validated_data):
        if not validated_data.get('role'):
            validated_data['role'] = 'S'
        user = User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            role=validated_data.get('role'),
        )
        return user


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = 'title', 'content', 'is_locked'

    def create(self, validated_data):
        article = Article.objects.create(
            title=validated_data.get('title'),
            content=validated_data.get('content'),
            is_locked=validated_data.get('is_locked'),
            author_id=self.context['request'].user.id,
        )
        return article
