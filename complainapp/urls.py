from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.handleLogin, name="handleLogin"),
    path('signup', views.handleSignup, name="handleSignup"),
    path('logout', views.handleLogout, name="handleLogout"),
    path('respondcomplain', views.respondComplain, name="respondComplain"),
    path('createcomplain', views.createComplain, name="createComplain"),
    # path('complainform/', views.complainForm, name='complainForm'),
    # path('form', views.form, name='form'),
    # path("contact", views.contact, name="contact"),
    # path('aboutus', views.about, name='aboutus'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
