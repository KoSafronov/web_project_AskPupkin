from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=14)
    password = models.CharField(max_length=20)
    avatar = models.CharField
    created_at = models.CharField

    pass

'''
Table users {
  id int [pk, increment]
  username varchar [pk]
  password varchar
  avatar varchar
  created_at datetime
  updated_at datetime

}
'''

class Question(models.Model):
    pass
'''
Table questions {
  id int [pk, increment]
  author_id int
  tag varchar
  likes_num int 
  created_at datetime

}
'''

class Answer(models.Model):
    pass
'''
Table answers {
  id int [pk, increment]
  question_id varchar
  author_id int
  tag varchar
  correction bool 
  created_at datetime
}
'''


class Tag(models.Model):
    pass
'''
Table tags {
  tag_name varchar [pk]
}
'''

class Like(models.Model):
    pass
'''
Table likes {
  id int [pk, increment]
  user_id int
  created_at datetime
  updated_at datetime
}
'''


'''

Ref: "likes"."user_id" < "users"."id"

Ref: "questions"."likes_num" < "likes"."id"

Ref: "questions"."tag" < "tags"."tag_name"

Ref: "answers"."tag" < "tags"."tag_name"

Ref: "answers"."id" < "questions"."id"

Ref: "questions"."author_id" < "users"."id"

Ref: "answers"."author_id" < "users"."id"

'''