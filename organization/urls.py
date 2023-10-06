from django.urls import path, include
from .views import NewOrgView
from . import views


app_name = 'organization'

urlpatterns = [
    path('', views.index, name = 'index'),
    path("new_organization/", NewOrgView.as_view(), name = 'neworg'),
    path('orgs/<int:org_id>', views.dashboardpage, name ='orgpage'),
    path('profile/<uuid:user_id>', views.profile, name ='profile'),
    path('info_pages/', include('info_pages.urls')),#static pages that can be accessed from landing page
]

