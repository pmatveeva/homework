from django.conf.urls import url
from . import views
from my_site.views import SingIn
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^reg/', views.registration),
    url(r'^login/', views.SingIn.as_view()),
    url(r'^logout/', views.logout_view),
    url(r'^main/add', views.add),
    url(r'^item-(?P<pk>[A-Za-z0-9-]+)$',
        views.OneItem.as_view(), name='item_view'),
    url(r'^create', views.addnew),
    url(r'^main/(?P<page_id>[0-9]+)', views.ItemsView.as_view()),
    url(r'^orders/deleteitem/', views.delete_item, name='delete_item'),
    url(r'^orders/close-[0-9]{4}', views.change_status),
    url(r'^orders/delete-[0-9]{4}', views.delete_order),
    url(r'^orders/$',
        login_required(
            redirect_field_name='',
            login_url='/login')(views.OrdersView.as_view())),
    url(r'^computers/', views.list_computers)
]


