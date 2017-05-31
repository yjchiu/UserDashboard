from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def reg(self,postData):
        if not EMAIL_REGEX.match(postData['email']):
            return {'error' : 'Invalid Format'}
        elif len(postData['first_name']) < 2 or any(char.isdigit() for char in postData['first_name']):
            return {'error' : 'No fewer than 2 characters in First Name; letters only'}
        elif len(postData['last_name']) < 2 or any(char.isdigit() for char in postData['last_name']):
            return {'error' : 'No fewer than 2 characters in First Name; letters only'}
        elif len(postData['pwd']) < 8:
            return {'error': 'No fewer than 8 characters in password'}
        elif postData['confirm_pwd'] != postData['pwd']:
            return {'error': 'No match password'}

        else:
            hashed_pw = bcrypt.hashpw(postData['pwd'].encode('utf-8'), bcrypt.gensalt())
            if User.objects.all().count() < 1:
                user_level = 9
            else:
                user_level = 1
            
            return {'theUser' : User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'],email = postData['email'], password = hashed_pw, user_level = user_level) }

    def login(self, postData):
        if not EMAIL_REGEX.match(postData['email']):
            return {'error' : 'Invalid Format'}

        user = User.objects.filter(email = postData['email'])
        if not user:
            return {'error' : 'user does not exist.'}
        else:
            stored_hash = user[0].password
            input_hash = bcrypt.hashpw(postData['pwd'].encode(), stored_hash.encode())
            if not input_hash == stored_hash:
                return {'error' : 'Wrong password'}
            else:
                print "Success"
                return {'theUser' : user[0] }
    
class MessageManager(models.Manager):
    def create_new_msg_with_valid(self,postData):
        if len(postData['msg']) < 1:
            return {'error' : "Can not post a empty message."}
        else:
            return {'thisMsg' : Message.objects.create(content = postData['msg'], user = User.objects.get(id = postData['user_id']))}

class CommentManager(models.Manager):
    def create_new_comment_with_valid(self,postData):
        if len(postData['comment']) < 1:
            return {'error' : "Can not post a empty comment."}
        else:
            return {'thisComment' : Comment.objects.create(content = postData['comment'], user = User.objects.get(id = postData['user_id']), message = Message.objects.get(id = postData['msg_id']))}



class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    user_level = models.IntegerField()
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Description(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name="description")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Message(models.Model):
    content = models.TextField()
    to_user = models.ForeignKey(User, default = None, null = True, related_name="messages_received")
    from_user = models.ForeignKey(User, default = None, null = True, related_name="messages_left")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = MessageManager()

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name="user_comments")
    message = models.ForeignKey(Message, related_name='message_comments')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = CommentManager()