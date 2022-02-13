from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyClientManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email должен быть установлен')
        if not password:
            raise ValueError('Пароль должен быть установлен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    """
    Пользователь
    """

    role_choices = [
        ('S', 'Subscriber'),
        ('A', 'Author'),
    ]

    email = models.EmailField(max_length=255, unique=True, verbose_name='Почта')
    password = models.CharField(max_length=128, verbose_name='Пароль')
    role = models.CharField(max_length=1, choices=role_choices, default='S', help_text='Subscriber or Author',
                            verbose_name='Роль')
    is_superuser = models.BooleanField(default=False, help_text='У этого пользователя есть все разрешения',
                                       verbose_name='Суперпользователь')

    objects = MyClientManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    is_locked = models.BooleanField(default=False, verbose_name='Закрытая статья')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='author', verbose_name='Автор статьи')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
