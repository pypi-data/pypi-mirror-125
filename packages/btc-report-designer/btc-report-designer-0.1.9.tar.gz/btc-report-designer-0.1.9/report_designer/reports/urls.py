from django.urls import path, include

from . import views


app_name = 'reports'


ajax_urls = [
    path('table/<str:type>/', views.ReportListView.as_view(), name='list'),
    path('create/', views.ReportCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.ReportUpdateView.as_view(), name='update'),
    path('<int:report_pk>/tables/<int:pk>/fields/', views.TableFieldsListView.as_view(), name='fields-list'),
    path('<int:report_pk>/tables/', views.DBTablesTreeListView.as_view(), name='tables-list'),
    path('<int:report_pk>/tables/included/', views.ReportDBTablesTreeListView.as_view(), name='included-tables-list'),
    path('<int:pk>/add_table/', views.ReportDBTableAddView.as_view(), name='add-table'),
    path('<int:pk>/remove_table/', views.ReportDBTableRemoveView.as_view(), name='remove-table'),
    path('<int:pk>/fields/<str:type>/', views.ReportFieldsListView.as_view(), name='report-fields-list'),
    path('<int:pk>/add_fields/', views.ReportFieldsAddView.as_view(), name='add-fields'),
    path('<int:pk>/change_order/', views.ReportFieldChangeOrderView.as_view(), name='field-change-order'),
]


urlpatterns = [
    path('', views.ReportListView.as_view(), name='list', kwargs={'type': 'base'}),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='detail'),
    path('ajax/', include(ajax_urls)),
]
