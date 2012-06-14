# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Versions(models.Model):
    versionid = models.IntegerField(primary_key=True)
    version = models.CharField(max_length=5)
    creation_ts = models.DateTimeField()
    monet_version = models.CharField(max_length=6)
    monet_release = models.CharField(max_length=11)
    scriptname = models.CharField(max_length=40)
    class Meta:
        managed=False
        db_table = u'versions'

class Frequencybands(models.Model):
    freqbandid = models.IntegerField(primary_key=True)
    freq_central = models.FloatField()
    freq_low = models.FloatField()
    freq_high = models.FloatField()

    class Meta:
        managed=False
        db_table = u'frequencybands'

    def __unicode__(self):
        if self.freq_central:
            return "%s MHz" % (int(self.freq_central/10**6),)
        else:
            return "0 MHz"

class Datasets(models.Model):
    dsid = models.IntegerField(primary_key=True)
    rerun = models.IntegerField()
    dstype = models.SmallIntegerField()
    process_ts = models.DateTimeField()
    dsinname = models.CharField(max_length=9)
    dsoutname = models.CharField(max_length=64)
    description = models.CharField(max_length=100)

    class Meta:
        managed=False
        db_table = u'datasets'

    def __unicode__(self):
        if self.description:
            return self.description
        elif self.dsinname:
            return self.dsinname
        else:
            return u"unnamed dataset"


class Images(models.Model):
    imageid = models.IntegerField(primary_key=True)
    ds = models.ForeignKey(Datasets)
    tau = models.IntegerField()
    band = models.ForeignKey(Frequencybands, db_column='band')
    stokes = models.CharField(max_length=1)
    tau_time = models.FloatField()
    freq_eff = models.FloatField()
    freq_bw = models.FloatField()
    taustart_ts = models.DateTimeField()
    #centr_ra = models.FloatField()
    #centr_decl = models.FloatField()
    #x = models.FloatField()
    #y = models.FloatField()
    #z = models.FloatField()
    #bsmaj = models.FloatField()
    #bsmin = models.FloatField()
    #bpa = models.FloatField()
    #fwhm_arcsec = models.FloatField()
    #fov_degrees = models.FloatField()
    url = models.CharField(max_length=1024)
    class Meta:
        managed=False
        db_table = u'images'

class Catalogs(models.Model):
    catid = models.IntegerField(primary_key=True)
    catname = models.CharField(max_length=4)
    fullname = models.CharField(max_length=33)
    class Meta:
        managed=False
        db_table = u'catalogs'

class Catalogedsources(models.Model):
    catsrcid = models.IntegerField(primary_key=True)
    cat = models.ForeignKey(Catalogs)
    orig_catsrcid = models.IntegerField()
    catsrcname = models.CharField(max_length=14)
    tau = models.IntegerField()
    band = models.ForeignKey(Frequencybands, db_column='band')
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
    ell_a = models.FloatField()
    ell_b = models.FloatField()
    pa = models.FloatField()
    pa_err = models.FloatField()
    major = models.FloatField()
    major_err = models.FloatField()
    minor = models.FloatField()
    minor_err = models.FloatField()
    i_peak_avg = models.FloatField()
    i_peak_avg_err = models.FloatField()
    i_peak_min = models.FloatField()
    i_peak_min_err = models.FloatField()
    i_peak_max = models.FloatField()
    i_peak_max_err = models.FloatField()
    i_int_avg = models.FloatField()
    i_int_avg_err = models.FloatField()
    i_int_min = models.FloatField()
    i_int_min_err = models.FloatField()
    i_int_max = models.FloatField()
    i_int_max_err = models.FloatField()
    frame = models.CharField(max_length=5)
    class Meta:
        managed=False
        db_table = u'catalogedsources'

class Extractedsources(models.Model):
    xtrsrcid = models.IntegerField(primary_key=True)
    image = models.ForeignKey(Images)
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
    semimajor = models.FloatField()
    semiminor = models.FloatField()
    pa = models.FloatField()
    i_peak = models.FloatField()
    i_peak_err = models.FloatField()
    i_int = models.FloatField()
    i_int_err = models.FloatField()
    node = models.SmallIntegerField()
    nodes = models.SmallIntegerField()
    class Meta:
        managed=False
        db_table = u'extractedsources'

