import random
import logging
import sys
from datetime import timedelta, datetime
import pytz

import pandas as pd
from django.contrib.auth import get_user_model
from faker import Faker

from adoorback.utils.content_types import get_content_type
from account.models import Friendship, FriendRequest
from feed.models import Article, Response, Question
from comment.models import Comment
from like.models import Like

DEBUG = False


def set_question_seed():
    df = pd.read_csv('adoorback/assets/questions.csv')

    User = get_user_model()
    admin = User.objects.get(username='adoor')

    for i in df.index:
        content = df.at[i, 'content']
        Question.objects.create(author=admin, is_admin_question=True, content=content)

    def date_range(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    start_date = datetime(2020, 9, 1, 0, 0, 0, tzinfo=pytz.UTC)
    end_date = datetime(2020, 11, 22, 0, 0, 0, tzinfo=pytz.UTC)
    for single_date in date_range(start_date, end_date):
        questions = Question.objects.filter(
            selected_date__isnull=True).order_by('?')[:30]
        # reset if we run out of questions to select from
        if questions.count() < 30:
            Question.objects.update(selected_date=None)
        questions |= Question.objects.filter(
            selected_date__isnull=True).order_by('?')[:(30 - questions.count())]
        for question in questions:
            question.selected_date = single_date
            question.save()


def set_mock_seed():
    if DEBUG:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    User = get_user_model()
    faker = Faker(locale='ko_KR')

    # Seed Superuser
    if User.objects.count() == 0:
        User.objects.create_superuser(
            username='adoor', email='adoor.team@gmail.com', password='adoor2020:)',
            question_history=",".join(map(str, faker.random_elements(
                                                  elements=range(1, 1501),
                                                  length=random.randint(3, 10),
                                                  unique=True))))
    logging.info("Superuser created!") if DEBUG else None

    # Seed User
    for i in range(100):
        User.objects.create_user(username=faker.user_name() + str(i),
                                 email=faker.email(),
                                 password=faker.password(),
                                 question_history=",".join(map(str,
                                                               faker.random_elements(
                                                                   elements=range(1, 1501),
                                                                   length=random.randint(3, 10),
                                                                   unique=True))))
    logging.info(
        f"{User.objects.count()} User(s) created!") if DEBUG else None

    # Seed Article/AdminQuestion/CustomQuestionPost
    users = User.objects.all()
    for _ in range(1000):
        user = random.choice(users)
        article = Article.objects.create(author=user,
                                         content=faker.bs(),
                                         share_with_friends=random.choice([True, False]),
                                         share_anonymously=random.choice([True, False]))
        if not article.share_anonymously and not article.share_with_friends:
            article.share_with_friends = True
            article.save()
    for _ in range(500):
        user = random.choice(users)
        Question.objects.create(
            author=user, is_admin_question=False, content=faker.bs())
    logging.info(
        f"{Article.objects.count()} Article(s) created!") if DEBUG else None
    logging.info(f"{Question.objects.count()} Question(s) created!") \
        if DEBUG else None
    set_question_seed()

    # Seed Response
    questions = Question.objects.all()
    for _ in range(2000):
        user = random.choice(users)
        question = random.choice(questions)
        response = Response.objects.create(author=user, content=faker.catch_phrase(), question=question,
                                           share_with_friends=random.choice([True, False]),
                                           share_anonymously=random.choice([True, False]))
        if not response.share_anonymously and not response.share_with_friends:
            response.share_with_friends = True
            response.save()
    logging.info(
        f"{Response.objects.count()} Response(s) created!") if DEBUG else None

    # Seed Comment (target=Feed)
    articles = Article.objects.all()
    responses = Response.objects.all()
    for _ in range(5000):
        user = random.choice(users)
        article = random.choice(articles)
        response = random.choice(responses)
        Comment.objects.create(author=user, target=article,
                               content=faker.catch_phrase(), is_private=_ % 2)
        Comment.objects.create(author=user, target=response,
                               content=faker.catch_phrase(), is_private=_ % 2)
    logging.info(
        f"{Comment.objects.count()} Comment(s) created!") if DEBUG else None

    # Seed Reply Comment (target=Comment)
    comment_model = get_content_type("Comment")
    comments = Comment.objects.all()
    for _ in range(15000):
        user = random.choice(users)
        comment = random.choice(comments)
        reply = Comment.objects.create(author=user, target=comment,
                                       content=faker.bs(), is_private=comment.is_private)
        if reply.target.is_private:
            reply.is_private = True
            reply.save()
    logging.info(f"{Comment.objects.filter(content_type=comment_model).count()} Repl(ies) created!") \
        if DEBUG else None

    # Seed Feed Like
    for i in range(3000):
        user = random.choice(users)
        article = Article.objects.get(id=i % 1000 + 1)
        question = Question.objects.get(id=i % 1500 + 1)
        response = Response.objects.get(id=i % 2000 + 1)
        Like.objects.get_or_create(user=user, content_type=get_content_type("Article"), object_id=article.id)
        Like.objects.get_or_create(user=user, content_type=get_content_type("Question"), object_id=question.id)
        Like.objects.get_or_create(user=user, content_type=get_content_type("Response"), object_id=response.id)

    # Seed Comment Like
    for i in range(10000):
        user = random.choice(users)
        comment = Comment.objects.comments_only()[i % 5000]
        reply = Comment.objects.replies_only()[i % 15000]
        Like.objects.get_or_create(user=user, content_type=get_content_type("Comment"), object_id=comment.id)
        Like.objects.get_or_create(user=user, content_type=get_content_type("Comment"), object_id=reply.id)
    logging.info(
        f"{Like.objects.count()} Like(s) created!") if DEBUG else None

    # Seed Friend Request
    for i in range(1000):
        user_1 = random.choice(users)
        user_2 = random.choice(users.exclude(id=user_1.id))

        FriendRequest.objects.get_or_create(user=user_1, friend=user_2)

    for i in range(500):
        user_1 = random.choice(users)
        user_2 = random.choice(users.exclude(id=user_1.id))

        Friendship.objects.get_or_create(user=user_1, friend=user_2)
