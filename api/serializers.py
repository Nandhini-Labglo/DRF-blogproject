from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Comment, Post

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    password = serializers.CharField(
        min_length=8, max_length=32, write_only=True)
    email = serializers.EmailField(max_length=50, allow_blank=False)
    token = serializers.SerializerMethodField('get_user_token')

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "token"]

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj

    def get_user_token(self, obj):
        return Token.objects.get_or_create(user=obj)[0].key


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "description", "body", "image"]


post_detail_url = serializers.HyperlinkedIdentityField(
    view_name='api:post_detail',
    lookup_field='id'
)


class PostListSerializer(serializers.ModelSerializer):

    url = post_detail_url
    comments = serializers.HyperlinkedIdentityField(
        view_name="api:comment_detail", read_only=True, many=True)

    class Meta:
        model = Post
        fields = ["id", "url", "title", "user",
                  "image", "description", "comments"]


class PostDetailSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = serializers.HyperlinkedIdentityField(
        view_name="api:comment_detail", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "description", "body",
                  "user", "image", "created_at", "updated_at", "comments"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "user", "body", "created_at", "updated_at", ]


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ["body","post","user"]
