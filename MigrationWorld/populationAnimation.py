import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import animation as anm
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import itertools
import matplotlib.ticker as ticker
from PIL import Image
from time import sleep


def loadFlags(df):
    """load flag image for countries"""
    flag_img = {}
    for c in df['ISO3_code'].unique():
        try:
            img = Image.open(f'PopulationWorld/img/{c}.png')
            img.thumbnail((50,30), Image.Resampling.LANCZOS)
            flag_img[c] = img
        except:
            pass
    return flag_img

def formatPlot(ax):
    """Format a matplotlib axes for a bar chart of population by country
    
    Remove top and right spines, set title, x-axis label, and tick parameters.
    """
    
    ax.set_yticks([])
    ax.spines['right'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_title('Top 10 Countries by Population 1950-2024', 
                 pad = 20, 
                 fontsize=24,
                 fontweight = 'bold')    
    ax.set_xlabel('Total Population (millions)',
                  va = 'top',
                  labelpad = 15,
                  fontsize = 20,
                  fontweight = 'bold')
    ax.tick_params(axis='y', which = 'both', left = False)
    ax.tick_params(axis='x', which = 'both', bottom = False, labelsize = 14)
    
# def setup_plot_style(ax):
#     """Apply consistent plot styling"""
#     ax.set_xlabel('Population (in millions)', fontsize = 20, fontweight = 'bold')
#     ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
#     ax.grid(True, axis='x', linestyle='--', alpha=0.7)
#     ax.spines['top'].set_visible(False)
#     ax.spines['right'].set_visible(False)
#     ax.set_title('Top 10 Populations', pad=20, fontsize = 24, fontweight = 'bold')

def create_animation(df):
    plt.rc('font',weight = 'bold')
    fig, ax = plt.subplots(figsize = (16,9))
    flags = loadFlags(df)
    ax.set
    frames = df['Time'].unique()
    def animate(frame):
        # for month in range(1, 13):
        year= frame//100
        ax.clear()
        
        # add year
        ax.text(0.9,0.1, 
                str(year), 
                transform = ax.transAxes, 
                ha = 'center', 
                fontsize = 24)
        # Countries needing extra space to prevent jitter
        # unstable_names = {'Germany', 'Mexico', 'Ethiopia', 'Bangladesh'}
        # main bar 
        largest_migration = df.loc[(df['Time']==frame)].nlargest(10,columns='NetMigrations').sort_values('NetMigrations',ascending=True)
        smallest_migration = df.loc[(df['Time']==frame)].nsmallest(10,columns='NetMigrations').sort_values('NetMigrations', ascending=True)
        migration_mix = pd.concat([smallest_migration,largest_migration])
            
        ax.barh(migration_mix['Location'], 
                migration_mix['NetMigrations'],
                alpha = 0.3)

        # element for each country
        for i, row in migration_mix.iterrows():
            if row['ISO3_code'] in flags:
                img_box = OffsetImage(flags[row['ISO3_code']], zoom=0.5)
                ab = AnnotationBbox(img_box, (1, row['Location']),
                                  frameon=False,
                                  box_alignment=(0, 0.5),
                                  xybox=(-30, 0),
                                #   xycoords=('data', 'data'),
                                  boxcoords="offset points")
                ax.add_artist(ab)

            # number
            ax.text(row['NetMigrations']+10, 
                    row['Location'], 
                    f"{row['NetMigrations']:,.2f}", 
                    va = 'center',
                    ha = 'left',
                    fontsize = 16)
                      
            # country_name = f"{row['Location']}  " if row['Location'] in unstable_names else row['Location']
            country_name = f"{row['Location']} "
            ax.text(-0.05, row['Location'], 
                    country_name, 
                    ha='right', 
                    va='center', 
                    transform=ax.get_yaxis_transform(),
                    fontsize = 16)

        
        formatPlot(ax)
        # setup_plot_style(ax)
        plt.rc('font', weight = 'bold')
        plt.tight_layout()
        # sleep(1000)

    return anm.FuncAnimation(fig, 
                             animate, 
                             frames = frames, 
                             interval = 20,
                             repeat = False)

if __name__ == '__main__':

    df = pd.read_csv('MigrationWorld/data/migration.csv')
    # print(df.loc[(df['Location']=='China') & (df['Year']==2024)])
    anim = create_animation(df)
    # anim.save('PopulationWorld/output/video.mp4', writer='ffmpeg', fps=18, dpi = 1920/16)
    plt.show()

