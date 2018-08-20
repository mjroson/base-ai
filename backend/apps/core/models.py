from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.deletion import ProtectedError
from django.urls import reverse

from .utils import generate_unique_slug


class ExcludeDeletedManager(models.Manager):
    def get_queryset(self):
        return super(ExcludeDeletedManager, self).get_queryset().filter(_deleted=False)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    _deleted = models.BooleanField(default=False)

    objects = ExcludeDeletedManager()
    admin_manager = models.Manager()

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def delete(self, using=None):
        try:
            super(BaseModel, self).delete(using)
        except ProtectedError:
            self._deleted = True
            self.save()


class ApiDummy(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(editable=False, unique=True)
    html_response = models.TextField(blank=True, null=True)
    json_response = JSONField(blank=True, null=True)

    @property
    def endpoint(self):
        return reverse('api-dummy', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(ApiDummy, [self.name])

        return super(ApiDummy, self).save(*args, **kwargs)
