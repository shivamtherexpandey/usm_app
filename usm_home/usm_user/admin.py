from django.contrib import admin
from usm_user.models import User, Subscription, SubscriptionPlan


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "is_staff", "is_superuser", "created_at")
    search_fields = ("email",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    exclude = ("password",)


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Subscription)
admin.site.register(SubscriptionPlan)
