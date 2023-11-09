from django.db import models

# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(editable=False, primary_key=True),

    created_time = models.DateTimeField(auto_now_add=True),

    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True