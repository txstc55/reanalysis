from django.db import models

# Create your models here.

class Sentence(models.Model):
	sentence=models.TextField()
	index=models.IntegerField(unique=True, primary_key=True)

	def __str__(self):
		return self.sentence