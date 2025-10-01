
import os
import shutil
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse
from .models import MapOverlay
from .forms import MapOverlayForm
import qrcode

# convenience paths
REPO_ROOT = settings.BASE_DIR
STATIC_OVERLAYS_DIR = os.path.join(REPO_ROOT, 'overlay_tool', 'static', 'overlay_tool', 'overlays')
os.makedirs(STATIC_OVERLAYS_DIR, exist_ok=True)
QR_DIR = os.path.join(REPO_ROOT, 'qr_codes')
os.makedirs(QR_DIR, exist_ok=True)

def dashboard(request):
    overlays = MapOverlay.objects.order_by('-date_created')
    return render(request, 'overlay_tool/dashboard.html', {'overlays': overlays})

def upload_overlay(request):
    if request.method == 'POST':
        form = MapOverlayForm(request.POST, request.FILES)
        if form.is_valid():
            mo = form.save()
            try:
                if mo.overlay_file and os.path.exists(mo.overlay_file.path):
                    src = mo.overlay_file.path
                    dst = os.path.join(STATIC_OVERLAYS_DIR, os.path.basename(src))
                    shutil.copyfile(src, dst)
            except Exception:
                pass

            try:
                view_url = request.build_absolute_uri(reverse('view_overlay', args=[mo.pk]))
                qr_img = qrcode.make(view_url)
                qr_path = os.path.join(QR_DIR, f"{mo.pk}.png")
                qr_img.save(qr_path)
                mo.qr_file = f"qr_codes/{mo.pk}.png"
                mo.save(update_fields=['qr_file'])
            except Exception:
                pass

            return redirect('dashboard')
    else:
        form = MapOverlayForm()
    return render(request, 'overlay_tool/upload.html', {'form': form})

def view_overlay(request, event_id):
    mo = get_object_or_404(MapOverlay, pk=event_id)
    def to_pair(s):
        parts = s.split(',')
        return [float(parts[0].strip()), float(parts[1].strip())]
    gps = {
        'nw': to_pair(mo.gps_nw),
        'ne': to_pair(mo.gps_ne),
        'sw': to_pair(mo.gps_sw),
        'se': to_pair(mo.gps_se),
    }
    return render(request, 'overlay_tool/view.html', {'mo': mo, 'gps': gps})

def edit_overlay(request, event_id):
    mo = get_object_or_404(MapOverlay, pk=event_id)
    if request.method == 'POST':
        form = MapOverlayForm(request.POST, request.FILES, instance=mo)
        if form.is_valid():
            mo = form.save()
            try:
                view_url = request.build_absolute_uri(reverse('view_overlay', args=[mo.pk]))
                qr_img = qrcode.make(view_url)
                qr_path = os.path.join(QR_DIR, f"{mo.pk}.png")
                qr_img.save(qr_path)
                mo.qr_file = f"qr_codes/{mo.pk}.png"
                mo.save(update_fields=['qr_file'])
            except Exception:
                pass
            try:
                if mo.overlay_file and os.path.exists(mo.overlay_file.path):
                    dst = os.path.join(STATIC_OVERLAYS_DIR, os.path.basename(mo.overlay_file.path))
                    shutil.copyfile(mo.overlay_file.path, dst)
            except Exception:
                pass
            return redirect('dashboard')
    else:
        form = MapOverlayForm(instance=mo)
    return render(request, 'overlay_tool/edit.html', {'form': form, 'mo': mo})

def delete_overlay(request, event_id):
    mo = get_object_or_404(MapOverlay, pk=event_id)
    if request.method == 'POST':
        try:
            if mo.overlay_file and os.path.exists(mo.overlay_file.path):
                os.remove(mo.overlay_file.path)
        except Exception:
            pass
        try:
            static_copy = os.path.join(STATIC_OVERLAYS_DIR, os.path.basename(mo.overlay_file.name))
            if os.path.exists(static_copy):
                os.remove(static_copy)
        except Exception:
            pass
        try:
            qr_path = os.path.join(REPO_ROOT, mo.qr_file) if mo.qr_file else None
            if qr_path and os.path.exists(qr_path):
                os.remove(qr_path)
        except Exception:
            pass
        mo.delete()
        return redirect('dashboard')
    return render(request, 'overlay_tool/delete_confirm.html', {'mo': mo})
