import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def main(profile, self, ylabel, xlabel, legend):
    """
    Plots the data from the .csv file
    """
    #
    figure = plt.Figure(figsize=(12, 2), dpi=100)
    ax1 = figure.add_subplot(211,zorder=2)
    ax2 = figure.add_subplot(212,zorder=1)

    ###### Top axis
    ax1.plot(profile[0], profile[1])
    ax1.margins(x=0, y=0)
    # Remove top and right spines
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    #Add legend
    ax1.legend([legend])
    ax1.set_xticks(ax1.get_xticks()[1:])

    # Add x-axis and y-axis labels
    ax1.set_xlabel(xlabel,x=1.0, ha='right')
    ax1.set_ylabel(ylabel)
    ax1.set_ylim(0, max(profile[1])+10)

    ###### Bottom axis
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.margins(x=0, y=0)
    ax2.set_ylim(-100,0)
    ax2.set_xlim(min(profile[0]),max(profile[0]))
    ax2.set_xticklabels([])
    ax2.set_xticks([])
    ax2.set_ylabel("Depth (Km)")

    figure.subplots_adjust(hspace=0)

    #Add hover annotations to the second subplot using mpl_connect
    annotation = None

    def on_motion(event):
        nonlocal annotation
        if event.inaxes == ax2:
            if annotation:
                annotation.remove()
            annotation = ax2.annotate(f'({event.xdata:.2f}, {event.ydata:.2f})',
                                      xy=(event.xdata, event.ydata),
                                      xytext=(10, -10),
                                      textcoords='offset points',
                                      bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white")
                                      )
            figure.canvas.draw_idle()
        elif annotation:
            annotation.remove()
            annotation = None  # Reset annotation
            figure.canvas.draw_idle()
    
    figure.canvas.mpl_connect('motion_notify_event', on_motion)
    
    canvas = FigureCanvasTkAgg(figure, self.canvas)
    canvas.draw()
    canvas_height = int(self.canvas.winfo_height())
    canvas.get_tk_widget().place(x=0, y=0, relwidth=1, relheight=canvas_height / self.canvas.winfo_height())

    return canvas