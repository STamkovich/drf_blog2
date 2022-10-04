from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from taggit.models import Tag

from .serializers import PostSerializer, TagSerializer, ContactSerailizer
from .models import Post
from rest_framework.response import Response
from rest_framework import pagination


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'  # если установлено, это строковое значение, указывающее имя параметра запроса, которое позволяет клиенту устанавливать размер страницы для каждого запроса. Это значит, что мы можем через запрос управлять размером страницы.
    ordering = 'created_at'


class PostViewSet(
    viewsets.ModelViewSet):  # viewsets.ModelViewSet позволяют нам объединить все вышеописанное в одну вьюху.
    # Она будет отвечать и за то чтобы отдавать список всех записей и за то, чтобы отдавать одну конкретную запись.
    serializer_class = PostSerializer  # мы создаем определяем сериалайзер для работы с моделью Post.
    queryset = Post.objects.all()  # определяем queryset который мы будем возвращать:
    lookup_field = 'slug'  # указываем поле по которому будем получать одну конкретную запись
    permission_classes = [
        permissions.AllowAny]  # добавиk к нашей вьюхе такие права, чтобы любой пользователь, без токена, мог получить список постов.
    pagination_class = PageNumberSetPagination  # Указывая параметр pagination_class мы как бы говорим вьюхе - используй эту пагинацию для вывода списка постов.


class TagDetailView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PageNumberSetPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return Post.objects.filter(tags=tag)


class TagView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class AsideView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-id')[:3]
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]


class FeedBackView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactSerailizer

    def post(self, request, *args, **kwargs):
        serializer_class = ContactSerailizer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            name = data.get('name')
            from_email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(f'От {name} | {subject}', message, from_email, ['amromashov@gmail.com'])
            return Response({"success": "Sent"})