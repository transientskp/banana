from __future__ import unicode_literals
from django.db import models
from convert import alpha
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections
from banana.managers import RunningcatalogManager

schema_version = 18


minmax_query = """\
SELECT min(x.ra - r.wm_ra)
  ,max(x.ra - r.wm_ra)
  ,min(x.decl - r.wm_decl)
  ,max(x.decl - r.wm_decl)
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
  ,((sub.scaled_decl  / (CAST(%(N_bins)s AS FLOAT) / (%(decl_max)s - %(decl_min)s))) + %(decl_min)s) * 3600
  ,count(sub.id)
FROM
  (SELECT r.id
    ,CAST((((x.ra - r.wm_ra) - %(decl_min)s ) * (CAST(%(N_bins)s AS FLOAT) / (%(ra_max)s - %(ra_min)s))
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


class Assoccatsource(models.Model):
    id = models.IntegerField(primary_key=True)
    xtrsrc = models.ForeignKey('Extractedsource', db_column='xtrsrc',
                               related_name='assoccatsources')
    catsrc = models.ForeignKey('Catalogedsource', db_column='catsrc',
                               related_name='assoccatsources')
    type = models.IntegerField()
    distance_arcsec = models.FloatField()
    r = models.FloatField()
    loglr = models.FloatField()

    class Meta:
        managed = False
        db_table = 'assoccatsource'


class Assocskyrgn(models.Model):
    id = models.IntegerField(primary_key=True)
    runcat = models.ForeignKey('Runningcatalog', db_column='runcat',
                               related_name='assocskyrgns')
    skyrgn = models.ForeignKey('Skyregion', db_column='skyrgn',
                               related_name='assocskyrgns')
    distance_deg = models.FloatField(null=True)

    class Meta:
        managed = False
        db_table = 'assocskyrgn'


class Assocxtrsource(models.Model):
    id = models.IntegerField(primary_key=True)
    runcat = models.ForeignKey('Runningcatalog', db_column='runcat',
                               related_name='Assocxtrsources')
    xtrsrc = models.ForeignKey('Extractedsource', db_column='xtrsrc',
                               related_name='asocxtrsources')
    type = models.IntegerField()
    distance_arcsec = models.FloatField()
    r = models.FloatField()
    loglr = models.FloatField(null=True)

    class Meta:
        managed = False
        db_table = 'assocxtrsource'


class Catalog(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    fullname = models.CharField(max_length=250)

    class Meta:
        managed = False
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
        managed = False
        db_table = 'catalogedsource'


class Classification(models.Model):
    id = models.IntegerField(primary_key=True)
    transient_id = models.IntegerField()
    classification = models.CharField(max_length=256)
    weight = models.FloatField()

    class Meta:
        managed = False
        db_table = 'classification'


class Dataset(models.Model):
    id = models.IntegerField(primary_key=True)
    rerun = models.IntegerField()
    type = models.IntegerField()
    process_start_ts = models.DateTimeField()
    process_end_ts = models.DateTimeField()
    detection_threshold = models.FloatField(null=True)
    analysis_threshold = models.FloatField(null=True)
    assoc_radius = models.FloatField(null=True)
    backsize_x = models.IntegerField(null=True)
    backsize_y = models.IntegerField(null=True)
    margin_width = models.FloatField(null=True)
    description = models.CharField(max_length=100)
    node = models.IntegerField()
    nodes = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dataset'

    def __unicode__(self):
        return self.description

    def transients(self):
        return Transient.objects.using(self._state.db).\
            filter(runcat__dataset=self)

    def extractedsources(self):
        return Extractedsource.objects.using(self._state.db).\
            filter(image__dataset=self)

    def heatmap(self, N_bins=21):
        """
        :param N_bins: the number of bins for each axes in the 2d histogram
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
                                      'N_bins': N_bins})
        return cursor.fetchall()


    def rejected_images(self):
        return Image.objects.using(self._state.db).filter(dataset=self).\
            annotate(num_rejections=Count('rejections')).\
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
        managed = False
        db_table = 'extractedsource'

    def __unicode__(self):
        return str(self.id)

    def runningcatalogs(self):
        assocs = Assocxtrsource.objects.using(self._state.db).\
            filter(xtrsrc=self.id)
        return [a.runcat for a in assocs]


