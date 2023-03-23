import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from core.helpfunctions import rgb_to_string, unit_to_string
from matplotlib.ticker import MaxNLocator

def histogram(data, mi=None, ma=None, nb_bins=10, xlabel='', ylabel='Count', cumulative=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    bins = np.linspace(mi, ma, nb_bins)
    labels = ['{0:.{1}f}'.format(b, 2) for b in bins]
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xticks(bins)
    ax.set_xticklabels(labels)
    ax.set_xlabel(xlabel , fontsize = 16)
    ax.set_ylabel(ylabel , fontsize = 16)
    ax.hist(data, bins, alpha=0.65, rwidth=0.8, cumulative=cumulative)
    plt.tight_layout()
    fig.show()
    
def multi_histogram(data, colors=None, legend_labels=None, mi=None, ma=None, nb_bins=10, xlabel='', ylabel='Count', cumulative=False, stacked=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    nb_data = len(data)
    bins = np.linspace(mi, ma, nb_bins)
    labels = ['{0:.{1}f}'.format(b, 2) for b in bins]
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xticks(bins)
    ax.set_xticklabels(labels)
    ax.set_xlabel(xlabel , fontsize = 16)
    ax.set_ylabel(ylabel, fontsize = 16)
    if colors is None:
        cmap = mpl.cm.get_cmap('Spectral')
        colors = [rgb_to_string(cmap(cvalue)) for cvalue in np.linspace(0, 1, nb_data)]
    ax.hist(data, bins, color=colors, alpha=0.65, stacked=stacked, rwidth=0.8, cumulative=cumulative)
    if legend_labels is not None: ax.legend(legend_labels)
    plt.tight_layout()
    fig.show()
    
def bar(data, labels, ylabel='Count', integer_y=True, show_zeros=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_ylabel(ylabel, fontsize = 16)
    if show_zeros: index = np.arange(len(data), dtype=np.int64)
    else: index = data != 0
    data = data[index]
    labels = labels[index]
    ax.bar(np.arange(len(data)), data)
    ax.set_xticks(np.arange(len(data)))
    ax.set_xticklabels(labels)
    ax.set_xlim(-1, len(data))
    if integer_y: ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    plt.tight_layout()
    fig.show()
    
def multi_bar(data, labels, colors, ylabel='Count', integer_y=True, show_zeros=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_ylabel(ylabel, fontsize = 16)
    nb_bars = np.nonzero(data)[0].size
    nb_plotted = 0
    for i, (segname, color) in enumerate(colors.items()):
        data_row = data[i]
        if show_zeros: index = np.arange(len(data_row), dtype=np.int64)
        else: index = data_row != 0
        data_row = data_row[index]
        bar = ax.bar(np.arange(nb_plotted, nb_plotted + len(data_row)), data_row, color=color)
        bar.set_label(segname)
        nb_plotted += len(data_row)
    ax.set_xticks(np.arange(nb_bars))
    ax.set_xticklabels(labels[np.nonzero(data)])
    ax.set_xlim(-1, nb_bars)
    ax.legend()
    if integer_y: ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    plt.tight_layout()
    fig.show()
    
def timeseries(data, frame_time=None, frame_unit=None, xlabel='Frames', ylabel='Count'):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xlabel(xlabel , fontsize = 16)
    ax.set_ylabel(ylabel , fontsize = 16)
    ax.plot(range(len(data)), data)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if frame_unit is not None:
        xticks = np.array(ax.get_xticks())
        min_xtick = xticks[xticks>0][0]
        unit = unit_to_string(min_xtick*frame_time, frame_unit, only_unit=True)
        if xlabel == 'Frames': ax.set_xlabel('Time [{}]'.format(unit) , fontsize = 16)
        xticks = [str(int(tick*frame_time)) if int(tick*frame_time)<1000 else str(np.round(tick*frame_time/1000, 1)) for tick in xticks]
        ax.set_xticklabels(xticks)
    plt.tight_layout()
    fig.show()
    
def multi_timeseries(data, colors=None, legend_labels=None, frame_time=None, frame_unit=None, xlabel='Frames', ylabel='Count'):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    data = np.array(list(data))
    nb_lines, nb_points = data.shape
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xlabel(xlabel , fontsize = 16)
    ax.set_ylabel(ylabel , fontsize = 16)
    ax.set_xlim(-1, nb_points)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if frame_unit is not None:
        xticks = np.array(ax.get_xticks())
        min_xtick = xticks[xticks>0][0]
        unit = unit_to_string(min_xtick*frame_time, frame_unit, only_unit=True)
        if xlabel == 'Frames': ax.set_xlabel('Time [{}]'.format(unit) , fontsize = 16)
        xticks = [str(int(tick*frame_time)) if int(tick*frame_time)<1000 else str(np.round(tick*frame_time/1000, 1)) for tick in xticks]
        ax.set_xticklabels(xticks)
    if colors is None:
        cmap = mpl.cm.get_cmap('Spectral')
        colors = [rgb_to_string(cmap(cvalue)) for cvalue in np.linspace(0, 1, nb_lines)]
    for i in range(nb_lines):
        if legend_labels is None: ax.plot(range(nb_points), data[i], color=colors[i], alpha=0.65)
        else: ax.plot(range(nb_points), data[i], color=colors[i], label=legend_labels[i], alpha=0.65)
    if legend_labels is not None: ax.legend()
    plt.tight_layout()
    fig.show()
    
def boolean_scatter(ts, scatter_size=0.5, frame_time=None, frame_unit=None, xlabel='Frames'):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ts = np.array(ts)
    ax.set_xlabel(xlabel , fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.scatter(np.arange(ts.size, dtype=np.int64), ts, s=scatter_size)
    ax.set_title('Joint Occupancy: '+str(np.round(ts.mean()*100,1)))
    ax.set_xlim(-1, ts.size)
    ax.set_yticks([-0.5,0.01,1.01,1.5])
    ax.set_yticklabels(['', 'false', 'true', ''])
    ax.tick_params(axis='y', which='both', bottom=False, top=False, labelbottom=False, length=0.0, width=0.0) 
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if frame_unit is not None:
        xticks = np.array(ax.get_xticks())
        min_xtick = xticks[xticks>0][0]
        unit = unit_to_string(min_xtick*frame_time, frame_unit, only_unit=True)
        if xlabel == 'Frames': ax.set_xlabel('Time [{}]'.format(unit) , fontsize = 16)
        xticks = [str(int(tick*frame_time)) if int(tick*frame_time)<1000 else str(np.round(tick*frame_time/1000, 1)) for tick in xticks]
        ax.set_xticklabels(xticks)
    plt.tight_layout()
    fig.show()
    
def heatmap(data, xresidues, yresidues, title):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel('residues', fontsize = 16)
    ax.set_ylabel('residues', fontsize = 16)
    im = ax.imshow(data, cmap='plasma')
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('Occupancy', rotation=-90, va="bottom")
    ax.set_xticks(np.arange(len(xresidues)))
    ax.set_yticks(np.arange(len(yresidues)))
    ax.set_xticklabels(xresidues)
    ax.set_yticklabels(yresidues)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    ax.set_title(title)
    plt.tight_layout()
    fig.show()