from rest_framework import serializers

from .models import List, Group, Comment, Post, Attachment

from users.serializers import CustomUserSerializer

class GroupSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)

    class Meta:
        model = Group
        fields = "__all__"


class ListReadSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    group = GroupSerializer(read_only=True)

    class Meta:
        model = List
        fields = "__all__"

class ListWriteSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = List
        fields = "__all__"

class AttachmentReadSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)

    class Meta:
        model = Attachment
        #fields = "__all__"
        exclude = ['post']

class AttachmentWriteSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Attachment
        fields = "__all__"

class PostReadSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    list = ListReadSerializer(read_only=True)
    attachments = AttachmentReadSerializer(many=True, read_only=True)

    def get_likes(self, obj):
        likes = list(
            like.username for like in obj.likes.get_queryset().only("username")
        )
        return likes

    class Meta:
        model = Post
        fields = "__all__"

class PostWriteSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    

    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


