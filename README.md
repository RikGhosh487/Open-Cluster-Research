# Open Cluster Research
This is the Data Science component of the **Astrometric**, **Photometric**, and **Spectroscopic** analysis of an Open Star Cluster.

>Structure of the Query region for Open Cluster<br />![Structure of region being Queried in Galactic Coordinates](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/Images/cluster_in_icrs.png)

>Vector Point Diagram of the Query region<br />![Vector Point Diagram of region being Queried](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/Images/vector_point_diagram.png)

>Parallax Distribution of Queried region<br />![Histogram with box plot for the distribution of Parallaxes for the Queried region](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/Images/parallax_distribution.png)

>Parallax Distrubution after Field Stars are removed<br />![Histogram with box plot for reduced distributio of Parallaxes for the Queried region](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/Images/reduced_parallax_distribution.png)

>Structure of the Query Region after Field Star removal<br />![Structure of Open Cluster queried in Galactic Coordinates](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/Images/cluster_in_icrs_post_parallax.png)

>Vector Point Diagram of the Query Region after Field Star removal<br />![Vector Point Diagram of Open Cluster after Field Star removal](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/Images/vpd_post_parallax.png)

>Color Magnitude Diagram of Open Cluster<br />![Scatterplot of Color Magnitude for Queried Open Cluster](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/Images/cmd.png)

## Current Data
| Paramater | Value |
| :--: | :--: |
| Right Ascension (α) | 235.486 |
| Declination (δ) | 11.093 |
| Parallax Data Retention | 7.96% |
| Raw Data Count | 7717 |
| Refined Data Count | 708 |
| Data Retention | 9.17% |

## Histograms
**Right Ascension (α)**<br />
![Right Ascension Histogram](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/Images/matplotlib/ra.png)
| Statistics | Value |
| :--: | :--: |
| Mean | 235.48177831737354 |
| Poisson Error | 0.06516604238717237 |
| Average Value | 235.482 ± 0.065 |

**Declination (δ)**
![Declination Histogram](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/Images/matplotlib/dec.png)
| Statistics | Value |
| :--: | :--: |
| Mean | 11.083738890559829 |
| Poisson Error | 0.30037020912563056 |
| Average Value | 11.084 ± 0.300 |

**Proper Motion in Right Ascension (μα)**
![Proper Motion in Right Ascension Histogram](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/Images/matplotlib/pmra.png)
| Statistics | Value |
| :--: | :--: |
| Mean | -5.5579432983169115 |
| Poisson Error | 0.4241729250792883 |
| Average Value | -5.558 ± 0.424 |

**Proper Motion in Declination (μδ)**
![Proper Motion in Declination Histogram](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/Images/matplotlib/pmdec.png)
| Statistics | Value |
| :--: | :--: |
| Mean | -6.120933518248045 |
| Poisson Error | 0.40419521581039136 |
| Average Value | -6.121 ± 0.404 |

**Parallax (π)**
![Parallax Histogram](https://github.com/RikGhosh487/Open-Cluster-Research/blob/main/Images/matplotlib/parallax.png)
| Statistics | Value |
| :--: | :--: |
| Mean | 0.9366727364406575 |
| Poisson Error | 1.0332515376519116 |
| Average Value | -0.937 ± 1.033 |

### Packages and Tools
- [Pandas](https://pandas.pydata.org/) - `v 1.2.4`
- [NumPy](https://numpy.org/) - `v 1.20.2`
- [SciPy](https://www.scipy.org/) - `v 1.6.2`
- [Plotly](https://plotly.com/) - `v 4.14.3`
- [Matplotlib](https://matplotlib.org) - `v 3.4.2`

### Source(s)
- [GAIA Early Data Release 3](https://www.cosmos.esa.int/web/gaia/early-data-release-3)
