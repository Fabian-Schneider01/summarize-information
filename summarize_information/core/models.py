from django.db import models

# Create your models here.
class Text(models.Model):
    input_text = models.TextField()
    output_text = models.TextField()
