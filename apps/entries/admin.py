from django.contrib import admin

from .models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('get_person_name', 'get_phone', 'get_status')

    def get_person_name(self, obj):
        return obj.person.full_name

    get_person_name.short_description = '氏名'

    def get_phone(self, obj):
        return obj.person.phone

    get_phone.short_description = '電話番号'

    def get_status(self, obj):
        return obj.reception.get_status_display()

    get_status.short_description = '受付状況'


# @admin.register(Entry)
# class _EntryAdmin(admin.ModelAdmin):
#     form = EntryForm
#     # list_display = ('get_person_name', 'get_phone', 'get_status')
#     list_display = ('person', 'inquiry', 'reception')
#     fieldsets = (
#         (
#             'Person情報',
#             {
#                 'fields': (
#                     'full_name',
#                     'full_name_kana',
#                     'age',
#                     'phone',
#                     'email',
#                     'line_name',
#                     'branch',
#                     'idcard',
#                     'description',
#                 )
#             },
#         ),
#         # (
#         #     'Inquiry情報',
#         #     {
#         #         'fields': (
#         #             'inquiry_method',
#         #             'inquiry_brand',
#         #             'inquiry_content',
#         #         )
#         #     },
#         # ),
#         # (
#         #     'Reception情報',
#         #     {
#         #         'fields': (
#         #             'reception_status',
#         #             'reception_remarks',
#         #         )
#         #     },
#         # ),
#         # (
#         #     'Interview情報',
#         #     {
#         #         'fields': (
#         #             'interview_scheduled_date',
#         #             'interview_status',
#         #             'interview_result_status',
#         #             'interview_result_memo',
#         #             'interview_decided_at',
#         #         )
#         #     },
#         # ),
#     )

#     def get_person_name(self, obj):
#         return obj.person.full_name

#     get_person_name.short_description = '氏名'

#     def get_phone(self, obj):
#         return obj.person.phone

#     get_phone.short_description = '電話番号'

#     def get_status(self, obj):
#         return obj.reception.get_status_display()

#     get_status.short_description = '受付状況'
