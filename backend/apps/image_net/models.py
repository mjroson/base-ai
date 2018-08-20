from django.db import models
from django.contrib.postgres import fields
from apps.core.models import BaseModel


class OcrTrack(BaseModel):

    image = models.ImageField(upload_to='image_processed')
    predictions = fields.JSONField(blank=True, null=True)
    label = models.CharField(max_length=100, blank=True)
    success_prediction = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if len(self.predictions) and self.label and \
                        self.predictions[0].get('label') == self.label:
            self.success_prediction = True

        return super(OcrTrack, self).save(*args, **kwargs)
