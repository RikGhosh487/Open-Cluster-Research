/* 
	@author: Rik Ghosh
	@copyright: Copyright 2021, University of Texas at Austin
	@credits: Soham Saha, Mihir Suvarna
	@license: MIT
	@version: 1.0.1
	@maintainer: Rik Ghosh
	@email: rikghosh487@gmail.com
	@status: production
--*/

SELECT
p.u - p.g AS ug, -- color U - G, unit: mag, datatype: real
p.g - p.r AS gr, -- color G - R, unit: mag, datatype: real
p.r - p.i AS ri, -- color R - I, unit: mag, datatype: real
p.i - p.z AS iz, -- color I - Z, unit: mag, datatype: real
sp.teffadop AS teff, -- Teff, unit: K, datatype: real
sp.loggadop AS logg, -- Log g, unit: dex, datatype: real
sp.fehadop AS feh -- Fe/H, unit: dex, datatype: real

FROM sppParams AS sp
JOIN photoObj AS p ON p.objid = sp.bestobjid  -- joining SEGUE data with SDSS photometric data

WHERE
p.type = 6 AND  -- stars only
p.mode = 1 AND  -- removes duplicates
p.g <= 18 AND  -- only g mag <= 18
sp.flag like 'nnnnn' AND  -- normal SSPP flags
sp.fehdaopn >= 2 AND  -- atleast 2 SSPP readings
sp.teffadop >= 4500 AND sp.teffadop <= 7500 AND  -- 4500 <= Teff <= 7500
sp.fehadop != -9999 AND sp.loggadop != -9999  -- remove bad data
