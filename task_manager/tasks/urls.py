from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.home, name='home'),
    path('login',views.login_user, name='login'),
    path('signup',views.signup, name='signup'),
    path('user_profile',views.user_profile, name='user_profile'),
    path('logout/', views.logout_user, name='logout'),
    path('create_task/', views.create_task, name='create_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('task_detail/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/delete_selected_photos/', views.delete_selected_photos, name='delete_selected_photos'),
    path('update_task/<int:task_id>/', views.update_task, name='update_task'),
    path('add_photo/<int:task_id>/', views.add_photo, name='add_photo'),
    path('mark_as_complete/', views.mark_as_complete, name='mark_as_complete'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('users/', views.user_list, name='user_list'),
    path('make_admin/<int:user_id>/', views.make_admin, name='make_admin'),
    path('remove_admin/<int:user_id>/', views.remove_admin, name='remove_admin'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)