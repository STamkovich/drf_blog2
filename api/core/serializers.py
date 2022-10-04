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
