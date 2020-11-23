from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable

from feed.models import Article, Response, Question, Post
from adoorback.serializers import AdoorBaseSerializer
from adoorback.settings import BASE_URL
from comment.serializers import CommentFriendSerializer
from account.serializers import AuthorFriendSerializer, AuthorAnonymousSerializer

User = get_user_model()


class PostFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, obj):
        if isinstance(obj.target, Article):
            self.Meta.model = Article
            return ArticleFriendSerializer(obj.target, context=self.context).to_representation(obj.target)
        elif isinstance(obj.target, Question):
            self.Meta.model = Question
            return QuestionFriendSerializer(obj.target, context=self.context).to_representation(obj.target)
        elif isinstance(obj.target, Response):
            self.Meta.model = Response
            return ResponseFriendSerializer(obj.target, context=self.context).to_representation(obj.target)
        raise NotAcceptable(detail=None, code=404)


class PostAnonymousSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, obj):
        if isinstance(obj.target, Article):
            self.Meta.model = Article
            return ArticleAnonymousSerializer(obj.target, context=self.context).to_representation(obj.target)
        elif isinstance(obj.target, Question):
            self.Meta.model = Question
            return QuestionAnonymousSerializer(obj.target, context=self.context).to_representation(obj.target)
        elif isinstance(obj.target, Response):
            self.Meta.model = Response
            return ResponseAnonymousSerializer(obj.target, context=self.context).to_representation(obj.target)
        raise NotAcceptable(detail=None, code=404)


class ArticleFriendSerializer(AdoorBaseSerializer):
    author = serializers.HyperlinkedIdentityField(
        view_name='user-detail', read_only=True)
    author_detail = AuthorFriendSerializer(source='author', read_only=True)
    comments = CommentFriendSerializer(
        source='article_comments', many=True, read_only=True)

    class Meta(AdoorBaseSerializer.Meta):
        model = Article
        fields = AdoorBaseSerializer.Meta.fields + ['share_with_friends', 'share_anonymously',
                                                    'author', 'author_detail', 'comments']


class ArticleAnonymousSerializer(AdoorBaseSerializer):
    author_detail = AuthorAnonymousSerializer(source='author', read_only=True)

    class Meta(AdoorBaseSerializer.Meta):
        model = Article
        fields = AdoorBaseSerializer.Meta.fields + ['share_with_friends', 'share_anonymously',
                                                    'author_detail']


class QuestionBaseSerializer(AdoorBaseSerializer):
    is_admin_question = serializers.SerializerMethodField(read_only=True)

    def get_is_admin_question(self, obj):
        return obj.author.is_superuser

    class Meta(AdoorBaseSerializer.Meta):
        model = Question
        fields = AdoorBaseSerializer.Meta.fields + \
            ['selected_date', 'is_admin_question']


class ResponseBaseSerializer(AdoorBaseSerializer):
    question = QuestionBaseSerializer(read_only=True)
    question_id = serializers.IntegerField()

    class Meta(AdoorBaseSerializer.Meta):
        model = Response
        fields = AdoorBaseSerializer.Meta.fields + ['share_with_friends', 'share_anonymously',
                                                    'question', 'question_id']


class ResponseFriendSerializer(ResponseBaseSerializer):
    author = serializers.HyperlinkedIdentityField(
        view_name='user-detail', read_only=True)
    author_detail = AuthorFriendSerializer(source='author', read_only=True)
    comments = CommentFriendSerializer(
        source='response_comments', many=True, read_only=True)

    class Meta(ResponseBaseSerializer.Meta):
        model = Response
        fields = ResponseBaseSerializer.Meta.fields + \
            ['author', 'author_detail', 'comments']


class ResponseAnonymousSerializer(ResponseBaseSerializer):
    author_detail = AuthorAnonymousSerializer(source='author', read_only=True)

    class Meta(ResponseBaseSerializer.Meta):
        model = Article
        fields = ResponseBaseSerializer.Meta.fields + ['author_detail']


