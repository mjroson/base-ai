from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
import io
from PIL import Image
from .keras_utils import prepare_image, model, graph
from keras.applications import imagenet_utils
import tensorflow as tf
from .models import OcrTrack
from .serializers import OcrTrackModelSerializer
from django.core.files import File
from django.core.files.base import ContentFile


class PredictApiView(APIView):


    def post(self, request, format=None):
        """
        Return a list of all users.
        """
        data = {}
        success = False
        image_original = None
        image_b = None
        if request.FILES.get('image'):
            image_original = request.FILES['image'].read()
            image_b = Image.open(io.BytesIO(image_original))

            # preprocess the image and preparate it for classification
            image = prepare_image(image_b, target=(224, 224))

            # classify the input image and then initialize the list
            # of predictions to return to the client
            preds = None
            sess = tf.Session()
            init = tf.global_variables_initializer()
            sess.run(init)
            with graph.as_default():
                preds = model.predict(image)
            results = imagenet_utils.decode_predictions(preds)
            data['predictions'] = []

            # loop over the results and add them to the list of
            # returned predictions
            for (imagenetID, label, prob) in results[0]:
                r = {'label': label, 'probability': float(prob)}
                data["predictions"].append(r)

            # indicate that the request was a success
            success = False

        if success:
            if image_b.mode != "RGB":
                image_b = image_b.convert("RGB")

            image_b = image_b.resize((224, 224)).tobytes()
            #import ipdb; ipdb.set_trace()
            # ocr_track = OcrTrack.objects.create(image=image_b,
            #                                     original_image=image_original,
            #                                     predictions=data["predictions"])
            ocr_track = OcrTrack()
            ocr_track.predictions=str(data["predictions"])
            ocr_track.image.save('ticket-filename.jpg', ContentFile(image_b), save=False)
            ocr_track.original_image.save('ticket-filename.jpg', ContentFile(image_original), save=False)
            ocr_track.save()
            data = OcrTrackModelSerializer(ocr_track).data

        return Response(data, status=200 if success else 400)


class OcrTrackModelViewSet(ModelViewSet):
    serializer_class = OcrTrackModelSerializer
    queryset = OcrTrack.objects.all()

    def perform_create(self, serializer):
        predictions = []
        if self.request.FILES.get('image'):
            image = self.request.FILES['image'].read()
            image = Image.open(io.BytesIO(image))

            # preprocess the image and preparate it for classification
            image = prepare_image(image, target=(224, 224))

            # classify the input image and then initialize the list
            # of predictions to return to the client
            preds = None
            sess = tf.Session()
            init = tf.global_variables_initializer()
            sess.run(init)
            with graph.as_default():
                preds = model.predict(image)
            results = imagenet_utils.decode_predictions(preds)

            # loop over the results and add them to the list of
            # returned predictions
            for (imagenetID, label, prob) in results[0]:
                r = {'label': label, 'probability': float(prob)}
                predictions.append(r)

        serializer.save(predictions=predictions)