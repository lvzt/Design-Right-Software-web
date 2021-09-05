from django.db import models

# Create your models here.
class SelectProject(models.Model):
    project_description = models.TextField(null=True, default='', max_length=500)
    # sketch_concept = models.ImageField(upload_to ='uploads/')