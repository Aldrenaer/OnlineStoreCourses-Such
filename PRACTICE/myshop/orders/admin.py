from django.contrib import admin
from .models import Order, OrderItem
import csv
import datetime
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={opts.verbose_name}.csv'
    writer = csv.writer(response)
    
    fields = [field for field in opts.get_fields() 
              if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'email', 
        'address', 'postal_code', 'city', 'paid',
        'created', 'updated', 'order_detail_link',
        'coupon', 'discount'        
    ]

    def order_detail_link(self, obj):
        url = reverse('orders:admin_order_detail', args=[obj.id])
        return format_html('<a href="{}">View</a>', url)
    order_detail_link.short_description = 'Detail'    


    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]