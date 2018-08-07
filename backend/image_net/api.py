from rest_framework.views import APIView
from rest_framework.response import Response
import io
from PIL import Image
from .keras_utils import prepare_image, model, graph
from keras.applications import imagenet_utils
import tensorflow as tf

class PredictApiView(APIView):


    def post(self, request, format=None):
        """
        Return a list of all users.
        """
        data = {"success": False}
        #import ipdb; ipdb.set_trace()
        if request.FILES.get('image'):
            image = request.FILES['image'].read()
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
            data['predictions'] = []

            # loop over the results and add them to the list of
            # returned predictions
            for (imagenetID, label, prob) in results[0]:
                r = {'label': label, 'probability': float(prob)}
                data["predictions"].append(r)

            # indicate that the request was a success
            data['success'] = True
        return Response(data)