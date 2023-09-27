from unicodedata import name
from django.urls import path
from . import views as ev

urlpatterns = [
    path('', ev.login, name='login'),
    path('validation', ev.validation, name='validation'),
    path('registration/', ev.registration, name='registration'),
    path('intelliextract/', ev.intelliextract, name='intelliextract'),
    path('search_history/', ev.search_history, name='search_history'),
    path('analyze_invoice/', ev.analyze_invoice, name='analyze_invoice'),

]
