from django.db import models
from ..inquiries.models import Inquiry, Interview, Reception
from ..persons.models import Person


class Entry(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    inquiry = models.OneToOneField(Inquiry, on_delete=models.CASCADE)
    reception = models.OneToOneField(
        Reception, on_delete=models.CASCADE, null=True, blank=True
    )
    interview = models.OneToOneField(
        Interview, on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.person.full_name} の応募"
