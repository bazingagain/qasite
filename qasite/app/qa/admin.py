from django.contrib import admin
from qasite.app.qa.models import QAPair,UserQAPair
# Register your models here.

admin.site.register(QAPair)
admin.site.register(UserQAPair)