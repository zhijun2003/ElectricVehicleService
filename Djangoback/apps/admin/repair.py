from django.contrib import admin
from apps.repair.models import RepairOrder


class RepairOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'status_badge', 'assigned_staff')
    list_filter = ('status',)

    def status_badge(self, obj):
        from django.utils.html import format_html
        colors = {'pending': 'orange', 'completed': 'green'}
        return format_html(
            '<span class="badge" style="background: {}">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )


admin.site.register(RepairOrder, RepairOrderAdmin)
