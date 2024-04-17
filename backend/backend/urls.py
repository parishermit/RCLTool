"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.Home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic.base import TemplateView
from trace_app.views import TraceView, DataProcess, ModifyDB, Test, TaskDB, List


urlpatterns = [
    path('admin/', admin.site.urls),
    path('getspanlist', TraceView.get_span_list, name='getspanlist'),
    path('gettracelist', TraceView.get_trace_list, name='gettracelist'),
    path('getNodesAndEdges', TraceView.get_nodes_and_edges, name='getNodesAndEdges'),
    path('getRootCause', ModifyDB.get_root_cause, name='getRootCause'),
    path('getdata', DataProcess.get_data, name='getdata'),
    path('outputtracecsv', DataProcess.output_trace_csv, name='outputtracecsv'),
    path('outputrclcsv', DataProcess.output_rcl_csv, name='outputrclcsv'),
    path('get_res', Test.get_res, name='get_res'),
    path('save_task', TaskDB.save_task, name='save_task'),
    path('get_task', TaskDB.get_task, name='get_task'),
    path('upload', TaskDB.upload, name='upload'),
    path('get_tree', List.get_tree, name='get_tree'),
    re_path(r'^$', TemplateView.as_view(template_name='index.html'))
]
