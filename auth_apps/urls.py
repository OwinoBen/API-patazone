from django.urls import path

from auth_apps import views

app_name='auth_apps'

urlpatterns =[
    path('createuser', views.registration_view, name="createuser"),
    path('login', views.login_user, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('update-account', views.update_account_view, name="update-account"),
    path('list-users', views.account_property_view, name="list-users"),
    path('oauthlogin', views.user_login),
    path('registeruser', views.TokenView.as_view()),
    path('reg', views.RefreshToken.as_view()),
]