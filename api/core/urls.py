from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, TagDetailView, TagView, AsideView, FeedBackView, RegisterView, ProfileView

router = DefaultRouter()  # создали переменную router и сохранили в нее DefaultRouter
router.register('posts', PostViewSet, basename='posts')  # зарегистрировали в router url до нашей вьюхи PostViewSet,
                                                         # которая будет обрабатывать запросы поступающие по url api/posts.



urlpatterns = [
    path('', include(router.urls)),
    path("tags/", TagView.as_view()),
    path("tags/<slug:tag_slug>/", TagDetailView.as_view()),
    path("aside/", AsideView.as_view()),
    path("feedback/", FeedBackView.as_view()),
    path('register/', RegisterView.as_view()),
    # path('profile/', ProfileView.as_view()),
]
