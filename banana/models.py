from __future__ import unicode_literals
from django.db import models
from convert import alpha
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections

schema_version = 40


# the 2 queries below are used to generate the 2D Histogram of position offset
# between Running Catalogs and Extracted Sources. The first query finds
# the minimum and maximum values for RA and DECL. these are used to scale
# the data. datapoints are grouped into integer groups.

minmax_query = """\
SELECT min(x.ra - r.wm_ra) as min_ra
  ,max(x.ra - r.wm_ra) as max_ra
  ,min(x.decl - r.wm_decl) as min_decl
  ,max(x.decl - r.wm_decl) as max_decl
FROM assocxtrsource a
  ,extractedsource x
  ,runningcatalog r
  ,image im1
WHERE a.runcat = r.id
AND a.xtrsrc = x.id
AND x.image = im1.id
AND im1.dataset = %s
"""

scaled_query = """\
SELECT ((sub.scaled_ra / (CAST(%(N_bins)s AS FLOAT) / (%(ra_max)s - %(ra_min)s))) + %(ra_min)s) * 3600
  , ((sub.scaled_decl  / (CAST(%(N_bins)s AS FLOAT) / (%(decl_max)s - %(decl_min)s))) + %(decl_min)s) * 3600
  ,count(sub.id)
FROM
  (SELECT r.id
    ,CAST((((x.ra - r.wm_ra) - %(ra_min)s ) * (CAST(%(N_bins)s AS FLOAT) / (%(ra_max)s - %(ra_min)s))
    ) AS INTEGER) AS scaled_ra
    ,CAST((((x.decl - r.wm_decl) - %(decl_min)s ) * (CAST(%(N_bins)s AS FLOAT) / (%(decl_max)s - %(decl_min)s))
    ) AS INTEGER) AS scaled_decl
  FROM assocxtrsource a
    ,extractedsource x
    ,runningcatalog r
    ,image im1
  WHERE a.runcat = r.id
  AND a.xtrsrc = x.id
  AND x.image = im1.id
  AND x.extract_type = 1
  AND im1.dataset = %(dataset)s
  ) AS sub
GROUP BY scaled_ra, scaled_decl
"""


class Assocskyrgn(models.Model):
    id = models.IntegerField(primary_key=True)
    runcat = models.ForeignKey('Runningcatalog', db_column='runcat',
                               related_name='assocskyrgns')
    skyrgn = models.ForeignKey('Skyregion', db_column='skyrgn',
                               related_name='assocskyrgns')
    distance_deg = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assocskyrgn'


class Assocxtrsource(models.Model):
    id = models.IntegerField(primary_key=True)
    runcat = models.ForeignKey('Runningcatalog', db_column='runcat',
                               related_name='assocxtrsources')


    xtrsrc = models.ForeignKey('Extractedsource', db_column='xtrsrc',
                               related_name='assocxtrsources',
                               blank=True, null=True)
    type = models.SmallIntegerField()
    distance_arcsec = models.FloatField(blank=True, null=True)
    r = models.FloatField(blank=True, null=True)
    loglr = models.FloatField(blank=True, null=True)
    v_int = models.FloatField()
    eta_int = models.FloatField()
    f_datapoints = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'assocxtrsource'


class Config(models.Model):
    id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey('Dataset', db_column='dataset', related_name='configs')
    section = models.CharField(max_length=100, blank=True)
    key = models.CharField(max_length=100, blank=True)
    value = models.CharField(max_length=500, blank=True)
    type = models.CharField(max_length=5, blank=True)

    class Meta:
        managed = False
        db_table = 'config'


