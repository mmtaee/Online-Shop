from django.urls import path
from user.api import views

app_name = "user_api"


urlpatterns = [
		# admin user
        path('list/', views.SuperUserListApiView.as_view(), name='list'),
        path('create/', views.SuperUserCreateApiView.as_view(), name='create'),
        path('manager/<int:id>/', views.SuperUserMangerApiView.as_view(), name='manager'),

        #other
        path('signup/', views.SignUpApiView.as_view(), name='signup'),
        path('login/', views.LoginApiView.as_view(), name='login'),
        path('logout/', views.LogoutApiView.as_view(), name='logout'),
        path('delete_account/', views.DeleteAccountApiView.as_view(), name='delete_account'),
        path('change_password/', views.ChangePasswordApiView.as_view(), name="change_password"),
]
