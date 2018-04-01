from django.contrib import admin


# admin:
# username: admin
# password: reanalysisadmin
# Register your models here.
from reanalysis.models import Sentence
admin.site.register(Sentence)
