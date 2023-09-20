from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, RegisterViewset


router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [

    path('register', RegisterViewset.as_view({'post': 'create'}))

]