class Dataset(models.Model):
    id = models.IntegerField(primary_key=True)
    rerun = models.IntegerField()
    type = models.SmallIntegerField()
    process_start_ts = models.DateTimeField()
    process_end_ts = models.DateTimeField(blank=True, null=True)
    detection_threshold = models.FloatField(blank=True, null=True)
    analysis_threshold = models.FloatField(blank=True, null=True)
    assoc_radius = models.FloatField(blank=True, null=True)
    backsize_x = models.SmallIntegerField(blank=True, null=True)
    backsize_y = models.SmallIntegerField(blank=True, null=True)
    margin_width = models.FloatField(blank=True, null=True)
    description = models.CharField(max_length=100)
    node = models.SmallIntegerField()
    nodes = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'dataset'

    def __unicode__(self):
        return self.description

    def newsources(self):
        return Newsource.objects.using(self._state.db). \
            filter(runcat__dataset=self)

    def extractedsources(self):
        return Extractedsource.objects.using(self._state.db). \
            filter(image__dataset=self)

    def heatmap(self, n_bins=21):
        """
        :param n_bins: the number of bins for each axes in the 2d histogram
        """
        cursor = connections[self._state.db].cursor()
        cursor.execute(minmax_query, [self.id])
        ra_min, ra_max, decl_min, decl_max = cursor.fetchall()[0]

        # handle case where returned values are None (no sources)
        if not (ra_min and ra_max and decl_min and decl_max):
            return []

        # handle case where all distances between extrsrc and runcat are same
        if ra_min == ra_max or decl_min == decl_max:
            return []

        # TODO: potential SQL injection here, but SQLite can't handle dict args
        cursor.execute(scaled_query % {'dataset': self.id, 'ra_min': ra_min,
                                       'ra_max': ra_max, 'decl_min': decl_min,
                                       'decl_max': decl_max,
                                       'N_bins': n_bins})
        return cursor.fetchall()

    def rejected_images(self):
        return Image.objects.using(self._state.db).filter(dataset=self). \
            annotate(num_rejections=Count('rejections')). \
            filter(num_rejections__gt=0)


class Extractedsource(models.Model):
    id = models.IntegerField(primary_key=True)
    image = models.ForeignKey('Image', db_column='image',
                              related_name='extractedsources')
    zone = models.IntegerField()
    ra = models.FloatField()
    decl = models.FloatField()
    uncertainty_ew = models.FloatField()
    uncertainty_ns = models.FloatField()
    ra_err = models.FloatField()
    decl_err = models.FloatField()
    ra_fit_err = models.FloatField()
    decl_fit_err = models.FloatField()
    ew_sys_err = models.FloatField()
    ns_sys_err = models.FloatField()
    error_radius = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    racosdecl = models.FloatField()
    margin = models.BooleanField(default=False)
    det_sigma = models.FloatField()
    semimajor = models.FloatField(blank=True, null=True)
    semiminor = models.FloatField(blank=True, null=True)
    pa = models.FloatField(blank=True, null=True)
    f_peak = models.FloatField(blank=True, null=True)
    f_peak_err = models.FloatField(blank=True, null=True)
    f_int = models.FloatField(blank=True, null=True)
    f_int_err = models.FloatField(blank=True, null=True)
    chisq= models.FloatField(blank=True, null=True)
    reduced_chisq= models.FloatField(blank=True, null=True)
    extract_type = models.SmallIntegerField(blank=True, null=True)
    fit_type = models.SmallIntegerField(blank=True, null=True)
    ff_runcat = models.ForeignKey('Runningcatalog', db_column='ff_runcat',
                                  blank=True, null=True)
    node = models.SmallIntegerField()
    nodes = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'extractedsource'

    def __unicode__(self):
        return str(self.id)


class Frequencyband(models.Model):
    id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey(Dataset, db_column='dataset')
    freq_central = models.FloatField(blank=True, null=True)
    freq_low = models.FloatField(blank=True, null=True)
    freq_high = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'frequencyband'

    def __unicode__(self):
        if self.freq_central:
            return "%s MHz" % int(self.freq_central / 10e5)
        else:
            return "0 MHz"


