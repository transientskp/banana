from banana.models import Runningcatalog, Extractedsource, Dataset, Image, Assocxtrsource
from rest_framework import serializers


class RunningcatalogSerializer(serializers.HyperlinkedModelSerializer):
    dataset = serializers.PrimaryKeyRelatedField(many=False)
    assocxtrsources = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = Runningcatalog
        fields = ('id', 'wm_ra', 'wm_decl', 'dataset', 'assocxtrsources')


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


class AssocxtrsourceSerializer(serializers.HyperlinkedModelSerializer):
    runcat = serializers.PrimaryKeyRelatedField(many=False)
    xtrsrc = serializers.PrimaryKeyRelatedField(many=False)

    class Meta:
        model = Assocxtrsource
        fields = ('id', 'runcat', 'xtrsrc', 'type', 'distance_arcsec', 'r',
                  'loglr', 'v_int', 'eta_int')
