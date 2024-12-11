import numpy as np
import matplotlib.pyplot as plt

def plotForestData(forest_data, x_label, y_label, vline_x = None, hline_y = None, line_name = None):
    forest_amount = len(forest_data)
    for i in range(forest_amount):
        plt.plot(range(len(forest_data[i])), forest_data[i])
    
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    
    if vline_x != None:
        if (type(vline_x) == list):
            for i in range(len(vline_x)):
                plt.axvline(vline_x[i], linestyle="dashed")
        else:
            plt.axvline(vline_x, linestyle="dashed")
    
    if hline_y != None:
        if (type(hline_y) == list):
            for i in range(len(hline_y)):
                plt.axvline(hline_y[i], linestyle="dashed")
        else:
            plt.axvline(hline_y, linestyle="dashed")
    if (line_name != None):
        line_name_list = [line_name] if (type(line_name) != list) else line_name
        if (forest_amount > 1):
            plt.legend(["Forest " + str(i) for i in range(forest_amount)] + line_name_list)
    else:
        if (forest_amount > 1):
            plt.legend(["Forest " + str(i) for i in range(forest_amount)])
    plt.show()
    
    
def plotPhaseDiagram(phase_diagram):
    plt.matshow(phase_diagram)
    plt.colorbar()

