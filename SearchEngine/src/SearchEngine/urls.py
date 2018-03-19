"""SearchEngine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Server import views as se_views
import settings

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^$', se_views.index, name='default'),
	url(r'^dashboard/$', se_views.dashboard, name='dashboard_index'),
	url(r'^dashboard/(creating|created)/$', se_views.dashboard, name='dashboard'),
	url(r'^login/$', se_views.login, name='login'),
	url(r'^logout/$', se_views.logout, name='logout'),
	url(r'^register/$', se_views.register, name='register'),
	url(r'^search/$', se_views.search, name="search"),
	url(r'^history/$', se_views.history, name="history"),
	url(r'^getHistoryDetail/$', se_views.getHistoryDetail, name="getHistoryDetail"),
	url(r'^getDetailMatchInfo/$', se_views.getDetailMatchInfo, name="getDetailMatchInfo"),
	url(r'^getDirectoryBrowserInfo/$', se_views.getHDFSDirectoryBrowserInfo, name="getHDFSDirectoryBrowserInfo"),
	url(r'^addDirectoryToDatabase/$', se_views.addDirectorytoDatabase, name='addDirectoryToDatabase'),
	url(r'^directoryAddition/$', se_views.directoryAddition, name='directoryAddition'),
	url(r'^test/$', se_views.test, name='test'),
	url(r'^changeString/$', se_views.changeString, name='changeString'),
	url(r'^validString/$', se_views.validString, name='validString'),
	url(r'^validMultiString/$', se_views.validMultiString, name='validMultiString'),
	url(r'^indexSearch/$', se_views.indexSearch, name='indexSearch'),
	url(r'^multiIndexSearch/$', se_views.multiIndexSearch, name='multiIndexSearch'),
	
	#url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT }),
]
