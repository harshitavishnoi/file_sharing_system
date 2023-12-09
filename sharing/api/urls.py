# urls.py
from django.urls import path
from newapp.views import ops_login, ops_upload, client_signup, client_download, client_list_files

urlpatterns = [
    path('ops/login/', ops_login),
    path('ops/upload/', ops_upload),
    path('client/signup/', client_signup),
    path('client/download/<int:assignment_id>/', client_download),
    path('client/list-files/', client_list_files),
]