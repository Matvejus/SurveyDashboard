from django.urls import path, include
from .views import NewOrgView, NewCollab
from . import views


app_name = 'organization'

urlpatterns = [
    path('', views.index, name = 'index'),
    path("new_organization/", NewOrgView.as_view(), name = 'neworg'),
    path("new_collaboration/", NewCollab.as_view(), name = 'new_collab'),
    path('dashboard', views.dashboardpage, name ='dashboard'),
    path('profile/<uuid:user_id>', views.profile, name ='profile'),
    path('info_pages/', include('info_pages.urls')),#static pages that can be accessed from landing page
]

