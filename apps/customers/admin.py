from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'name_kana', 'age', 'phone', 'email', 'created_at')
    search_fields = ('name', 'name_kana', 'phone', 'email')
    list_filter = ('created_at',)

    fieldsets = (
        ('基本情報', {'fields': ('name', 'name_kana', 'age')}),
        ('連絡先', {'fields': ('phone', 'email')}),
        ('その他', {'fields': ('memo',)}),
    )
    readonly_fields = ('created_at',)

    actions = ['send_dm']

    def send_dm(self, request, queryset):
        for customer in queryset:
            # ここでDM送信などの処理をする（ダミーではメッセージだけ表示）
            self.message_user(request, f"{customer.name} にDMを送信しました。")

    send_dm.short_description = "選択した顧客にDMを送信"
