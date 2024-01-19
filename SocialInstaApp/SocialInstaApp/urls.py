"""
URL configuration for SocialInstaApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from social import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignUpView.as_view(),name="signup"),
    path('',views.SignInView.as_view(),name="signin"),
    path('home/',views.IndexView.as_view(),name="home"),
    path('profiles/add',views.ProfileCreateView.as_view(),name="profile_add"),
    path('profile',views.MyProfileView.as_view(),name="myprofile"),
    path('profiles/<int:pk>/change',views.ProfileEditView.as_view(),name="profile_edit"),
    path('posts/<int:pk>/comments/add',views.AddCoomentView.as_view(),name="comment_add"),
    path('posts/<int:pk>/like/add',views.AddLikeView.as_view(),name="like_add"),
    path("logout",views.signout_view,name="signout"),
    path("users/<int:pk>/following/add",views.following_view,name="follow"),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