class Image(models.Model):
    id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey(Dataset, db_column='dataset',
                                related_name='images')
    tau = models.IntegerField(blank=True, null=True)
    band = models.ForeignKey(Frequencyband, db_column='band',
                             related_name='images')
    stokes = models.SmallIntegerField()
    tau_time = models.FloatField(blank=True, null=True)
    freq_eff = models.FloatField()
    freq_bw = models.FloatField(blank=True, null=True)
    taustart_ts = models.DateTimeField()
    skyrgn = models.ForeignKey('Skyregion', db_column='skyrgn',
                               related_name='images')
    rb_smaj = models.FloatField()
    rb_smin = models.FloatField()
    rb_pa = models.FloatField()
    deltax = models.FloatField()
    deltay = models.FloatField()
    fwhm_arcsec = models.FloatField(blank=True, null=True)
    fov_degrees = models.FloatField(blank=True, null=True)
    rms_qc = models.FloatField()
    rms_min = models.FloatField(blank=True, null=True)
    rms_max = models.FloatField(blank=True, null=True)
    detection_thresh = models.FloatField(blank=True, null=True)
    analysis_thresh = models.FloatField(blank=True, null=True)
    url = models.CharField(max_length=1024, blank=True)
    node = models.SmallIntegerField()
    nodes = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'image'

    def filename(self):
        if self.url:
            return self.url.split('/')[-1]
            
    def blind_extractedsources(self):
        """
        returns only the blindly extracted sources for the image (extract_type 0)
        """
        return Extractedsource.objects.using(self._state.db). \
            filter(image=self). \
            filter(extract_type=0)
            
    def forced_extractedsources(self):
        """
        returns only the forcefully extracted sources for the image (extract_type 1)
        """
        return Extractedsource.objects.using(self._state.db). \
            filter(image=self). \
            filter(extract_type=1)

    def get_next_previous(self):
        """
        returns previous image, limited by dataset, stokes and frequency,
        sorted by time.
        """
        qs = Image.objects.using(self._state.db)\
            .filter(dataset=self.dataset, band=self.band, stokes=self.stokes)\
            .order_by("taustart_ts")
        l = list(qs.values_list('id', flat=True))
        index = l.index(self.id)

        previous_index = index - 1
        if 0 <= previous_index < len(l):
            previous = Image.objects.using(self._state.db).get(id=l[previous_index])
        else:
            previous = None

        next_index = index + 1
        if 0 <= next_index < len(l):
            next = Image.objects.using(self._state.db).get(id=l[next_index])
        else:
            next = None

        return previous, next

    def __str__(self):
        return "image #%s" % self.id


class Imagedata(models.Model):
    image = models.OneToOneField(Image, db_column='image', related_name='data')
    fits_header = models.TextField(blank=True, null=True)
    fits_data = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imagedata'


class Monitor(models.Model):
    id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey(Dataset, db_column='dataset',
                                related_name='monitors')
    ra = models.FloatField()
    decl = models.FloatField()
    runcat = models.ForeignKey('Runningcatalog', db_column='runcat',
                               blank=True, null=True, related_name='monitors')
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monitor'


class Newsource(models.Model):
    id = models.IntegerField(primary_key=True)
    runcat = models.OneToOneField('Runningcatalog', db_column='runcat',
                                  related_name='newsource')
    trigger_xtrsrc = models.ForeignKey(Extractedsource,
                                       db_column='trigger_xtrsrc')
    newsource_type = models.SmallIntegerField()
    previous_limits_image = models.ForeignKey(Image,
                                              db_column='previous_limits_image')

    class Meta:
        managed = False
        db_table = 'newsource'

    def __str__(self):
        return 'newsource #%s' % self.id



class Node(models.Model):
    id = models.IntegerField(primary_key=True)
    node = models.SmallIntegerField()
    zone = models.SmallIntegerField()
    zone_min = models.SmallIntegerField(blank=True, null=True)
    zone_max = models.SmallIntegerField(blank=True, null=True)
    zone_min_incl = models.NullBooleanField()
    zone_max_incl = models.NullBooleanField()
    zoneheight = models.FloatField(blank=True, null=True)
    nodes = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'node'


class Rejection(models.Model):
    id = models.IntegerField(primary_key=True)
    image = models.ForeignKey(Image, db_column='image', blank=True, null=True,
                              related_name='rejections')
    rejectreason = models.ForeignKey('Rejectreason', db_column='rejectreason',
                                     blank=True, null=True)
    comment = models.CharField(max_length=512, blank=True)

    class Meta:
        managed = False
        db_table = 'rejection'

    def __unicode__(self):
        return "%s: %s" % (self.rejectreason, self.comment)


class Rejectreason(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=512, blank=True)

    class Meta:
        managed = False
        db_table = 'rejectreason'

    def __unicode__(self):
        return "%s" % self.description


