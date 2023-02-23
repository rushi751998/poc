from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from app1 import views

urlpatterns =[
    path('admin/',admin.site.urls),
    path('',views.index,name="index"),
    path('index/',views.index),
    path('videos/',views.videos),
    path('videos/'+'videos2/',views.videos2),

    path('videos/'+'videos2/'+'dashboard/',views.dashboard)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  