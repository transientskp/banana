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
    versionid = models.IntegerField()
    version = models.CharField(max_length=5)
    creation_ts = models.DateTimeField()
    monet_version = models.CharField(max_length=7)
    monet_release = models.CharField(max_length=10)
    scriptname = models.CharField(max_length=40)
    class Meta:
        db_table = u'versions'

class Frequencybands(models.Model):
    freqbandid = models.IntegerField()
    freq_central = models.TextField() # This field type is a guess.
    freq_low = models.TextField() # This field type is a guess.
    freq_high = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'frequencybands'

class Datasets(models.Model):
    dsid = models.IntegerField()
    rerun = models.IntegerField()
    dstype = models.TextField() # This field type is a guess.
    process_ts = models.DateTimeField()
    dsinname = models.CharField(max_length=20)
    dsoutname = models.CharField()
    description = models.CharField()
    class Meta:
        db_table = u'datasets'

class Images(models.Model):
    imageid = models.IntegerField()
    ds_id = models.IntegerField()
    tau = models.IntegerField()
    band = models.IntegerField()
    stokes = models.TextField() # This field type is a guess.
    tau_time = models.TextField() # This field type is a guess.
    freq_eff = models.TextField() # This field type is a guess.
    freq_bw = models.TextField() # This field type is a guess.
    taustart_ts = models.DateTimeField()
    centr_ra = models.TextField() # This field type is a guess.
    centr_decl = models.TextField() # This field type is a guess.
    x = models.TextField() # This field type is a guess.
    y = models.TextField() # This field type is a guess.
    z = models.TextField() # This field type is a guess.
    bsmaj = models.TextField() # This field type is a guess.
    bsmin = models.TextField() # This field type is a guess.
    bpa = models.TextField() # This field type is a guess.
    fwhm_arcsec = models.TextField() # This field type is a guess.
    fov_degrees = models.TextField() # This field type is a guess.
    url = models.CharField(max_length=52)
    class Meta:
        db_table = u'images'

class Catalogs(models.Model):
    catid = models.IntegerField()
    catname = models.CharField(max_length=4)
    fullname = models.CharField(max_length=33)
    class Meta:
        db_table = u'catalogs'

class Catalogedsources(models.Model):
    catsrcid = models.IntegerField()
    cat_id = models.IntegerField()
    orig_catsrcid = models.IntegerField()
    catsrcname = models.CharField(max_length=14)
    tau = models.IntegerField()
    band = models.IntegerField()
    freq_eff = models.TextField() # This field type is a guess.
    zone = models.IntegerField()
    ra = models.TextField() # This field type is a guess.
    decl = models.TextField() # This field type is a guess.
    ra_err = models.TextField() # This field type is a guess.
    decl_err = models.TextField() # This field type is a guess.
    x = models.TextField() # This field type is a guess.
    y = models.TextField() # This field type is a guess.
    z = models.TextField() # This field type is a guess.
    margin = models.BooleanField()
    det_sigma = models.TextField() # This field type is a guess.
    src_type = models.CharField()
    fit_probl = models.CharField()
    ell_a = models.TextField() # This field type is a guess.
    ell_b = models.TextField() # This field type is a guess.
    pa = models.TextField() # This field type is a guess.
    pa_err = models.TextField() # This field type is a guess.
    major = models.TextField() # This field type is a guess.
    major_err = models.TextField() # This field type is a guess.
    minor = models.TextField() # This field type is a guess.
    minor_err = models.TextField() # This field type is a guess.
    i_peak_avg = models.TextField() # This field type is a guess.
    i_peak_avg_err = models.TextField() # This field type is a guess.
    i_peak_min = models.TextField() # This field type is a guess.
    i_peak_min_err = models.TextField() # This field type is a guess.
    i_peak_max = models.TextField() # This field type is a guess.
    i_peak_max_err = models.TextField() # This field type is a guess.
    i_int_avg = models.TextField() # This field type is a guess.
    i_int_avg_err = models.TextField() # This field type is a guess.
    i_int_min = models.TextField() # This field type is a guess.
    i_int_min_err = models.TextField() # This field type is a guess.
    i_int_max = models.TextField() # This field type is a guess.
    i_int_max_err = models.TextField() # This field type is a guess.
    frame = models.CharField(max_length=5)
    class Meta:
        db_table = u'catalogedsources'

