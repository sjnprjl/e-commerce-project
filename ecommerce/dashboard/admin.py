from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from .models import Account, Isp, Customer, Subscription


class AccountAdmin(UserAdmin):
    list_display = (
        "email",
        "username",
        "full_name",
        "phone",
        "date_joined",
        "last_login",
        "is_admin",
        "is_staff",
    )
    search_fields = ("email", "username")
    readonly_fields = ("date_joined", "last_login")
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# class customerAdmin(AdminSite.ModelAdmin):
    list_display = (
        "full_name",
        "phone",
        "address",
        "reg_date",
        "isp",
        "user",
    )
    search_fields = ("full_name",)
    # filter_horizontal = ()
    # list_filter = ()
    # fieldsets = ()
class DashboardAdminSite(AdminSite):
    site_header = "Super Admin pannel"
    site_title = "Dashboard-Admin"
    index_title = "Welcome to ISP Super Admin pannel"

dashboard_admin_site = DashboardAdminSite(name='dashboard_admin')

# dashboard_admin_site.register(Account, AccountAdmin)
dashboard_admin_site.register(Isp)
dashboard_admin_site.register(Subscription)
# dashboard_admin_site.register(Customer, customerAdmin)


