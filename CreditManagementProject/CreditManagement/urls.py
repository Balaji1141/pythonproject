from django.urls import path

from . import views
from .views import *
urlpatterns=[
    path('listledgers', ListLedgers.as_view()),
    path('editledger', EditLedger.as_view()),
    path('createledger',CreateLedger.as_view()),
    path('transaction/<str:type>',Transaction.as_view())
]