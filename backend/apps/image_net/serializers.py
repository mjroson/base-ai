from apps.core.serializers import BaseModelSerializer

from .models import OcrTrack




OCR_BASE_EXTRA_KWARGS = {
        'label': {'required': None}
}

OCR_BASE_READ_ONLY_FIELDS = ('predictions', 'is_prediction', 'id')

class OcrTrackModelSerializer(BaseModelSerializer):

    class Meta:
        model = OcrTrack
        fields = '__all__'
        read_only_fields = OCR_BASE_READ_ONLY_FIELDS
        fields_config = {
            'create': {
                'extra_kwargs': OCR_BASE_EXTRA_KWARGS, #dict(OCR_BASE_EXTRA_KWARGS, **{'parent': {'read_only': False}})
                'required_fields': ('image', ),
                'read_only_fields': OCR_BASE_READ_ONLY_FIELDS + ('label',)
            },
            'update': {
                'read_only_fields': OCR_BASE_READ_ONLY_FIELDS + ('image', ),
                'extra_kwargs': { 'image': {'read_only': True}}
            }
        }