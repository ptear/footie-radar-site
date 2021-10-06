import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Radar
import io


def chart_maker(p1, p2, df, font_1, font_2, font_3):

    # inputs
    player_1 = p1
    player_2 = p2
    club_1 = df[df["Player"] == player_1]["Squad"].values[0]
    club_2 = df[df["Player"] == player_2]["Squad"].values[0]
    nineties_1 = df[df["Player"] == player_1]["90s"].values[0]
    nineties_2 = df[df["Player"] == player_2]["90s"].values[0]

    # compute and analyse
    df_new = pd.concat([df[(df["Player"] == player_1)], df[(df["Player"] == player_2)]]).reset_index()
    df_new = df_new.drop(
        ["index", "Rk", "Nation", "Pos", "Squad", "Age", "Born", "90s", "FK", "PK", "PKatt", "Matches"], axis=1)
    params = list(df_new.columns)
    params = params[1:]
    min_range = []
    max_range = []

    for x in params:
        a = min(df[x])
        min_range.append(a)
        b = max(df[x])
        max_range.append(b)

    a_values = df_new.iloc[0].values.tolist()[1:]
    b_values = df_new.iloc[1].values.tolist()[1:]

    def radar_mosaic(radar_height=0.915, title_height=0.06, figheight=14):
        """ Create a Radar chart flanked by a title and endnote axes.
        Parameters
        ----------
        radar_height: float, default 0.915
            The height of the radar axes in fractions of the figure height (default 91.5%).
        title_height: float, default 0.06
            The height of the title axes in fractions of the figure height (default 6%).
        figheight: float, default 14
            The figure height in inches.
        Returns
        -------
        fig : matplotlib.figure.Figure
        axs : dict[label, Axes]
        """
        if title_height + radar_height > 1:
            error_msg = 'Reduce one of the radar_height or title_height so the total is ≤ 1.'
            raise ValueError(error_msg)
        endnote_height = 1 - title_height - radar_height
        figwidth = figheight * radar_height
        figure, axes = plt.subplot_mosaic([['title'], ['radar'], ['endnote']],
                                          gridspec_kw={'height_ratios': [title_height, radar_height,
                                                                         endnote_height],
                                                       # the grid takes up the whole of the figure 0-1
                                                       'bottom': 0, 'left': 0, 'top': 1,
                                                       'right': 1, 'hspace': 0},
                                          figsize=(figwidth, figheight))
        axes['title'].axis('off')
        axes['endnote'].axis('off')
        return figure, axes

    radar = Radar(params=params, min_range=min_range, max_range=max_range)

    # creating the figure using the function defined above:
    fig, axs = radar_mosaic(radar_height=0.915, title_height=0.06, figheight=14)

    # plot radar
    radar.setup_axis(ax=axs['radar'])  # format axis as a radar
    rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#ffb2b2', edgecolor='#fc5f5f')
    radar_output = radar.draw_radar_compare(a_values, b_values, ax=axs['radar'],
                                            kwargs_radar={'facecolor': '#00f2c1', 'alpha': 0.6},
                                            kwargs_compare={'facecolor': '#d80499', 'alpha': 0.6})
    radar_poly, radar_poly2, vertices1, vertices2 = radar_output
    range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=25,
                                           fontproperties=font_1.prop)
    param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=25,
                                           fontproperties=font_2.prop)
    axs['radar'].scatter(vertices1[:, 0], vertices1[:, 1],
                         c='#00f2c1', edgecolors='#6d6c6d', marker='o', s=150, zorder=2)
    axs['radar'].scatter(vertices2[:, 0], vertices2[:, 1],
                         c='#d80499', edgecolors='#6d6c6d', marker='o', s=150, zorder=2)

    # adding the endnote and title text (these axes range from 0-1, i.e. 0, 0 is the bottom left)
    # Note we are slightly offsetting the text from the edges by 0.01 (1%, e.g. 0.99)
    endnote_text = axs['endnote'].text(0.99, 0.5, 'Inspired By: StatsBomb / Rami Moghadam', fontsize=15,
                                       fontproperties=font_1.prop, ha='right', va='center')
    titlexy_text= axs['title'].text(0.42, 0.25, "games played", fontsize=25, color='black',
                                    fontproperties=font_3.prop, ha='left', va='center')
    title1_text = axs['title'].text(0.01, 0.65, player_1, fontsize=25, color='#01c49d',
                                    fontproperties=font_3.prop, ha='left', va='center')
    title2_text = axs['title'].text(0.01, 0.25, club_1, fontsize=20,
                                    fontproperties=font_2.prop,
                                    ha='left', va='center', color='#01c49d')
    titlex_text = axs['title'].text(0.35, 0.25, nineties_1, fontsize=20,
                                    fontproperties=font_2.prop,
                                    ha='right', va='center', color='#01c49d')
    title3_text = axs['title'].text(0.99, 0.65, player_2, fontsize=25,
                                    fontproperties=font_3.prop,
                                    ha='right', va='center', color='#d80499')
    title4_text = axs['title'].text(0.99, 0.25, club_2, fontsize=20,
                                    fontproperties=font_2.prop,
                                    ha='right', va='center', color='#d80499')
    titley_text = axs['title'].text(0.65, 0.25, nineties_2, fontsize=20,
                                    fontproperties=font_2.prop,
                                    ha='left', va='center', color='#d80499')

    # convert to file-like data
    obj = io.BytesIO()             # file in memory to save image without using disk  #
    plt.savefig(obj, format='png')    # save in file (BytesIO) #
    plt.close()
    obj.seek(0)                    # move to beginning of file (BytesIO) to read it   #

    return obj
