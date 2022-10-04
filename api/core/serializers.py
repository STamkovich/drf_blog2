from rest_framework import serializers
from .models import Post
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from django.contrib.auth.models import User
from taggit.models import Tag


#  TaggitSerializer здесь использован, только из-за того что в нашей модели есть теги.
class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:  # Мета класс и внутри него указывается на какой модели основан сериализатор.
        model = Post
        fields = ("id", "h1", "title", "slug", "description", "content", "image", "created_at", "author",
                  "tags")  # перечисляем какие поля нам нужны из модели.
        lookup_field = 'slug'  # переопределили по какому полю мы будем получать конкретную запись.
        # По умолчанию запись можно получить по id, но мы намеренно изменили это поле на slug.
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        #  Существует также shortcut, позволяющий указать произвольные дополнительные аргументы ключевых слов в полях,
        #  используя опцию extra_kwargs. Как и в случае с read_only_fields, это означает,
        #  что вам не нужно явно объявлять поле в сериализаторе.


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)
        lookup_field = 'name'
        extra_kwargs = {
            'url': {
                lookup_field: 'name'
            }
        }


class ContactSerailizer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    subject = serializers.CharField()
    message = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)  # write_only Установите это значение True, чтобы поле можно было использовать при обновлении или создании экземпляра, но оно не включалось при сериализации представления.

    class Meta:    # модель на основе которой создаем сериализатор и указываем поля, который будут доступны для нашей апишки:
        model = User
        fields = [
            "username",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data): # метод create. Он нужен для сохранения инстансов - для создания пользователей
        username = validated_data["username"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer): # сериализатор, который возвращает нам все данные о пользователе
    class Meta:
        model = User
        fields = '__all__'