class Extractedsources(models.Model):
    xtrsrcid = models.IntegerField()
    image_id = models.IntegerField()
    zone = models.IntegerField()
    ra = models.TextField() # This field type is a guess.
    decl = models.TextField() # This field type is a guess.
    ra_err = models.TextField() # This field type is a guess.
    decl_err = models.TextField() # This field type is a guess.
    x = models.TextField() # This field type is a guess.
    y = models.TextField() # This field type is a guess.
    z = models.TextField() # This field type is a guess.
    margin = models.BooleanField()
    det_sigma = models.TextField() # This field type is a guess.
    semimajor = models.TextField() # This field type is a guess.
    semiminor = models.TextField() # This field type is a guess.
    pa = models.TextField() # This field type is a guess.
    i_peak = models.TextField() # This field type is a guess.
    i_peak_err = models.TextField() # This field type is a guess.
    i_int = models.TextField() # This field type is a guess.
    i_int_err = models.TextField() # This field type is a guess.
    node = models.TextField() # This field type is a guess.
    nodes = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'extractedsources'

class Assoccatsources(models.Model):
    xtrsrc_id = models.IntegerField(null=False)
    assoc_catsrc_id = models.IntegerField(null=False)
    assoc_weight = models.FloatField()
    assoc_distance_arcsec = models.FloatField()
    assoc_lr_method = models.IntegerField(null=False, default=0)
    assoc_r = models.FloatField()
    assoc_loglr = models.FloatField()
    class Meta:
        db_table = u'assoccatsources'
        managed = False

class Assocxtrsources(models.Model):
    xtrsrc_id = models.IntegerField()
    assoc_xtrsrc_id = models.IntegerField()
    assoc_weight = models.TextField() # This field type is a guess.
    assoc_distance_arcsec = models.TextField() # This field type is a guess.
    assoc_lr_method = models.IntegerField()
    assoc_r = models.TextField() # This field type is a guess.
    assoc_lr = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'assocxtrsources'

class Lsm(models.Model):
    lsmid = models.IntegerField()
    cat_id = models.IntegerField()
    orig_catsrcid = models.IntegerField()
    catsrcname = models.CharField()
    tau = models.IntegerField()
    band = models.IntegerField()
    freq_eff = models.TextField() # This field type is a guess.
    zone = models.IntegerField()
    ra = models.TextField() # This field type is a guess.
    decl = models.TextField() # This field type is a guess.
    ra_err = models.TextField() # This field type is a guess.
    decl_err = models.TextField() # This field type is a guess.
    x = models.TextField() # This field type is a guess.
    y = models.TextField() # This field type is a guess.
    z = models.TextField() # This field type is a guess.
    margin = models.BooleanField()
    det_sigma = models.TextField() # This field type is a guess.
    src_type = models.CharField()
    fit_probl = models.CharField()
    ell_a = models.TextField() # This field type is a guess.
    ell_b = models.TextField() # This field type is a guess.
    pa = models.TextField() # This field type is a guess.
    pa_err = models.TextField() # This field type is a guess.
    major = models.TextField() # This field type is a guess.
    major_err = models.TextField() # This field type is a guess.
    minor = models.TextField() # This field type is a guess.
    minor_err = models.TextField() # This field type is a guess.
    i_peak_avg = models.TextField() # This field type is a guess.
    i_peak_avg_err = models.TextField() # This field type is a guess.
    i_peak_min = models.TextField() # This field type is a guess.
    i_peak_min_err = models.TextField() # This field type is a guess.
    i_peak_max = models.TextField() # This field type is a guess.
    i_peak_max_err = models.TextField() # This field type is a guess.
    i_int_avg = models.TextField() # This field type is a guess.
    i_int_avg_err = models.TextField() # This field type is a guess.
    i_int_min = models.TextField() # This field type is a guess.
    i_int_min_err = models.TextField() # This field type is a guess.
    i_int_max = models.TextField() # This field type is a guess.
    i_int_max_err = models.TextField() # This field type is a guess.
    frame = models.CharField()
    class Meta:
        db_table = u'lsm'

class Spectralindices(models.Model):
    spindxid = models.IntegerField()
    catsrc_id = models.IntegerField()
    spindx_degree = models.IntegerField()
    c0 = models.TextField() # This field type is a guess.
    c1 = models.TextField() # This field type is a guess.
    c2 = models.TextField() # This field type is a guess.
    c3 = models.TextField() # This field type is a guess.
    c4 = models.TextField() # This field type is a guess.
    c5 = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'spectralindices'

