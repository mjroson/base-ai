from django import forms
from .models import OCR
from .keras_classifiers.classifiers import (
    get_model,
    predict,
)
import tensorflow as tf


keras_model = get_model()
# also stored the graph under with the model is built
graph = tf.get_default_graph()


class OCRForm(forms.ModelForm):
    class Meta:
        model = OCR
        fields = [
            'img_path',
        ]

    def save(self, commit=True):
        # override save method and call the classifier
        instance = super(OCRForm, self).save(commit=False)
        # update first to get the image path
        instance.save()

        # inference the model under the same graph
        with graph.as_default():
            instance.pred_char = predict(keras_model, instance.img_path.path)
        if commit:
            instance.save()

        return instance