class Assoccatsources(models.Model):
    xtrsrc_id = models.IntegerField()
    assoc_catsrc_id = models.IntegerField()
    assoc_weight = models.FloatField()
    assoc_distance_arcsec = models.FloatField()
    assoc_lr_method = models.IntegerField()
    assoc_r = models.FloatField()
    assoc_loglr = models.FloatField()
    class Meta:
        managed=False
        db_table = u'assoccatsources'

class Assocxtrsources(models.Model):
    xtrsrc_id = models.IntegerField()
    assoc_xtrsrc_id = models.IntegerField()
    assoc_weight = models.FloatField()
    assoc_distance_arcsec = models.FloatField()
    assoc_lr_method = models.IntegerField()
    assoc_r = models.FloatField()
    assoc_lr = models.FloatField()
    class Meta:
        managed=False
        db_table = u'assocxtrsources'

class Lsm(models.Model):
    lsmid = models.IntegerField(primary_key=True)
    cat_id = models.IntegerField()
    orig_catsrcid = models.IntegerField()
    catsrcname = models.CharField(max_length=120)
    tau = models.IntegerField()
    band = models.IntegerField()
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
    ell_a = models.FloatField()
    ell_b = models.FloatField()
    pa = models.FloatField()
    pa_err = models.FloatField()
    major = models.FloatField()
    major_err = models.FloatField()
    minor = models.FloatField()
    minor_err = models.FloatField()
    i_peak_avg = models.FloatField()
    i_peak_avg_err = models.FloatField()
    i_peak_min = models.FloatField()
    i_peak_min_err = models.FloatField()
    i_peak_max = models.FloatField()
    i_peak_max_err = models.FloatField()
    i_int_avg = models.FloatField()
    i_int_avg_err = models.FloatField()
    i_int_min = models.FloatField()
    i_int_min_err = models.FloatField()
    i_int_max = models.FloatField()
    i_int_max_err = models.FloatField()
    frame = models.CharField(max_length=100)
    class Meta:
        managed=False
        db_table = u'lsm'

class Spectralindices(models.Model):
    spindxid = models.IntegerField(primary_key=True)
    catsrc = models.ForeignKey(Catalogedsources)
    spindx_degree = models.IntegerField()
    c0 = models.FloatField()
    c1 = models.FloatField()
    c2 = models.FloatField()
    c3 = models.FloatField()
    c4 = models.FloatField()
    c5 = models.FloatField()
    class Meta:
        managed=False
        db_table = u'spectralindices'

class Runningcatalog(models.Model):
    xtrsrc_id = models.IntegerField()
    ds_id = models.IntegerField()
    band = models.IntegerField()
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
    beam_semimaj = models.FloatField()
    beam_semimin = models.FloatField()
    beam_pa = models.FloatField()
    avg_i_peak = models.FloatField()
    avg_i_peak_sq = models.FloatField()
    avg_weight_peak = models.FloatField()
    avg_weighted_i_peak = models.FloatField()
    avg_weighted_i_peak_sq = models.FloatField()
    class Meta:
        managed=False
        db_table = u'runningcatalog'

class Temprunningcatalog(models.Model):
    xtrsrc_id = models.IntegerField()
    assoc_xtrsrc_id = models.IntegerField()
    ds_id = models.IntegerField()
    band = models.IntegerField()
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
    beam_semimaj = models.FloatField()
    beam_semimin = models.FloatField()
    beam_pa = models.FloatField()
    avg_i_peak = models.FloatField()
    avg_i_peak_sq = models.FloatField()
    avg_weight_peak = models.FloatField()
    avg_weighted_i_peak = models.FloatField()
    avg_weighted_i_peak_sq = models.FloatField()
    class Meta:
        managed=False
        db_table = u'temprunningcatalog'