class Runningcatalog(models.Model):
    xtrsrc_id = models.IntegerField()
    ds_id = models.IntegerField()
    band = models.IntegerField()
    datapoints = models.IntegerField()
    zone = models.IntegerField()
    wm_ra = models.TextField() # This field type is a guess.
    wm_decl = models.TextField() # This field type is a guess.
    wm_ra_err = models.TextField() # This field type is a guess.
    wm_decl_err = models.TextField() # This field type is a guess.
    avg_wra = models.TextField() # This field type is a guess.
    avg_wdecl = models.TextField() # This field type is a guess.
    avg_weight_ra = models.TextField() # This field type is a guess.
    avg_weight_decl = models.TextField() # This field type is a guess.
    x = models.TextField() # This field type is a guess.
    y = models.TextField() # This field type is a guess.
    z = models.TextField() # This field type is a guess.
    margin = models.BooleanField()
    beam_semimaj = models.TextField() # This field type is a guess.
    beam_semimin = models.TextField() # This field type is a guess.
    beam_pa = models.TextField() # This field type is a guess.
    avg_i_peak = models.TextField() # This field type is a guess.
    avg_i_peak_sq = models.TextField() # This field type is a guess.
    avg_weight_peak = models.TextField() # This field type is a guess.
    avg_weighted_i_peak = models.TextField() # This field type is a guess.
    avg_weighted_i_peak_sq = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'runningcatalog'

class Temprunningcatalog(models.Model):
    xtrsrc_id = models.IntegerField()
    assoc_xtrsrc_id = models.IntegerField()
    ds_id = models.IntegerField()
    band = models.IntegerField()
    datapoints = models.IntegerField()
    zone = models.IntegerField()
    wm_ra = models.TextField() # This field type is a guess.
    wm_decl = models.TextField() # This field type is a guess.
    wm_ra_err = models.TextField() # This field type is a guess.
    wm_decl_err = models.TextField() # This field type is a guess.
    avg_wra = models.TextField() # This field type is a guess.
    avg_wdecl = models.TextField() # This field type is a guess.
    avg_weight_ra = models.TextField() # This field type is a guess.
    avg_weight_decl = models.TextField() # This field type is a guess.
    x = models.TextField() # This field type is a guess.
    y = models.TextField() # This field type is a guess.
    z = models.TextField() # This field type is a guess.
    margin = models.BooleanField()
    beam_semimaj = models.TextField() # This field type is a guess.
    beam_semimin = models.TextField() # This field type is a guess.
    beam_pa = models.TextField() # This field type is a guess.
    avg_i_peak = models.TextField() # This field type is a guess.
    avg_i_peak_sq = models.TextField() # This field type is a guess.
    avg_weight_peak = models.TextField() # This field type is a guess.
    avg_weighted_i_peak = models.TextField() # This field type is a guess.
    avg_weighted_i_peak_sq = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'temprunningcatalog'

class Detections(models.Model):
    lra = models.TextField() # This field type is a guess.
    ldecl = models.TextField() # This field type is a guess.
    lra_err = models.TextField() # This field type is a guess.
    ldecl_err = models.TextField() # This field type is a guess.
    li_peak = models.TextField() # This field type is a guess.
    li_peak_err = models.TextField() # This field type is a guess.
    li_int = models.TextField() # This field type is a guess.
    li_int_err = models.TextField() # This field type is a guess.
    ldet_sigma = models.TextField() # This field type is a guess.
    lsemimajor = models.TextField() # This field type is a guess.
    lsemiminor = models.TextField() # This field type is a guess.
    lpa = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'detections'

class Node(models.Model):
    zone = models.IntegerField()
    zoneheight = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'node'

class Selectedcatsources(models.Model):
    catsrc_id = models.IntegerField()
    cat_id = models.IntegerField()
    zone = models.IntegerField()
    ra = models.TextField() # This field type is a guess.
    decl = models.TextField() # This field type is a guess.
    ra_err = models.TextField() # This field type is a guess.
    decl_err = models.TextField() # This field type is a guess.
    x = models.TextField() # This field type is a guess.
    y = models.TextField() # This field type is a guess.
    z = models.TextField() # This field type is a guess.
    margin = models.BooleanField()
    i_peak = models.TextField() # This field type is a guess.
    i_peak_err = models.TextField() # This field type is a guess.
    i_int = models.TextField() # This field type is a guess.
    i_int_err = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'selectedcatsources'

