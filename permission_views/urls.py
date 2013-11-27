from django.conf.urls import patterns, url
from views import PermissionDeniedTemplateView

urlpatterns = patterns('',
	url(r'^denied/', PermissionDeniedTemplateView.as_view(), name = "denied"),
)