class Detections(models.Model):
    lra = models.FloatField()
    ldecl = models.FloatField()
    lra_err = models.FloatField()
    ldecl_err = models.FloatField()
    li_peak = models.FloatField()
    li_peak_err = models.FloatField()
    li_int = models.FloatField()
    li_int_err = models.FloatField()
    ldet_sigma = models.FloatField()
    lsemimajor = models.FloatField()
    lsemiminor = models.FloatField()
    lpa = models.FloatField()
    class Meta:
        managed=False
        db_table = u'detections'

class Node(models.Model):
    zone = models.IntegerField()
    zoneheight = models.FloatField()
    class Meta:
        managed=False
        db_table = u'node'

class Selectedcatsources(models.Model):
    catsrc_id = models.IntegerField()
    cat_id = models.IntegerField()
    zone = models.IntegerField()
    ra = models.FloatField()
    decl = models.FloatField()
    ra_err = models.FloatField()
    decl_err = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    margin = models.BooleanField()
    i_peak = models.FloatField()
    i_peak_err = models.FloatField()
    i_int = models.FloatField()
    i_int_err = models.FloatField()
    class Meta:
        managed=False
        db_table = u'selectedcatsources'

class Tempmergedcatalogs(models.Model):
    catsrc_id = models.IntegerField()
    assoc_catsrc_id = models.IntegerField()
    assoc_cat_id = models.IntegerField()
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
    i_peak = models.FloatField()
    i_int = models.FloatField()
    class Meta:
        managed=False
        db_table = u'tempmergedcatalogs'

class Mergedcatalogs(models.Model):
    catsrc_id = models.IntegerField()
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
    i_peak_vlss = models.FloatField()
    i_peak_vlss_err = models.FloatField()
    i_int_vlss = models.FloatField()
    i_int_vlss_err = models.FloatField()
    i_peak_wenssm = models.FloatField()
    i_peak_wenssm_err = models.FloatField()
    i_int_wenssm = models.FloatField()
    i_int_wenssm_err = models.FloatField()
    i_peak_wenssp = models.FloatField()
    i_peak_wenssp_err = models.FloatField()
    i_int_wenssp = models.FloatField()
    i_int_wenssp_err = models.FloatField()
    i_peak_nvss = models.FloatField()
    i_peak_nvss_err = models.FloatField()
    i_int_nvss = models.FloatField()
    i_int_nvss_err = models.FloatField()
    alpha_v_wm = models.FloatField()
    alpha_v_wp = models.FloatField()
    alpha_v_n = models.FloatField()
    alpha_wm_wp = models.FloatField()
    alpha_wm_n = models.FloatField()
    alpha_wp_n = models.FloatField()
    alpha_v_wm_n = models.FloatField()
    chisq_v_wm_n = models.FloatField()
    class Meta:
        managed=False
        db_table = u'mergedcatalogs'

class Assoccrosscatsources(models.Model):
    catsrc_id = models.IntegerField()
    assoc_catsrc_id = models.IntegerField()
    assoc_weight = models.FloatField()
    assoc_distance_arcsec = models.FloatField()
    assoc_lr_method = models.IntegerField()
    assoc_r = models.FloatField()
    assoc_lr = models.FloatField()
    class Meta:
        managed=False
        db_table = u'assoccrosscatsources'

class Monitoringlist(models.Model):
    monitorid = models.IntegerField(primary_key=True)
    xtrsrc_id = models.IntegerField()
    ra = models.FloatField()
    decl = models.FloatField()
    ds_id = models.IntegerField()
    userentry = models.BooleanField()
    class Meta:
        managed=False
        db_table = u'monitoringlist'

class Transients(models.Model):
    transientid = models.IntegerField(primary_key=True)
    xtrsrc_id = models.IntegerField()
    siglevel = models.FloatField()
    v = models.FloatField()
    eta = models.FloatField()
    detection_level = models.FloatField()
    trigger_xtrsrc_id = models.IntegerField()
    status = models.IntegerField()
    t_start = models.DateTimeField()
    class Meta:
        managed=False
        db_table = u'transients'

class Classification(models.Model):
    transient_id = models.IntegerField()
    classification = models.CharField(max_length=1024)
    weight = models.FloatField()
    class Meta:
        managed=False
        db_table = u'classification'

