from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=14)
    password = models.CharField(max_length=20)
    avatar = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pass


class Question(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text_space = models.TextField()
    likes_sum = models.Sum()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pass


class Answer(models.Model):
    STATUS_CHOICES = [("cr", "Correct"), ("noinf", "NoInformation")]
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text_space = models.TextField()
    correction = models.CharField(choices=STATUS_CHOICES, max_length=15)
    likes_sum = models.Sum()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pass


class Tag(models.Model):
    name = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pass

class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    pass

class link_like(models.Model):
    obj_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    like_id = models.ForeignKey(Like, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    pass

class link_tag(models.Model):

    obj_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    pass


'''
class link_like(models.Model):
    obj_id = models.ForeignKey((Question, Answer), on_delete=models.SET_NULL)
    like_id = models.ForeignKey(Like, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    pass


class link_tag(models.Model):
    OBJ_CHOICES = {
        "Q":"Question",
        "A":"Answer",
    }
    obj_id = models.ForeignKey(choices=OBJ_CHOICES, on_delete=models.SET_NULL)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    pass





'''