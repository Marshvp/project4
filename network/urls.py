
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<int:user_id>/", views.profile, name="profile"),
    path("check_following/<int:targetUserId>/", views.check_following, name="check_following"),
    path('follow_unfollow/<int:target_user_id>/', views.follow_unfollow, name='follow_unfollow'),
    path('following/', views.follow_page, name='following_page'),
    path('editModeldata/<int:postId>/', views.editModeldata, name="editModeldata")
]
