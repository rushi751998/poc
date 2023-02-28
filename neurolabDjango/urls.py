from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from app1 import views

urlpatterns =[
    path('admin/',admin.site.urls),
    path('',views.index,name="index"),
    path('videos/',views.videos,name = "videos"),
    path('videos/videos2/',views.videos2,name = "videos2"),
    path('videos/videos2/dashboard_filter/',views.dashboard,name = "dashboard_filter"),
    path('videos/videos2/dashboard_filter/graphs',views.graph,name = "graphs"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  