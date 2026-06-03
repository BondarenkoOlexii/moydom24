from django.contrib.auth.mixins import AccessMixin, PermissionRequiredMixin
from src.users.models import User, Role

class AdminpanelRestrictionMixin(AccessMixin):
    required_section = None

    def dispatch(self, request, *args, **kwargs):

        user = request.user

        if not user.is_authenticated or not user.is_staff:
            return self.handle_no_permission()

        role = Role.objects.get(user=user)


        if user.is_superuser or user.id == 1:
            return super().dispatch(request, *args, **kwargs)

        attribute = getattr(role, self.required_section, False)

        if not attribute:
            return self.handle_no_permission()

        # if self.required_section == 'users':
        #     if not role.users:
        #         return self.handle_no_permission()
        #
        # elif self.required_section == 'role':
        #     if not role.role_list:
        #         return self.handle_no_permission()
        #
        # elif self.required_section == 'payment_info':
        #     if not role.payment_data:
        #         return self.handle_no_permission()

        if self.required_section is None:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)