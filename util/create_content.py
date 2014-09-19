"""
Populate a TKP database with Mock data.
"""
import tkp.db
from tkp.testutil import db_subs


def main():
    database = tkp.db.Database()
    dataset = tkp.db.DataSet(data={'description': "Banana test data"},
                             database=database)

    n_images = 4
    new_source_sigma_margin = 3
    image_rms = 1e-3
    detection_thresh = 10

    reliably_detectable_flux = 1.01 * image_rms * (detection_thresh +
                                                   new_source_sigma_margin)

    # 1mJy image RMS, 10-sigma detection threshold = 10mJy threshold.
    test_specific_img_params = {'rms_qc': image_rms, 'rms_min': image_rms,
                                'rms_max': image_rms,
                                'detection_thresh': detection_thresh}

    im_params = db_subs.generate_timespaced_dbimages_data(n_images,
                                                          **test_specific_img_params)

    src_tuple = db_subs.example_extractedsource_tuple(ra=im_params[0]['centre_ra'],
                                                      dec=im_params[0]['centre_decl'],)
    transient_src = db_subs.MockSource(
        template_extractedsource=src_tuple,
        lightcurve={im_params[2]['taustart_ts']:
                        reliably_detectable_flux}
    )

    for img_pars in im_params:
        db_subs.insert_image_and_simulated_sources(dataset, img_pars,
                                                   [transient_src],
                                                   new_source_sigma_margin)
    tkp.db.commit()



if __name__ == '__main__':
    main()