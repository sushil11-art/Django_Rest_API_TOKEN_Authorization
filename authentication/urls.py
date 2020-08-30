from django.urls import path
from authentication.views import RegisterView,HelloView,ApiRoot,login,LoginView

# from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('',ApiRoot.as_view(),name='root'),
    path('register/',RegisterView.as_view(),name='register'),
    path('hello/',HelloView.as_view(),name='hello'),
    # path('login/',login,name='login'),
    path('login/',LoginView.as_view(),name='login')
]

# urlpatterns=format_suffix_patterns(urlpatterns)