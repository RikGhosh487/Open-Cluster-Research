# Open Cluster Research
This is the Data Science component of the **Astrometric**, **Photometric**, and **Spectroscopic** analysis of an Open Star Cluster.

## Search Parameters
| Parameter | Data |
| :--: | :--: |
| Right Ascension (α) | 345.67348 |
| Declination (δ) | 59.55911 |
| Search Radius | 40' |
| Database | [GAIA EDR3](https://www.cosmos.esa.int/web/gaia/early-data-release-3) |

There were **23117** data points in [raw_data.csv](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/csv/raw_data.csv). After dropping the rows with missing fields, there were **22442** data points. After enforcing statistical data reductions on the errors, there were **11980** data points that get compiled into [err_rm.csv](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/csv/err_rm.csv). DBSCAN was used to select the densest cluster in the Vector Point Diagram (VPD) to remove outliers and other noise. The resulting datafile had **10695** data points and was compiled into [reduced.csv](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/csv/reduced.csv). From that **68%** of the data was extracted to perform a *mean-centered* parallax, pmra, and pmdec adjustment and was compiled into [stat_adj.csv](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/csv/stat_adj.csv) which contains **3317** data points. A minimum spanning tree (MST) was then used to calculate the most likely members of the open cluster with the starting vertex at the densest point in the VPD. The algorithm determined the best transition point from the cluster to field, further reducing the data to **1710** data points. The new data was stored in [vpd_adj.csv](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/csv/vpd_adj.csv).Finally, a radius determination algorithm was used to find the final radius (`18 arcmins`) of the cluster, which brought down the data points to **769** datapoints. This final dataset was stored in [final.csv](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/csv/final.csv). Therefore, the total data reduction was **3.266%** from `raw_data.csv`.

## Histograms
***NOTE:*** All Margins of Error (M) are calculated using `M = 2 * std / sqrt(N)` where `std` is the standard deviation of the data, and `N` is the number of data points. This information was obtained from [Guide to Computing Margins of Error for Percentages and Means](http://crab.rutgers.edu/~goertzel/marginsoferror.htm)

**Right Ascension (α)**<br />
![Right Ascension Histogram](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/images/matplot/ra.png)
| Statistics | Value |
| :--: | :--: |
| Mean | 345.66314481804375 |
| Standard Deviation | 0.15144225704447303 |
| Margin of Error | 0.010922294928050361 |
| Average | 345.663 ± 0.011 |

**Declination (δ)**<br />
![Declination Histogram](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/images/matplot/dec.png)
| Statistics | Value |
| :--: | :--: |
| Mean | 59.53581462646116 |
| Standard Deviation | 0.1437598306538746 |
| Margin of Error | 0.010368224165776182 |
| Average | 59.536 ± 0.010 |

**Proper Motion in Right Ascension (μα)**<br />
![Proper Motion in Right Ascension Histogram](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/images/matplot/pmra.png)
| Statistics | Value |
| :--: | :--: |
| Mean | -2.760202412869038 |
| Standard Deviation | 0.4699322371922647 |
| Margin of Error | 0.033892379782118114 |
| Average | -2.760 ± 0.034 |

**Proper Motion in Declination (μδ)**<br />
![Proper Motion in Declination Histogram](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/images/matplot/pmdec.png)
| Statistics | Value |
| :--: | :--: |
| Mean | -1.6177784385191247 |
| Standard Deviation | 0.3804956560679288 |
| Margin of Error | 0.027442048576940464 |
| Average | -1.618 ± 0.027 |

**Parallax (π)**<br />
![Parallax Histogram](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/images/matplot/parallax.png)
| Statistics | Value |
| :--: | :--: |
| Mean | 0.24363781527560777 |
| Standard Deviation | 0.06721153470950784 |
| Margin of Error | 0.00484741986147604 |
| Average | 0.244 ± 0.005 |

## Spectroscopic Data
The **ugriz** filters in the SDSS database record the *Balmer Jump* and can be used to obtain spectroscopic information through a photometric estimation. A Machine Learning module is used to train and then test the data with existing spectroscopic information. Then, the paired data for the cluster in focus is fed into the model, which produces the best *Photometric Approximation* to the missing Spectroscopic data. The training data has **139555** data points with **ugriz** filters and spectroscopic data such as **Metallicity**. The [segue.csv](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/csv/segue.csv) file, containing the training data, is split into the train test models for the *Random Forest Regressor* to use on a `80% train - 20% test` ratio.

**Metallicity ([Fe/H])**<br />
![Metallicity Truth-to-Predicted Scatterplot](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/images/matplot/feh.png)
| Statistics | Value |
| :--: | :--: |
| Root Mean Square Error | 0.0828 |
| Catastrophic Prediction Error Rate | 0.0275 |
| Cluster Metallicity Value | -0.583106 |

### Packages and Tools
- [Pandas](https://pandas.pydata.org/) - `v 1.2.4`
- [NumPy](https://numpy.org/) - `v 1.20.2`
- [SciPy](https://www.scipy.org/) - `v 1.6.2`
- [Matplotlib](https://matplotlib.org) - `v 3.4.2`
- [Scikit-Learn](https://scikit-learn.org/stable/) - `v 0.24.2`

### Source(s)
- [Global Astrometric Interferometer for Astrophysics (GAIA) Early Data Release 3](https://www.cosmos.esa.int/web/gaia/early-data-release-3)
- [Sloan Digital Sky Survey Data (SDSS) Release 16](https://www.sdss.org/dr16/)
- [Sloan Extension for Galactic Understanding and Exploration (SEGUE) 2](http://www.sdss3.org/surveys/segue2.php)
