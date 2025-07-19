from django.contrib import admin

from .models import Branch, Brand, Idcard


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin): ...


@admin.register(Brand)
class TradeAdmin(admin.ModelAdmin): ...


@admin.register(Idcard)
class IdcardAdmin(admin.ModelAdmin):
    list_display = ('name',)
