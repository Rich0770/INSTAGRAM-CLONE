from django.core.validators import FileExtensionValidator
from django.db import models
from shared.models import BaseModel
from users.models import User


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='images/post_images', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    video = models.FileField(upload_to='post_videos', null=True,
    validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    post = models.TextField()

    class Meta:
        db_table = 'post'


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=250)
    post = models.ForeignKey(Post, models.CASCADE, related_name='comment')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reply'
    )
    class Meta:
        db_table = 'comment'

class CommentLike(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentlike')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='commentlikes')

    class Meta:
        db_table = 'commentlike'

class Like(BaseModel):
    post = models.ForeignKey(Post, models.CASCADE, related_name='like')
    user = models.ForeignKey(Post, models.CASCADE, related_name='likes')

    class Meta:
        db_table = 'like'