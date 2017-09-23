from django.contrib import admin
from .models import User, Records, Event, Decks

admin.site.register(User)
admin.site.register(Records)
admin.site.register(Event)
admin.site.register(Decks)

# Register your models here.
