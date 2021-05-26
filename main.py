import plotly.express as px
import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde

def main():
    # reading file
    df = pd.read_csv('result.csv')
    
    # statistical data reduction
    df = df[df['pmra_error'] < 1]
    df = df[df['pmdec_error'] < 1]

    # KDE color determination
    x = np.asarray(df['pmra'])
    y = np.asarray(df['pmdec'])
    xy = np.vstack([x, y])
    color = gaussian_kde(xy)(xy)
    df['color'] = color

    # hardcoded Data Reductions
    df = df[df['pmra'] <= 40]
    df = df[df['pmra'] >= -40]
    df = df[df['pmdec'] <= 40]
    df = df[df['pmdec'] >= -40]

    '''
    # Scatter Plot of Denisty Graph
    fig1 = px.scatter(df, x='pmra', y='pmdec', opacity=0.8, color='color', title='Density Graph',
                    color_continuous_scale='tealgrn',
                    labels={
                        'pmra': '\u03bc \u03b1 (mas/year)',
                        'pmdec': '\u03bc \u03b4 (mas/year)'
                    })
    fig1.update_traces(marker=dict(size=4))
    fig1.update_layout(height=550, width=550, autosize=False, plot_bgcolor='rgb(50,50,50)')
    fig1.show()
    # '''

    # parallax stat data
    meanp = np.mean(df['parallax'])
    stdp = np.std(df['parallax'])
    
    '''
    # Raw Histogram
    fig2 = px.histogram(df, x='parallax', opacity=0.8, title='Parallax Histogram',
                        marginal='rug',
                        labels={
                            'parallax': '\u03d6 (mas)'
                        })
    fig2.update_layout(autosize=False, plot_bgcolor='rgb(50,50,50)')
    fig2.show()
    # '''
    
    # data reductions for histogram
    df = df[df['parallax'] >= meanp - 0.17 * stdp]
    df = df[df['parallax'] <= meanp + 0.17 * stdp]

    '''
    # Refined Histogram
    fig4 = px.histogram(df, x='parallax', opacity=0.8, title='Reduced Parallax Histogram',
                        marginal='rug',
                        labels={
                            'parallax': '\u03d6 (mas)'
                        })
    fig4.update_layout(autosize=False, plot_bgcolor='rgb(50,50,50)')
    fig4.show()
    # '''

    # '''
    # VPD Scatter plot after adjusting for parallax
    fig5 = px.scatter(df, x='pmra', y='pmdec', opacity=0.8, color='color',
                    title='Parallax Adjusted Density Graph',
                    color_continuous_scale='tealgrn',
                    labels={
                        'pmra': '\u03bc \u03b1 (mas/year)',
                        'pmdec': '\u03bc \u03b4 (mas/year)'
                    })
    fig5.update_traces(marker=dict(size=4))
    fig5.update_layout(height=550, width=550, autosize=False, plot_bgcolor='rgb(50,50,50)')
    fig5.show()
    # '''

    print(len(df))

    fig6 = px.scatter(df, x='bp_rp', y='phot_g_mean_mag', opacity=0.8, color='color',
                      title='Color Magnitude Diagram', color_continuous_scale='tealgrn',
                      labels={
                          'bp_rp': 'BP - RP (mag)',
                          'phot_g_mean_mag': 'G (mag)'
                      })
    fig6.update_traces(marker=dict(size=4))
    fig6.update_layout(height=550, width=550, autosize=False, plot_bgcolor='rgb(50,50,50)',
                       yaxis=dict(autorange='reversed'))
    fig6.show()

if __name__ == '__main__':
    main()
    