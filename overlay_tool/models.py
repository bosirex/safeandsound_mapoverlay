
import os
from django.db import models
from django.conf import settings
import qrcode

def overlay_upload_to(instance, filename):
    return f'overlays/{filename}'

class MapOverlay(models.Model):
    event_name = models.CharField(max_length=255)
    overlay_file = models.ImageField(upload_to=overlay_upload_to)
    gps_nw = models.CharField(max_length=50)
    gps_ne = models.CharField(max_length=50)
    gps_sw = models.CharField(max_length=50)
    gps_se = models.CharField(max_length=50)
    qr_file = models.CharField(max_length=255, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.event_name}"

    def generate_qr(self, request=None):
        # create absolute url if request provided
        if request:
            view_url = request.build_absolute_uri(f"/overlay/view/{self.pk}/")
        else:
            view_url = f"/overlay/view/{self.pk}/"
        qr_path = os.path.join(settings.BASE_DIR, 'qr_codes', f"{self.pk}.png")
        img = qrcode.make(view_url)
        img.save(qr_path)
        self.qr_file = f'qr_codes/{self.pk}.png'
        self.save(update_fields=['qr_file'])
