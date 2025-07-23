from django.contrib import admin
from .models import Category, Event, RSVP

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'date', 'time', 'location')
    list_filter = ('category', 'date')
    search_fields = ('name', 'location')
    filter_horizontal = ('participants',)

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status', 'rsvp_time')
    list_filter = ('status', 'rsvp_time')
    search_fields = ('user__username', 'event__name')
