from django.urls import path, include
from .views import (
    CreateCommentAPIView,
    CreatePostAPIView,
    DetailCommentAPIView,
    DetailPostAPIView,
    ListCommentAPIView,
    ListPostAPIView,
    LoginAPI,
    RegisterAPI,
)
from rest_framework.routers import DefaultRouter

app_name = "api"

router = DefaultRouter()
router.register(r'register', RegisterAPI) #-----------------> User-register

urlpatterns = [

    #login
    path("login/", LoginAPI.as_view(), name="login"),

    #post
    path("", ListPostAPIView.as_view(), name="list_post"),
    path("create/", CreatePostAPIView.as_view(), name="create_post"),
    path("<int:id>/", DetailPostAPIView.as_view(), name="post_detail"),

    #comment
    path("<int:id>/comment/", ListCommentAPIView.as_view(), name="list_comment"),
    path("<int:id>/comment/create/",
         CreateCommentAPIView.as_view(), name="create_comment"),
    path("comment/<int:pk>/", DetailCommentAPIView.as_view(), name="comment_detail"),

    #router
    path('router/', include(router.urls)),

]