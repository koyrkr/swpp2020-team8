import json

from django.contrib.auth import get_user_model, authenticate, login
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer

from adoorback.permissions import IsOwnerOrReadOnly
from account.models import FriendRequest
from account.serializers import UserProfileSerializer, \
    UserFriendRequestSerializer, \
    UserFriendshipStatusSerializer, AuthorFriendSerializer
from feed.serializers import QuestionAnonymousSerializer
from feed.models import Question

User = get_user_model()


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super().__init__(content, **kwargs)


@ensure_csrf_cookie
def token_anonymous(request):
    if request.method == 'GET':
        return HttpResponse(status=204)
    else:
        return HttpResponseNotAllowed(['GET'])


def user_signup(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserProfileSerializer(data=data,
                                           context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

    return HttpResponseNotAllowed(['POST'])


def user_login(request):
    if request.method == "POST":
        try:
            req_data = json.loads(request.body)
            username = str(req_data['username'])
            password = str(req_data['password'])
        except (KeyError, TypeError, json.JSONDecodeError):
            return HttpResponseBadRequest()

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(status=204)
        return HttpResponse(status=401)

    return HttpResponseNotAllowed(['POST'])


class SignupQuestions(generics.ListAPIView):
    queryset = Question.objects.order_by('?')[:5]
    serializer_class = QuestionAnonymousSerializer
    model = serializer_class.Meta.model


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        if self.request.user.is_superuser:
            queryset = User.objects.all()
        return queryset


class CurrentUserFriendList(generics.ListAPIView):
    serializer_class = AuthorFriendSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.friends.all()


class CurrentUserProfile(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        return User.objects.get(id=self.request.user.id)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserFriendshipStatusSerializer
    permission_classes = [IsAuthenticated]


class UserSearch(generics.ListAPIView):
    serializer_class = UserFriendshipStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.GET.get('query')
        queryset = User.objects.none()
        if query:
            queryset = User.objects.filter(
                username__icontains=self.request.GET.get('query'))
        return queryset


class UserFriendDestroy(generics.DestroyAPIView):
    """
    Destroy a friendship.
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, obj):
        obj.friends.remove(self.request.user)


class UserFriendRequestList(generics.ListCreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = UserFriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(requestee=self.request.user)


class UserFriendRequestDestroy(generics.DestroyAPIView):
    serializer_class = UserFriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return FriendRequest.objects.get(requester_id=self.request.user.id,
                                         requestee_id=self.kwargs.get('pk'))


class UserFriendRequestUpdate(generics.UpdateAPIView):
    serializer_class = UserFriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return FriendRequest.objects.get(requester_id=self.kwargs.get('pk'),
                                         requestee_id=self.request.user.id)
