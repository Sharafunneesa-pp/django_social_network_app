from django.contrib import admin

# Register your models here.
from social.models import Posts,Comments,UserProfile

admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(UserProfile)


