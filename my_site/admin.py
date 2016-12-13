from django.contrib import admin
from .models import Computer, BelongTO, Order, UserProfile
from django.contrib.auth.admin import UserAdmin, User
from .forms import ComputerForm


class UserInline(admin.StackedInline):
    model = UserProfile
    fields = ('birth_date', 'gender')
    can_delete = False
    verbose_name_plural = 'Additionally'


class UserAdmin(UserAdmin):
    inlines = (UserInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class BelongTOInline(admin.TabularInline):
    model = BelongTO
    extra = 1
    verbose_name_plural = 'Orders list'


class ComputerAdmin(admin.ModelAdmin):
    def orders(self, request):
        orders = []
        for s in BelongTO.objects.filter(item_id=request.name):
            orders.append(s.order_id)
        return orders
    inlines = (BelongTOInline,)
    list_display = ('name',
                    'price',
                    'description',
                    'pic',
                    'type',
                    'quantity',
                    'orders')


class OrderAdmin(admin.ModelAdmin):
    def total(self, request):
        total = 0
        items = BelongTO.objects.filter(order_id=request.code)
        for i in items:
            computer = Computer.objects.get(name=i.item_id)
            total += computer.price
        return total
    readonly_fields = ('total',)
    list_display = ('code', 'customer', 'total', 'is_open', 'date',)
    inlines = (BelongTOInline,)


admin.site.register(Computer, ComputerAdmin)
admin.site.register(Order, OrderAdmin)
