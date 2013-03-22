# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Assoccatsource(models.Model):
    xtrsrc = models.ForeignKey('Extractedsource', primary_key=True,
                               db_column='xtrsrc',
                               related_name='assoccatsources')
    catsrc = models.ForeignKey('Catalogedsource', db_column='catsrc',
                               related_name='assoccatsources')
    type = models.IntegerField()
    distance_arcsec = models.FloatField()
    r = models.FloatField()
    loglr = models.FloatField()
    class Meta:
        db_table = 'assoccatsource'

class Assocskyrgn(models.Model):
    runcat = models.ForeignKey('Runningcatalog', db_column='runcat',
                               related_name='assocskyrgns')
    skyrgn = models.ForeignKey('Skyregion', db_column='skyrgn',
                               related_name='assocskyrgns')
    distance_deg = models.FloatField()
    class Meta:
        db_table = 'assocskyrgn'

class Assocxtrsource(models.Model):
    runcat = models.ForeignKey('Runningcatalog', primary_key=True,
                               db_column='runcat',
                               related_name='Assocxtrsources')
    xtrsrc = models.ForeignKey('Extractedsource', db_column='xtrsrc',
                               related_name='asocxtrsources')
    type = models.IntegerField()
    distance_arcsec = models.FloatField()
    r = models.FloatField()
    loglr = models.FloatField()
    class Meta:
        db_table = 'assocxtrsource'

