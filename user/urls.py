from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegisterViewset


router = DefaultRouter()
router.register(r'register', RegisterViewset)

urlpatterns = [

    path('', include(router.urls))

]
