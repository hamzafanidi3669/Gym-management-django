from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.home, name='home'),

    path('profile/', views.redirect_to_profile, name='redirect_to_profile'),
    path('profile/<int:userid>/', views.profile, name='profile'),
    path('like_unlike_post/<int:postuserid>/', views.like_unlike_post, name='like_unlike_post'),
    path('profile/status/<int:userid>/', views.profile_status, name='profile_status'),
    path('profile/media/<int:userid>/', views.profile_media, name='profile_media'),

    path('profile/status/', views.redirect_to_profile_status, name='redirect_to_profile_status'),
    path('profile/media/', views.redirect_to_profile_media, name='redirect_to_profile_media'),



    path('add_post', views.add_post, name='add_post'),

    path('delete_post/<int:postid>/', views.delete_post, name='delete_post'),
    path('edit_post/<int:postid>/', views.edit_post, name='edit_post'),

    path('add_comment/<int:postuserid>', views.add_comment, name='add_comment'),

    path('update_photo_prfl/<int:postid>', views.update_photo_prfl, name='update_photo_prfl'),
    path('update_photo_couverture/<int:postid>', views.update_photo_couverture, name='update_photo_couverture'),

    path('search_users', views.search_users, name='search_users'),
    
    path('send_friend_request/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('cancel_friend_request/<str:username>/', views.cancel_friend_request, name='cancel_friend_request'),

    #notifications 
    path('show_all_notifications', views.show_all_notifications, name='show_all_notifications'),

    path('ajax_search_users/', views.ajax_search_users, name='ajax_search_users'),



    path('ajax_get_notifications/', views.ajax_get_notifications, name='ajax_get_notifications'),


    path('mark_notification_as_read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('mark_all_notifications_as_read/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),



    path('post/<int:postid>/', views.view_post, name='view_post'),

    path('dispo_coach/<int:coach_id>/', views.disponibilites_coach, name='dispo_coach'),
    path('coach/reservations/', views.coach_reservations, name='coach_reservations'),


    path('usersmanager', views.usersmanager, name='usersmanager'),



    path('ban_user/<int:user_id>/', views.ban_user, name='ban_user'),
    path('unban-user/<int:user_id>/', views.unban_user, name='unban_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
