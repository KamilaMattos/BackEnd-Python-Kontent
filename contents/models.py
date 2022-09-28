from django.db import models


class Content(models.Model):
    title = models.CharField(max_length=50, null=False)
    module = models.TextField(max_length=None)
    students = models.IntegerField(null=False, blank=False)
    description = models.TextField(max_length=None, null=True)
    is_active = models.BooleanField(null=True, default=False)

    def __repr__(self) -> str:
        return f"<[{self.id}] {self.title} - {self.module}"
