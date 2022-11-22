from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework import viewsets
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
)
from .permissions import IsOwnerOrReadOnly, IsOwner
from .serializers import (
    CommentCreateUpdateSerializer,
    CommentSerializer,
    LoginSerializer,
    UserSerializer,
    PostCreateUpdateSerializer,
    PostDetailSerializer,
    PostListSerializer
)
from .models import Comment, Post

# Create your views here.

User = get_user_model()


class LoginAPI(ListAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data["username"]
        password = request.data["password"]
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=username, password=password)
            print(user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })


class RegisterAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]
    serializer_class = UserSerializer


class CreatePostAPIView(APIView):
    """
    post:
        Creates a new post instance. Returns created post data
        parameters: [title, body, description, image]
    """

    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        serializer = PostCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)


class ListPostAPIView(ListAPIView):
    """
    get:
        Returns a list of all existing posts
    """

    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DetailPostAPIView(RetrieveUpdateDestroyAPIView):
    """
    get:
        Returns the details of a post instance. Searches post using id field.
    put:
        Updates an existing post. Returns updated post data
        parameters: [id, title, body, description, image]
    delete:
        Delete an existing post
        parameters = [id]
    """

    queryset = Post.objects.all()
    lookup_field = "id"
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CreateCommentAPIView(APIView):
    """
    post:
        Create a comment instance. Returns created comment data
        parameters: [id, body]
    """

    serializer_class = CommentCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, id, *args, **kwargs):
        post = get_object_or_404(Post, id=id)
        serializer = CommentCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)


class ListCommentAPIView(APIView):
    """
    get:
        Returns the list of comments on a particular post
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        post = Post.objects.get(id=id)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data, status=200)


class DetailCommentAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
