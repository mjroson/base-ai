import os
from django.db import models
from uuid import uuid4


def rename_upload_path(path):
    """Rename the filename path.

    The image will have prefix path,
    the filename will be altered upon conflict.
    """
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]

        if instance.pk:
            filename = "{}.{}".format(instance.pk, ext)
        else:
            filename = "{}.{}".format(uuid4().hex, ext)

        return os.path.join(path, filename)
    return wrapper


class OCR(models.Model):
    # img_path = models.ImageField(upload_to="img/", default="img/default.jpg")
    img_path = models.ImageField(upload_to='img/',
                                 default="img/default.jpg")
    timestamp = models.DateTimeField(auto_now=True)
    pred_char = models.CharField(max_length=1)

    def __str__(self):
        return self.img_path.path
