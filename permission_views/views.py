from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

class PermissionDeniedTemplateView(TemplateView):
	template_name = "permissions/denied.html"
	def get_context_data(self, *args, **kwargs):
		context = super(PermissionDeniedTemplateView, self).get_context_data(**kwargs)
		context.update({
			'permission' : Permission.objects.get(codename = self.request.GET.get("permission").split(".")[1])
		})
		return context

class BasePermissionMixin(object):
	# Don't raise an exception by default
	raise_exception = False
	# Default required perms to none
	permission_required = None
	# Redirect to the permission denied URL or login URL
	def get_redirect_url(self):
		return reverse("permissions:denied") #getattr(settings, "PERMISSION_DENIED_URL", getattr(settings, "LOGIN_URL"))
	# Checks the permission exists on the user and redirect the page if not set
	def dispatch(self, request, *args, **kwargs):
		# Make sure that the permission_required attribute is set on the
		# view, or raise a configuration error.
		if self.permission_required is None:
			raise ImproperlyConfigured(
				"'PermissionRequiredMixin' requires "
				"'permission_required' attribute to be set.")
		# Check to see if the request's user has the required permission.
		has_permission = request.user.has_perm(self.permission_required)
		# If the user lacks the permission
		if not has_permission and request.user.is_authenticated():
			# *and* if an exception was desired
			if self.raise_exception:
				raise PermissionDenied  # return a forbidden response.
			return HttpResponseRedirect("%(url)s?permission=%(permission)s" % {
				"url" : self.get_redirect_url(),
				"permission" : self.permission_required,
			})
		return super(BasePermissionMixin, self).dispatch(request, *args, **kwargs)

class AddPermissionMixin(BasePermissionMixin):
	def dispatch(self, request, *args, **kwargs):
		meta = self.model._meta
		self.permission_required = "%s.%s" % (meta.app_label, meta.get_add_permission())
		return super(AddPermissionMixin, self).dispatch(request, *args, **kwargs)

class ViewPermissionMixin(BasePermissionMixin):
	def dispatch(self, request, *args, **kwargs):
		meta = self.model._meta
		self.permission_required = "%s.%s" % (meta.app_label, 'view_%s' % meta.object_name.lower())
		return super(ViewPermissionMixin, self).dispatch(request, *args, **kwargs)

class ChangePermissionMixin(BasePermissionMixin):
	def dispatch(self, request, *args, **kwargs):
		meta = self.model._meta
		self.permission_required = "%s.%s" % (meta.app_label, self.model.get_change_permission())
		return super(ChangePermissionMixin, self).dispatch(request, *args, **kwargs)

class DeletePermissionMixin(BasePermissionMixin):
	def dispatch(self, request, *args, **kwargs):
		meta = self.model._meta
		self.permission_required = "%s.%s" % (meta.app_label, meta.get_delete_permission())
		return super(DeletePermissionMixin, self).dispatch(request, *args, **kwargs)