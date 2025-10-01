
from django.contrib import admin
from .models import MapOverlay
@admin.register(MapOverlay)
class MapOverlayAdmin(admin.ModelAdmin):
    list_display = ('id','event_name','date_created')