class Frequencyband(models.Model):
    id = models.IntegerField(primary_key=True)
    freq_central = models.FloatField(null=True)
    freq_low = models.FloatField(null=True)
    freq_high = models.FloatField(null=True)

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
    tau = models.IntegerField(null=True)
    band = models.ForeignKey(Frequencyband, db_column='band',
                             related_name='images')
    stokes = models.IntegerField()
    tau_time = models.FloatField(null=True)
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
    fwhm_arcsec = models.FloatField(null=True)
    fov_degrees = models.FloatField(null=True)
    url = models.CharField(max_length=1024)
    node = models.IntegerField()
    nodes = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'image'

    def filename(self):
        return self.url.split('/')[-1]

    def get_next_by_taustart_ts_only(self):
        """
        returns next image, limited by dataset, stokes and frequency,
        sorted by time.
        """
        qs = Image.objects.using(self._state.db).\
            filter(dataset=self.dataset,
                   band=self.band,
                   stokes=self.stokes,
                   skyrgn=self.skyrgn
                   ).\
            order_by("taustart_ts")
        l = list(qs.values_list('id', flat=True))
        index = l.index(self.id)
        try:
            id = l[index+1]
        except IndexError:
            raise ObjectDoesNotExist
        return Image.objects.using(self._state.db).get(id=id)


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
        managed = False
        db_table = 'monitoringlist'


class Node(models.Model):
    id = models.IntegerField(primary_key=True)
    node = models.IntegerField()
    zone = models.IntegerField()
    zone_min = models.IntegerField()
    zone_max = models.IntegerField()
    zone_min_incl = models.BooleanField()
    zone_max_incl = models.BooleanField()
    zoneheight = models.FloatField()
    nodes = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'node'


class Rejection(models.Model):
    id = models.IntegerField(primary_key=True)
    image = models.ForeignKey(Image, db_column='image',
                              related_name='rejections')
    rejectreason = models.ForeignKey('Rejectreason', db_column='rejectreason')
    comment = models.CharField(max_length=512)

    class Meta:
        managed = False
        db_table = 'rejection'

    def __unicode__(self):
        return "%s: %s" % (self.rejectreason, self.comment)


class Rejectreason(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=512)

    class Meta:
        managed = False
        db_table = 'rejectreason'

    def __unicode__(self):
        return "%s" % (self.description)


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
    margin = models.BooleanField()
    inactive = models.BooleanField()

    objects = RunningcatalogManager()

    class Meta:
        managed = False
        db_table = 'runningcatalog'

    def __unicode__(self):
        return "%s" % (self.id)

    def lightcurve(self):
        assocs = Assocxtrsource.objects.using(self._state.db).filter(runcat=self.id)
        related = ['image', 'image__band']
        return Extractedsource.objects.using(self._state.db).filter(asocxtrsources__in=assocs).prefetch_related(*related)

    @property
    def ra_err(self):
        return alpha(self.wm_uncertainty_ew, self.wm_decl)
    @property
    def decl_err(self):
        return self.wm_uncertainty_ns


class RunningcatalogFlux(models.Model):
    id = models.IntegerField(primary_key=True)
    runcat = models.ForeignKey(Runningcatalog, db_column='runcat')
    band = models.ForeignKey(Frequencyband, db_column='band')
    stokes = models.IntegerField()
    f_datapoints = models.IntegerField()
    resolution = models.FloatField(null=True)
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
    stokes = models.IntegerField()
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
        managed = False
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
    t_start = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'transient'

    def __unicode__(self):
        return str(self.id)

    def lightcurve(self):
        assocs = Assocxtrsource.objects.using(self._state.db).\
            filter(runcat=self.runcat)
        related = ['image', 'image__band']
        return Extractedsource.objects.using(self._state.db).\
            filter(asocxtrsources__in=assocs).prefetch_related(*related)

    def index_in_dataset(self):
        #Memoize this, since it's not going to change
        # (unless a transient is deleted?)
        if not hasattr(self, '_index_in_dataset'):
            qs = Transient.objects.using(self._state.db).\
                filter(runcat__dataset=self.runcat.dataset,
                       ).\
                order_by("id")
            l = list(qs.values_list('id', flat=True))
            self._index_in_dataset = l.index(self.id)
        return self._index_in_dataset

    def number_in_dataset(self):
        num = Transient.objects.using(self._state.db).\
            filter(runcat__dataset=self.runcat.dataset).count()
        return num

    def get_next_by_id_offset(self, offset):
        """
        Returns transient 'offset' places away in list of transients.

        List is limited to parent dataset, sorted by id.

        If 'offset' places the next id outside the list,
        raises ObjectDoesNotExist error

        """
        qs = Transient.objects.using(self._state.db).\
            filter(runcat__dataset=self.runcat.dataset,
                   ).\
            order_by("id")
        l = list(qs.values_list('id', flat=True))

        index = l.index(self.id)
        offset_idx = index+offset

        if offset_idx<0 or offset_idx>=len(l):
            #Desired behaviour is to only return linear offsets
            #i.e. don't loop using -ve index behaviour!
            raise ObjectDoesNotExist

        id = l[offset_idx]
        return Transient.objects.using(self._state.db).get(id=id)

    def get_next_by_id(self):
        return self.get_next_by_id_offset(1)
    def get_prev_by_id(self):
        return self.get_next_by_id_offset(-1)



class Version(models.Model):
    name = models.CharField(max_length=12, primary_key=True)
    value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'version'
