from django.conf.urls import include
from django.urls import path
from library.constant.api import URL_BACKEND_API

# from api.backend.v1.login.views import LoginView

urlpatterns = [
    # path('login/', LoginView.as_view({'post': 'post'})),

    path('company/', include('api.backend.company.urls'))

]
