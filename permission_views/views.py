from braces.views import PermissionRequiredMixin
from django.conf import settings

class BasePermissionMixin(PermissionRequiredMixin):
	login_url = getattr(settings, "PERMISSION_DENIED_URL", getattr(settings, "LOGIN_URL"))

class AddPermissionMixin(BasePermissionMixin):
	def dispatch(self, request, *args, **kwargs):
		self.permission_required = self.model._meta.get_add_permission()
		return super(AddPermissionMixin, self).dispatch(request, *args, **kwargs)

class ChangePermissionMixin(BasePermissionMixin):
	def dispatch(self, request, *args, **kwargs):
		self.permission_required = self.model._meta.get_change_permission()
		return super(ChangePermissionMixin, self).dispatch(request, *args, **kwargs)

class DeletePermissionMixin(BasePermissionMixin):
	def dispatch(self, request, *args, **kwargs):
		self.permission_required = self.model._meta.get_delete_permission()
		return super(DeletePermissionMixin, self).dispatch(request, *args, **kwargs)