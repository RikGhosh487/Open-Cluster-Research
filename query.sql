/* 
	@author: Rik Ghosh
	@copyright: Copyright 2021, University of Texas at Austin
	@credits: Soham Saha, Katherine Clark, Mihir Suvarna
	@license: MIT
	@version: 1.0.3
	@maintainer: Rik Ghosh
	@email: rikghosh487@gmail.com
	@status: production
--*/

SELECT
gaia_source.source_id, -- datatype: long
gaia_source.ra, -- unit: deg, datatype: double
gaia_source.ra_error, -- unit: mas, datatype: float
gaia_source.dec, -- unit: deg, datatype: double
gaia_source.dec_error, -- unit: mas, datatype: float
gaia_source.parallax, -- unit: mas, datatype: double
gaia_source.parallax_error, -- unit: mas, datatype: float
gaia_source.pm, -- unit: mas/yr, datatype: float
gaia_source.pmra, -- unit: mas/yr, datatype: double
gaia_source.pmra_error, -- unit: mas/yr, datatype: float
gaia_source.pmdec, -- unit: mas/yr, datatype: double
gaia_source.pmdec_error, -- unit: mas/yr, datatype: float
gaia_source.parallax_pmra_corr, -- datatype: float
gaia_source.parallax_pmdec_corr, -- datatype: float
gaia_source.pmra_pmdec_corr, -- datatype: float
gaia_source.phot_g_mean_mag, -- unit: mag, datatype: float
gaia_source.bp_rp, -- unit: mag, datatype: float
gaia_source.dr2_radial_velocity, -- unit: km/s, datatype: float
gaia_source.dr2_radial_velocity_error -- unit: km/s, datatype: float

FROM gaiaedr3.gaia_source

WHERE 
CONTAINS(
	POINT('ICRS', gaiaedr3.gaia_source.ra, gaiaedr3.gaia_source.dec),
	CIRCLE('ICRS', 345.67348, 59.55911, 0.16666666666667)
)=1  AND  (gaiaedr3.gaia_source.parallax_error < 1)
