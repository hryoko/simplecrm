from django.contrib import admin
from ..models.inquiry import Inquiry, InquiryMethod

# from inquiries.models import InquiryType, InquiryResult


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'person',
        'method',
        'content',
        'status',
        'created_at',
        'updated_at',
    )


admin.site.register(InquiryMethod)
# admin.site.register(InquiryType)
# admin.site.register(InquiryResult)
