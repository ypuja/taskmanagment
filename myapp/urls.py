from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet,SignupView, LoginView, TasklListView, StatusViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'status', StatusViewSet)

urlpatterns = [

    path('signup/', SignupView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='loginview'),
    path('task-list/', TasklListView.as_view(), name='your-model-list'),

]
urlpatterns += router.urls