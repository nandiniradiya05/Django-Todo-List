from django.urls import path
from .views import *


urlpatterns = [
    path('tasks/', TaskView.as_view(), name='user-tasks'),
    path('tasks/<int:task_id>/', TaskView.as_view(), name='update-tasks'),    
    path('tasks/other/', OtherUserTasksView.as_view(), name='other-user-tasks'),
    path('signup-login/', SignupLoginView.as_view(), name='signup-login'),

]