class ResponseResponsiveSerializer(ResponseBaseSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    author_detail = serializers.SerializerMethodField(
        source='author', read_only=True)

    def get_author_detail(self, obj):
        # TODO: need to modify after friendship implementation; are friends
        if obj.author != self.context.get('request', None).user:
            return AuthorAnonymousSerializer(obj.author).data
        return AuthorFriendSerializer(obj.author).data

    def get_author(self, obj):
        if obj.author == self.context.get('request', None).user:
            return f'{BASE_URL}/api/user/{obj.author.id}/'
        return None

    class Meta(ResponseBaseSerializer.Meta):
        model = Article
        fields = ResponseBaseSerializer.Meta.fields + \
            ['author', 'author_detail']


class QuestionResponsiveSerializer(QuestionBaseSerializer):
    """
    for questions in question feed (no responses, author profile responsive)
    """
    author = serializers.SerializerMethodField(read_only=True)
    author_detail = serializers.SerializerMethodField(
        source='author', read_only=True)

    def get_author_detail(self, obj):
        # TODO: need to modify after friendship implementation; are friends
        if obj.author != self.context.get('request', None).user:
            return AuthorAnonymousSerializer(obj.author).data
        return AuthorFriendSerializer(obj.author).data

    def get_author(self, obj):
        if obj.author == self.context.get('request', None).user:
            return f'{BASE_URL}/api/user/{obj.author.id}/'
        return None

    class Meta(QuestionBaseSerializer.Meta):
        model = Question
        fields = QuestionBaseSerializer.Meta.fields + \
            ['author', 'author_detail']


class QuestionFriendSerializer(QuestionBaseSerializer):
    """
    for questions in friend feed (no responses)

    function is redundant to `QuestionResponsiveSerializer`
    but allows for faster responses when rendering friend/anonymous feeds.
    """
    author = serializers.HyperlinkedIdentityField(
        view_name='user-detail', read_only=True)
    author_detail = AuthorFriendSerializer(source='author', read_only=True)

    class Meta(QuestionBaseSerializer.Meta):
        model = Question
        fields = QuestionBaseSerializer.Meta.fields + \
            ['author', 'author_detail']


class QuestionAnonymousSerializer(QuestionBaseSerializer):
    """
    for questions in anonymous feed (no responses)

    function is redundant to `QuestionResponsiveSerializer`
    but allows for faster responses when rendering friend/anonymous feeds.
    """
    author_detail = AuthorAnonymousSerializer(source='author', read_only=True)

    class Meta(QuestionBaseSerializer.Meta):
        model = Question
        fields = QuestionBaseSerializer.Meta.fields + ['author_detail']


class QuestionDetailAllResponsesSerializer(QuestionResponsiveSerializer):
    """
    for question detail page w/ all responses (friend + anonymous)
    """
    response_set = serializers.SerializerMethodField()

    def get_response_set(self, obj):
        responses = obj.response_set.all().filter(author_id=self.context.get('request', None).user.id) | \
            obj.response_set.all().filter(share_anonymously=True)
        return ResponseResponsiveSerializer(responses, many=True, read_only=True,
                                            context={'request': self.context.get('request', None)}).data

    class Meta(QuestionResponsiveSerializer.Meta):
        model = Question
        fields = QuestionResponsiveSerializer.Meta.fields + ['response_set']


class QuestionDetailFriendResponsesSerializer(QuestionResponsiveSerializer):
    """
    for question detail page w/ friend responses
    """
    response_set = serializers.SerializerMethodField()

    def get_response_set(self, obj):
        responses = obj.response_set.all().filter(
            author_id=self.context.get('request', None).user.id)
        return ResponseFriendSerializer(responses, many=True, read_only=True,
                                        context={'request': self.context.get('request', None)}).data

    class Meta(QuestionResponsiveSerializer.Meta):
        model = Question
        fields = QuestionResponsiveSerializer.Meta.fields + ['response_set']


class QuestionDetailAnonymousResponsesSerializer(QuestionResponsiveSerializer):
    """
    for question detail page w/ anonymous responses
    """
    response_set = serializers.SerializerMethodField()

    def get_response_set(self, obj):
        responses = obj.response_set.all().filter(share_anonymously=True)
        return ResponseAnonymousSerializer(responses, many=True, read_only=True,
                                           context={'request': self.context.get('request', None)}).data

    class Meta(QuestionResponsiveSerializer.Meta):
        model = Question
        fields = QuestionResponsiveSerializer.Meta.fields + ['response_set']
