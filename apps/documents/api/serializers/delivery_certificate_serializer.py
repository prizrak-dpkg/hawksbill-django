from rest_framework.serializers import ModelSerializer
from apps.documents.models import DeliveryCertificate


class DeliveryCertificateSerializer(ModelSerializer):
    class Meta:
        model = DeliveryCertificate
        exclude = ("registration_date", "modification_date", "status")
