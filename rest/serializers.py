from banana.models import Runningcatalog, Extractedsource, Dataset, Image
from rest_framework import serializers


class RunningcatalogSerializer(serializers.HyperlinkedModelSerializer):
    dataset = serializers.PrimaryKeyRelatedField(many=False)

    class Meta:
        model = Runningcatalog
        fields = ('id', 'wm_ra', 'wm_decl', 'dataset')


class ExtractedsourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Extractedsource
        fields = ('id', 'ra', 'decl')


class DatasetSerializer(serializers.HyperlinkedModelSerializer):
    images = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = Dataset
        fields = ('id', 'process_start_ts', 'description', 'images')


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    dataset = serializers.PrimaryKeyRelatedField(many=False)

    class Meta:
        model = Image
        fields = ('id', 'freq_eff', 'freq_bw', 'taustart_ts', 'dataset')