class Tempmergedcatalogs(models.Model):
    catsrc_id = models.IntegerField()
    assoc_catsrc_id = models.IntegerField()
    assoc_cat_id = models.IntegerField()
    datapoints = models.IntegerField()
    zone = models.IntegerField()
    wm_ra = models.TextField() # This field type is a guess.
    wm_decl = models.TextField() # This field type is a guess.
    wm_ra_err = models.TextField() # This field type is a guess.
    wm_decl_err = models.TextField() # This field type is a guess.
    avg_wra = models.TextField() # This field type is a guess.
    avg_wdecl = models.TextField() # This field type is a guess.
    avg_weight_ra = models.TextField() # This field type is a guess.
    avg_weight_decl = models.TextField() # This field type is a guess.
    x = models.TextField() # This field type is a guess.
    y = models.TextField() # This field type is a guess.
    z = models.TextField() # This field type is a guess.
    margin = models.BooleanField()
    i_peak = models.TextField() # This field type is a guess.
    i_int = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'tempmergedcatalogs'

class Mergedcatalogs(models.Model):
    catsrc_id = models.IntegerField()
    datapoints = models.IntegerField()
    zone = models.IntegerField()
    wm_ra = models.TextField() # This field type is a guess.
    wm_decl = models.TextField() # This field type is a guess.
    wm_ra_err = models.TextField() # This field type is a guess.
    wm_decl_err = models.TextField() # This field type is a guess.
    avg_wra = models.TextField() # This field type is a guess.
    avg_wdecl = models.TextField() # This field type is a guess.
    avg_weight_ra = models.TextField() # This field type is a guess.
    avg_weight_decl = models.TextField() # This field type is a guess.
    x = models.TextField() # This field type is a guess.
    y = models.TextField() # This field type is a guess.
    z = models.TextField() # This field type is a guess.
    margin = models.BooleanField()
    i_peak_vlss = models.TextField() # This field type is a guess.
    i_peak_vlss_err = models.TextField() # This field type is a guess.
    i_int_vlss = models.TextField() # This field type is a guess.
    i_int_vlss_err = models.TextField() # This field type is a guess.
    i_peak_wenssm = models.TextField() # This field type is a guess.
    i_peak_wenssm_err = models.TextField() # This field type is a guess.
    i_int_wenssm = models.TextField() # This field type is a guess.
    i_int_wenssm_err = models.TextField() # This field type is a guess.
    i_peak_wenssp = models.TextField() # This field type is a guess.
    i_peak_wenssp_err = models.TextField() # This field type is a guess.
    i_int_wenssp = models.TextField() # This field type is a guess.
    i_int_wenssp_err = models.TextField() # This field type is a guess.
    i_peak_nvss = models.TextField() # This field type is a guess.
    i_peak_nvss_err = models.TextField() # This field type is a guess.
    i_int_nvss = models.TextField() # This field type is a guess.
    i_int_nvss_err = models.TextField() # This field type is a guess.
    alpha_v_wm = models.TextField() # This field type is a guess.
    alpha_v_wp = models.TextField() # This field type is a guess.
    alpha_v_n = models.TextField() # This field type is a guess.
    alpha_wm_wp = models.TextField() # This field type is a guess.
    alpha_wm_n = models.TextField() # This field type is a guess.
    alpha_wp_n = models.TextField() # This field type is a guess.
    alpha_v_wm_n = models.TextField() # This field type is a guess.
    chisq_v_wm_n = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'mergedcatalogs'

class Assoccrosscatsources(models.Model):
    catsrc_id = models.IntegerField()
    assoc_catsrc_id = models.IntegerField()
    assoc_weight = models.TextField() # This field type is a guess.
    assoc_distance_arcsec = models.TextField() # This field type is a guess.
    assoc_lr_method = models.IntegerField()
    assoc_r = models.TextField() # This field type is a guess.
    assoc_lr = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'assoccrosscatsources'

class Monitoringlist(models.Model):
    monitorid = models.IntegerField()
    xtrsrc_id = models.IntegerField()
    ra = models.TextField() # This field type is a guess.
    decl = models.TextField() # This field type is a guess.
    ds_id = models.IntegerField()
    userentry = models.BooleanField()
    class Meta:
        db_table = u'monitoringlist'

class Transients(models.Model):
    transientid = models.IntegerField()
    xtrsrc_id = models.IntegerField()
    siglevel = models.TextField() # This field type is a guess.
    v = models.TextField() # This field type is a guess.
    eta = models.TextField() # This field type is a guess.
    detection_level = models.TextField() # This field type is a guess.
    trigger_xtrsrc_id = models.IntegerField()
    status = models.IntegerField()
    t_start = models.DateTimeField()
    class Meta:
        db_table = u'transients'

class Classification(models.Model):
    transient_id = models.IntegerField()
    classification = models.CharField()
    weight = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'classification'

