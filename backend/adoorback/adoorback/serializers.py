from rest_framework import serializers
from django.contrib.auth import get_user_model

from feed.models import Article, Response, Question
from comment.models import Comment

User = get_user_model()


class AdoorBaseSerializer(serializers.ModelSerializer):
    author = serializers.HyperlinkedIdentityField(view_name='user-detail', read_only=True)
    author_detail = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    current_user_liked = serializers.SerializerMethodField(read_only=True)

    def get_author_detail(self, obj):
        author = obj.author
        return {
            "id": author.id,
            "username": author.username,
        }

    def get_like_count(self, obj):
        if isinstance(obj, Article):
            return obj.article_likes.all().count()
        elif isinstance(obj, Question):
            return obj.question_likes.all().count()
        elif isinstance(obj, Response):
            return obj.response_likes.all().count()
        elif isinstance(obj, Comment):
            return obj.comment_likes.all().count()

    def get_current_user_liked(self, obj):
        current_user = self.context['request'].user
        if isinstance(obj, Article):
            return obj.article_likes.all().filter(user=current_user).count() > 0
        elif isinstance(obj, Question):
            return obj.question_likes.all().filter(user=current_user).count() > 0
        elif isinstance(obj, Response):
            return obj.response_likes.all().filter(user=current_user).count() > 0
        elif isinstance(obj, Comment):
            return obj.comment_likes.all().filter(user=current_user).count() > 0

    class Meta:
        model = None
        fields = ['id', 'type', 'author', 'author_detail', 'content',
                  'like_count', 'current_user_liked', 'created_at', 'updated_at']