class Runningcatalog(models.Model):
    id = models.IntegerField(primary_key=True)

    # we don't create a reverse mapping here, since this is only the first
    # extracted source
    xtrsrc = models.ForeignKey(Extractedsource, db_column='xtrsrc',
                               related_name='+')
    dataset = models.ForeignKey(Dataset, db_column='dataset',
                                related_name='runningcatalogs')
    datapoints = models.IntegerField()
    zone = models.IntegerField()
    wm_ra = models.FloatField()
    wm_decl = models.FloatField()
    wm_uncertainty_ew = models.FloatField()
    wm_uncertainty_ns = models.FloatField()
    avg_ra_err = models.FloatField()
    avg_decl_err = models.FloatField()
    avg_wra = models.FloatField()
    avg_wdecl = models.FloatField()
    avg_weight_ra = models.FloatField()
    avg_weight_decl = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    inactive = models.BooleanField(default=False)
    mon_src = models.BooleanField(default=False)
    extractedsources = models.ManyToManyField(Extractedsource,
                                              through=Assocxtrsource)

    skyregions = models.ManyToManyField('Skyregion', through=Assocskyrgn)
    forcedfits_count = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s" % self.id

    @property
    def ra_err(self):
        return alpha(self.wm_uncertainty_ew, self.wm_decl)

    @property
    def decl_err(self):
        return self.wm_uncertainty_ns


    class Meta:
        managed = False
        db_table = 'runningcatalog'


class RunningcatalogFlux(models.Model):
    id = models.IntegerField(primary_key=True)
    runcat = models.ForeignKey(Runningcatalog, db_column='runcat')
    band = models.ForeignKey(Frequencyband, db_column='band')
    stokes = models.SmallIntegerField()
    f_datapoints = models.IntegerField()
    avg_f_peak = models.FloatField(blank=True, null=True)
    avg_f_peak_sq = models.FloatField(blank=True, null=True)
    avg_f_peak_weight = models.FloatField(blank=True, null=True)
    avg_weighted_f_peak = models.FloatField(blank=True, null=True)
    avg_weighted_f_peak_sq = models.FloatField(blank=True, null=True)
    avg_f_int = models.FloatField(blank=True, null=True)
    avg_f_int_sq = models.FloatField(blank=True, null=True)
    avg_f_int_weight = models.FloatField(blank=True, null=True)
    avg_weighted_f_int = models.FloatField(blank=True, null=True)
    avg_weighted_f_int_sq = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
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

    def __unicode__(self):
        return "%s, %s" % (self.centre_ra, self.centre_decl)

    class Meta:
        managed = False
        db_table = 'skyregion'


class Temprunningcatalog(models.Model):
    id = models.IntegerField(primary_key=True)
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
    stokes = models.SmallIntegerField()
    datapoints = models.IntegerField()
    zone = models.IntegerField()
    wm_ra = models.FloatField()
    wm_decl = models.FloatField()
    wm_uncertainty_ew = models.FloatField()
    wm_uncertainty_ns = models.FloatField()
    avg_ra_err = models.FloatField()
    avg_decl_err = models.FloatField()
    avg_wra = models.FloatField()
    avg_wdecl = models.FloatField()
    avg_weight_ra = models.FloatField()
    avg_weight_decl = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    margin = models.BooleanField(default=False)
    inactive = models.BooleanField(default=False)
    beam_semimaj = models.FloatField(blank=True, null=True)
    beam_semimin = models.FloatField(blank=True, null=True)
    beam_pa = models.FloatField(blank=True, null=True)
    f_datapoints = models.IntegerField(blank=True, null=True)
    avg_f_peak = models.FloatField(blank=True, null=True)
    avg_f_peak_sq = models.FloatField(blank=True, null=True)
    avg_f_peak_weight = models.FloatField(blank=True, null=True)
    avg_weighted_f_peak = models.FloatField(blank=True, null=True)
    avg_weighted_f_peak_sq = models.FloatField(blank=True, null=True)
    avg_f_int = models.FloatField(blank=True, null=True)
    avg_f_int_sq = models.FloatField(blank=True, null=True)
    avg_f_int_weight = models.FloatField(blank=True, null=True)
    avg_weighted_f_int = models.FloatField(blank=True, null=True)
    avg_weighted_f_int_sq = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'temprunningcatalog'


class Varmetric(models.Model):
    id = models.IntegerField(primary_key=True)
    runcat = models.ForeignKey(Runningcatalog, db_column='runcat')
    v_int = models.FloatField(blank=True, null=True)
    eta_int = models.FloatField(blank=True, null=True)
    band = models.ForeignKey(Frequencyband, db_column='band')
    newsource = models.IntegerField(blank=True, null=True)
    sigma_rms_max = models.FloatField(blank=True, null=True)
    sigma_rms_min = models.FloatField(blank=True, null=True)
    lightcurve_max = models.FloatField(blank=True, null=True)
    lightcurve_avg = models.FloatField(blank=True, null=True)
    lightcurve_median = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'varmetric'


class Version(models.Model):
    name = models.CharField(max_length=12, primary_key=True)
    value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'version'
