from django.contrib import admin

from ..models.inquiry import Inquiry, InquiryMethod

# from inquiries.models import InquiryType, InquiryResult


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = [field.name for field in model._meta.fields]

    # list_display = (
    #     'id',
    #     'person',
    #     'method',
    #     'brand',
    #     'content',
    #     'created_at',
    #     'updated_at',
    # )


admin.site.register(InquiryMethod)
# admin.site.register(InquiryType)
# admin.site.register(InquiryResult)
