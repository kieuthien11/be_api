from django.urls import path

from api.backend.company.views import CompanyViewSet

urlpatterns = [
    path('list/', CompanyViewSet.as_view({'get': 'list'})),
    path('create_or_update/', CompanyViewSet.as_view({'post': 'create_or_update'})),
    path('detail/', CompanyViewSet.as_view({'get': 'detail_company'})),
    path('delete/', CompanyViewSet.as_view({'post': 'delete_company'})),

]
