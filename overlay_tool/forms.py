
from django import forms
from .models import MapOverlay

class MapOverlayForm(forms.ModelForm):
    class Meta:
        model = MapOverlay
        fields = ['event_name','overlay_file','gps_nw','gps_ne','gps_sw','gps_se']
        widgets = {
            'gps_nw': forms.TextInput(attrs={'placeholder':'lat,lng'}),
            'gps_ne': forms.TextInput(attrs={'placeholder':'lat,lng'}),
            'gps_sw': forms.TextInput(attrs={'placeholder':'lat,lng'}),
            'gps_se': forms.TextInput(attrs={'placeholder':'lat,lng'}),
        }

    def clean_overlay_file(self):
        f = self.cleaned_data.get('overlay_file')
        if f:
            if not f.content_type in ('image/png', 'image/x-png'):
                raise forms.ValidationError('Only PNG overlays are accepted (preserve transparency).')
            if f.size > 6 * 1024 * 1024:
                raise forms.ValidationError('File too large (limit 6 MB).')
        return f

    def clean_gps_nw(self):
        return self._clean_gps_field('gps_nw')

    def clean_gps_ne(self):
        return self._clean_gps_field('gps_ne')

    def clean_gps_sw(self):
        return self._clean_gps_field('gps_sw')

    def clean_gps_se(self):
        return self._clean_gps_field('gps_se')

    def _clean_gps_field(self, name):
        raw = self.data.get(name) or self.initial.get(name)
        if not raw:
            raise forms.ValidationError('GPS field required (format: lat,lng).')
        try:
            lat_str, lng_str = [p.strip() for p in raw.split(',')]
            lat = float(lat_str)
            lng = float(lng_str)
        except Exception:
            raise forms.ValidationError('GPS must be two numbers separated by a comma: lat,lng')
        if not (-90 <= lat <= 90 and -180 <= lng <= 180):
            raise forms.ValidationError('GPS values out of range.')
        return f"{lat:.6f},{lng:.6f}"
