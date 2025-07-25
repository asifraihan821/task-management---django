from django.urls import path
from users.views import sign_up,sign_in,sign_out,activate_user,admin_dashboard,assigned_role,create_group,group_list,CustomLoginView,ProfileView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    # path('sign-in/', sign_in, name='sign-in'),
    path('sign-in/', CustomLoginView.as_view(), name='sign-in'),
    # path('sign-out/', sign_out, name='sign-out'),
    path('sign-out/', LogoutView.as_view(), name='sign-out'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/<int:user_id>/assign-role/', assigned_role, name='assign-role'),
    path('create-group/', create_group, name= 'create-group'),
    path('admin/group-list/',group_list,name='group-list'),
    path('profile/', ProfileView.as_view(),name='profile'),
]
