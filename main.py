import plotly.express as px
import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde

BG_COLOR = 'rgb(50, 50, 50)'
OPACITY = 0.8
MARKER_SIZE = 4

# Assigns color based on Kernel Density Evaluation
def get_color_kde(dataframe):
    x = np.asarray(dataframe['pmra'])
    y = np.asarray(dataframe['pmdec'])
    xy = np.vstack([x, y])
    color = gaussian_kde(xy)(xy)
    dataframe['color'] = color
    return dataframe

# Generates scatterplot from the given parameters
def get_scatterplot(dataframe, paramx, paramy, dimensions, title='Scatterplot',
                    sequence='magma', display=False, reverse=False):
    if(display):
        fig = px.scatter(data_frame=dataframe, x=paramx['name'], y=paramy['name'], opacity=OPACITY,
                        color='color', title=title, color_continuous_scale=sequence,
                        labels={
                            paramx['name']: paramx['axis'],
                            paramy['name']: paramy['axis']
                        })
        fig.update_traces(marker=dict(size=MARKER_SIZE))
        if reverse:
            fig.update_layout(height=dimensions, width=dimensions, autosize=False, plot_bgcolor=BG_COLOR,
                            yaxis=dict(autorange='reversed'))
        else:
            fig.update_layout(height=dimensions, width=dimensions, autosize=False, plot_bgcolor=BG_COLOR)
        fig.show()

# Generates histogram from the given parameters
def get_histogram(dataframe, param, dimensions, title='Histogram', marginal='rug', display=False):
    if(display):
        fig = px.histogram(data_frame=dataframe, x=param['name'], opacity=OPACITY, title=title,
                           marginal=marginal, labels={ param['name']: param['axis']})
        fig.update_layout(autosize=False, plot_bgcolor=BG_COLOR)
        fig.show()

def main():
    # reading file
    df = pd.read_csv('vpd_adjust.csv')

    # KDE color determination
    df = get_color_kde(dataframe=df)

    # produces scatterplot for raw data with hard-coded data reductions
    get_scatterplot(dataframe=df, paramx=dict(name='pmra', axis='\u03bc \u03b1 (mas/year)'),
                    paramy=dict(name='pmdec', axis='\u03bc \u03b4 (mas/year)'), dimensions=550,
                    title='Vector Point Diagram (Density Graph)', sequence='tealgrn', display=False)
    
    get_scatterplot(dataframe=df, paramx=dict(name='ra', axis='\u03b1 (deg)'),
                    paramy=dict(name='dec', axis='\u03b4 (deg)'), dimensions=600,
                    title='Structure of Open Cluster (based on ICRS)', sequence='tealgrn', display=False)

    print(len(df))

    get_histogram(dataframe=df, param=dict(name='parallax', axis='\u03d6 (mas)'), dimensions=550,
                  title='Reduced Parallax Histogram', marginal='box', display=True)

    get_scatterplot(dataframe=df, paramx=dict(name='pmra', axis='\u03bc \u03b1 (mas/year)'),
                    paramy=dict(name='pmdec', axis='\u03bc \u03b4 (mas/year)'), dimensions=550,
                    title='Parallax Adjusted VPD Density Graph', sequence='tealgrn', display=True)

    get_scatterplot(dataframe=df, paramx=dict(name='ra', axis='\u03b1 (deg)'),
                    paramy=dict(name='dec', axis='\u03b4 (deg)'), dimensions=600,
                    title='Structure of Open Cluster (based on ICRS)', sequence='tealgrn', display=True)

    get_scatterplot(dataframe=df, paramx=dict(name='bp_rp', axis='BP - RP (mag)'),
                    paramy=dict(name='phot_g_mean_mag', axis='G (mag)'), dimensions=600,
                    title='Color Magnitude Diagram',sequence='tealgrn', display=True, reverse=True)

if __name__ == '__main__':
    main()
    