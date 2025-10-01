
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_overlay, name='upload_overlay'),
    path('view/<int:event_id>/', views.view_overlay, name='view_overlay'),
    path('edit/<int:event_id>/', views.edit_overlay, name='edit_overlay'),
    path('delete/<int:event_id>/', views.delete_overlay, name='delete_overlay'),
]
