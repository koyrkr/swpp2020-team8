from rest_framework import generics
from rest_framework import permissions

from feed.serializers import ArticleSerializer, ResponseSerializer, \
    QuestionSerializer, QuestionDetailSerializer, PostSerializer
from feed.models import Article, Response, Question, Post
from adoorback.permissions import IsAuthorOrReadOnly


class DailyQuestionList(generics.ListAPIView):
    queryset = Question.objects.all().filter(id__lte=30)
    serializer_class = QuestionSerializer
    model = serializer_class.Meta.model
    permission_classes = [permissions.IsAuthenticated]


class ArticleList(generics.ListCreateAPIView):
    """
    List all articles, or create a new article.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or destroy an article.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]


class QuestionList(generics.ListCreateAPIView):
    """
    List all questions, or create a new question.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or destroy a question.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]


class ResponseList(generics.ListCreateAPIView):
    """
    List all responses, or create a new response.
    """
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ResponseDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or destroy a response.
    """
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]


class PostList(generics.ListCreateAPIView):
    """
    List all posts
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class FriendFeedPostList(generics.ListCreateAPIView):
    """
    List friend feed posts
    """
    queryset = Post.objects.friend_posts_only()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class AnonymousFeedPostList(generics.ListCreateAPIView):
    """
    List anonymous feed posts
    """
    queryset = Post.objects.anonymous_posts_only()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
