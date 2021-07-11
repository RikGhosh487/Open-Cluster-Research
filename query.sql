SELECT
gaia_source.source_id, gaia_source.ra, gaia_source.ra_error, gaia_source.dec, gaia_source.dec_error,
gaia_source.parallax, gaia_source.parallax_error, gaia_source.pm, gaia_source.pmra, gaia_source.pmra_error,
gaia_source.pmdec, gaia_source.pmdec_error, gaia_source.parallax_pmra_corr, gaia_source.parallax_pmdec_corr,
gaia_source.pmra_pmdec_corr, gaia_source.phot_g_mean_mag, gaia_source.phot_bp_mean_mag,
gaia_source.phot_rp_mean_mag, gaia_source.bp_rp
FROM gaiaedr3.gaia_source 
WHERE 
CONTAINS(
	POINT('ICRS',gaiaedr3.gaia_source.ra,gaiaedr3.gaia_source.dec),
	CIRCLE('ICRS', 235.486, 11.093, 0.5)
)=1  AND  (gaiaedr3.gaia_source.parallax_error<=0.999999)
