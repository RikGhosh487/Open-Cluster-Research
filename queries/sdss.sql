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
p.ra,  -- unit: deg, datatype: real
p.dec,  -- unit: deg, datatype: real
p.u - p.g AS ug, -- color U - G, unit: mag, datatype: real
p.g - p.r AS gr, -- color G - R, unit: mag, datatype: real
p.r - p.i AS ri, -- color R - I, unit: mag, datatype: real
p.i - p.z AS iz -- color I - Z, unit: mag, datatype: real

FROM photoObj AS p
JOIN dbo.fGetNearbyObjEq(345.67348, 59.55911, 20) AS n ON n.objid = p.objid

WHERE
p.type = 6 AND  -- stars only
p.mode = 1 AND  -- duplicated removed
p.g <= 18  -- only g mag <= 18
