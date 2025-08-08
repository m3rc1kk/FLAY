from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('vote/<int:award_id>/<int:nominee_id>/', vote_for_nominee, name='vote'),
    path('nominee/<slug:slug>/', NomineesView.as_view(), name='nominees'),
]