class Catalog(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    fullname = models.CharField(max_length=250)
    class Meta:
        db_table = 'catalog'

class Catalogedsource(models.Model):
    id = models.IntegerField(primary_key=True)
    catalog = models.ForeignKey(Catalog, db_column='catalog',
                                related_name='catalogedsources')
    orig_catsrcid = models.IntegerField()
    catsrcname = models.CharField(max_length=120)
    tau = models.IntegerField()
    band = models.ForeignKey('Frequencyband', db_column='band',
                             related_name='catalogedsources')
    stokes = models.IntegerField()
    freq_eff = models.FloatField()
    zone = models.IntegerField()
    ra = models.FloatField()
    decl = models.FloatField()
    ra_err = models.FloatField()
    decl_err = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    margin = models.BooleanField()
    det_sigma = models.FloatField()
    src_type = models.CharField(max_length=1)
    fit_probl = models.CharField(max_length=2)
    pa = models.FloatField()
    pa_err = models.FloatField()
    major = models.FloatField()
    major_err = models.FloatField()
    minor = models.FloatField()
    minor_err = models.FloatField()
    avg_f_peak = models.FloatField()
    avg_f_peak_err = models.FloatField()
    avg_f_int = models.FloatField()
    avg_f_int_err = models.FloatField()
    frame = models.CharField(max_length=20)
    class Meta:
        db_table = 'catalogedsource'

class Classification(models.Model):
    transient_id = models.IntegerField()
    classification = models.CharField(max_length=256)
    weight = models.FloatField()
    class Meta:
        db_table = 'classification'

class Dataset(models.Model):
    id = models.IntegerField(primary_key=True)
    rerun = models.IntegerField()
    type = models.IntegerField()
    process_ts = models.DateTimeField()
    detection_threshold = models.FloatField()
    analysis_threshold = models.FloatField()
    assoc_radius = models.FloatField()
    backsize_x = models.IntegerField()
    backsize_y = models.IntegerField()
    margin_width = models.FloatField()
    description = models.CharField(max_length=100)
    node = models.IntegerField()
    nodes = models.IntegerField()
    class Meta:
        db_table = 'dataset'

    def __unicode__(self):
        return self.description


class Extractedsource(models.Model):
    id = models.IntegerField(primary_key=True)
    image = models.ForeignKey('Image', db_column='image',
                              related_name='extractedsources')
    zone = models.IntegerField()
    ra = models.FloatField()
    decl = models.FloatField()
    ra_err = models.FloatField()
    decl_err = models.FloatField()
    ra_fit_err = models.FloatField()
    decl_fit_err = models.FloatField()
    ra_sys_err = models.FloatField()
    decl_sys_err = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    racosdecl = models.FloatField()
    margin = models.BooleanField()
    det_sigma = models.FloatField()
    semimajor = models.FloatField()
    semiminor = models.FloatField()
    pa = models.FloatField()
    f_peak = models.FloatField()
    f_peak_err = models.FloatField()
    f_int = models.FloatField()
    f_int_err = models.FloatField()
    extract_type = models.IntegerField()
    node = models.IntegerField()
    nodes = models.IntegerField()
    class Meta:
        db_table = 'extractedsource'

class Frequencyband(models.Model):
    id = models.IntegerField(primary_key=True)
    freq_central = models.FloatField()
    freq_low = models.FloatField()
    freq_high = models.FloatField()
    class Meta:
        db_table = 'frequencyband'

    def __unicode__(self):
        if self.freq_central:
            return "%s MHz" % (int(self.freq_central/10**6),)
        else:
            return "0 MHz"

class Image(models.Model):
    id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey(Dataset, db_column='dataset',
                                related_name='images')
    tau = models.IntegerField()
    band = models.ForeignKey(Frequencyband, db_column='band',
                             related_name='images')
    stokes = models.IntegerField()
    tau_time = models.FloatField()
    freq_eff = models.FloatField()
    freq_bw = models.FloatField()
    taustart_ts = models.DateTimeField()
    skyrgn = models.ForeignKey('Skyregion', db_column='skyrgn',
                               related_name='images')
    rb_smaj = models.FloatField()
    rb_smin = models.FloatField()
    rb_pa = models.FloatField()
    deltax = models.FloatField()
    deltay = models.FloatField()
    fwhm_arcsec = models.FloatField()
    fov_degrees = models.FloatField()
    url = models.CharField(max_length=1024)
    node = models.IntegerField()
    nodes = models.IntegerField()
    class Meta:
        db_table = 'image'

class Monitoringlist(models.Model):
    id = models.IntegerField(primary_key=True)
    runcat = models.ForeignKey('Runningcatalog', db_column='runcat',
                               related_name='monitoringlists')
    ra = models.FloatField()
    decl = models.FloatField()
    dataset = models.ForeignKey(Dataset, db_column='dataset',
                                related_name='monitoringlists')
    userentry = models.BooleanField()
    class Meta:
        db_table = 'monitoringlist'

class Node(models.Model):
    node = models.IntegerField(primary_key=True)
    zone = models.IntegerField()
    zone_min = models.IntegerField()
    zone_max = models.IntegerField()
    zone_min_incl = models.BooleanField()
    zone_max_incl = models.BooleanField()
    zoneheight = models.FloatField()
    nodes = models.IntegerField()
    class Meta:
        db_table = 'node'

class Rejection(models.Model):
    id = models.IntegerField(primary_key=True)
    image = models.ForeignKey(Image, db_column='image',
                              related_name='rejections')
    rejectreason = models.ForeignKey('Rejectreason', db_column='rejectreason')
    comment = models.CharField(max_length=512)
    class Meta:
        db_table = 'rejection'

class Rejectreason(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=512)
    class Meta:
        db_table = 'rejectreason'

class Runningcatalog(models.Model):
    id = models.IntegerField(primary_key=True)
    xtrsrc = models.ForeignKey(Extractedsource, db_column='xtrsrc',
                               related_name='runningcatalogs')
    dataset = models.ForeignKey(Dataset, db_column='dataset',
                                related_name='runningcatalogs')
    datapoints = models.IntegerField()
    zone = models.IntegerField()
    wm_ra = models.FloatField()
    wm_decl = models.FloatField()
    wm_ra_err = models.FloatField()
    wm_decl_err = models.FloatField()
    avg_wra = models.FloatField()
    avg_wdecl = models.FloatField()
    avg_weight_ra = models.FloatField()
    avg_weight_decl = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    margin = models.BooleanField()
    inactive = models.BooleanField()
    class Meta:
        db_table = 'runningcatalog'

class RunningcatalogFlux(models.Model):
    runcat = models.ForeignKey(Runningcatalog, primary_key=True,
                               db_column='runcat')
    band = models.ForeignKey(Frequencyband, db_column='band')
    stokes = models.IntegerField()
    f_datapoints = models.IntegerField()
    resolution = models.FloatField()
    avg_f_peak = models.FloatField()
    avg_f_peak_sq = models.FloatField()
    avg_f_peak_weight = models.FloatField()
    avg_weighted_f_peak = models.FloatField()
    avg_weighted_f_peak_sq = models.FloatField()
    avg_f_int = models.FloatField()
    avg_f_int_sq = models.FloatField()
    avg_f_int_weight = models.FloatField()
    avg_weighted_f_int = models.FloatField()
    avg_weighted_f_int_sq = models.FloatField()
    class Meta:
        db_table = 'runningcatalog_flux'

class Skyregion(models.Model):
    id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey(Dataset, db_column='dataset',
                                related_name='skyregions')
    centre_ra = models.FloatField()
    centre_decl = models.FloatField()
    xtr_radius = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    class Meta:
        db_table = 'skyregion'

class Temprunningcatalog(models.Model):
    runcat = models.ForeignKey(Runningcatalog, db_column='runcat',
                               related_name='Temprunningcatalogs')
    xtrsrc = models.ForeignKey(Extractedsource, db_column='xtrsrc',
                               related_name='Temprunningcatalogs')
    distance_arcsec = models.FloatField()
    r = models.FloatField()
    dataset = models.ForeignKey(Dataset, db_column='dataset',
                                related_name='Temprunningcatalogs')
    band = models.ForeignKey(Frequencyband, db_column='band',
                             related_name='Temprunningcatalogs')
    stokes = models.IntegerField()
    datapoints = models.IntegerField()
    zone = models.IntegerField()
    wm_ra = models.FloatField()
    wm_decl = models.FloatField()
    wm_ra_err = models.FloatField()
    wm_decl_err = models.FloatField()
    avg_wra = models.FloatField()
    avg_wdecl = models.FloatField()
    avg_weight_ra = models.FloatField()
    avg_weight_decl = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    margin = models.BooleanField()
    inactive = models.BooleanField()
    beam_semimaj = models.FloatField()
    beam_semimin = models.FloatField()
    beam_pa = models.FloatField()
    f_datapoints = models.IntegerField()
    avg_f_peak = models.FloatField()
    avg_f_peak_sq = models.FloatField()
    avg_f_peak_weight = models.FloatField()
    avg_weighted_f_peak = models.FloatField()
    avg_weighted_f_peak_sq = models.FloatField()
    avg_f_int = models.FloatField()
    avg_f_int_sq = models.FloatField()
    avg_f_int_weight = models.FloatField()
    avg_weighted_f_int = models.FloatField()
    avg_weighted_f_int_sq = models.FloatField()
    class Meta:
        db_table = 'temprunningcatalog'

class Transient(models.Model):
    id = models.IntegerField(primary_key=True)
    runcat = models.ForeignKey(Runningcatalog, db_column='runcat',
                               related_name='transients')
    band = models.ForeignKey(Frequencyband, db_column='band',
                             related_name='transients')
    siglevel = models.FloatField()
    v_int = models.FloatField()
    eta_int = models.FloatField()
    detection_level = models.FloatField()
    trigger_xtrsrc = models.ForeignKey(Extractedsource,
                                       db_column='trigger_xtrsrc',
                                       related_name='transients')
    status = models.IntegerField()
    t_start = models.DateTimeField()
    class Meta:
        db_table = 'transient'

class Version(models.Model):
    name = models.CharField(max_length=12, primary_key=True)
    value = models.IntegerField()
    class Meta:
        db_table = 'version'

