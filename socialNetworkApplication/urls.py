"""
URL configuration for socialNetworkApplication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", user_views.home, name="home"),
    path('login/', user_views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name='logout'),
    path("signup/", user_views.signup, name="signup"),
    path('send_friend_request/', user_views.SendFriendRequestView.as_view(), name='send_friend_request'),
    path('accept_friend_request/', user_views.AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('reject_friend_request/', user_views.RejectFriendRequestView.as_view(), name='reject_friend_request'),
    path('pending_friend_request/', user_views.ShowPendingFriendRequests, name='pending_friend_request'),
    path('friends/', user_views.ShowFriends, name='friends'),
]

urlpatterns += []+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
