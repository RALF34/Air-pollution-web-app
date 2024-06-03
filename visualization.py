from typing import List

import streamlit as st
from matplotlib import pyplot


# https://www.who.int/news-room/feature-stories/detail/what-are-the-who-air-quality-guidelines
WHO_RECOMMENDATIONS = {
    pollutant: value for (pollutant, value) in zip(
        ["NO2","SO2","PM2.5","PM10","CO"],
        [25,40,15,45,4]
    )
}

def plot_variation(
    values: List[List[float]],
    pollutant: str,
    station: str) -> pyplot.figure:
    '''
    Generate the graph showing average daily variation (obtained using
    average concentrations recorded at each of the 24 hours of the day, 
    stored in "values") of air concentration of "pollutant" recorded by 
    "station".
    '''
    figure, ax = pyplot.subplots()
    figure.set_size_inches(17,14)
    x = [str(x)+"h00" for x in range(24)]
    highest_value = max(values[0]+values[1])
    ax.set_ylim(0,highest_value)
    colors = ("dodgerblue", "cyan")
    labels = ("Working_days","Week_end")

    def contains_zero(lists: List[List[float]]) -> bool:
        '''
        Return False if zero is not in any of the lists given by the
        "lists" argument, and True, along with the position of the
        list(s) containing zero, otherwise.
        '''
        answer, L = False, []
        for l in lists:
            for e in l:
                if not(e):
                    L.append(l.index(lists))
                    if not(answer):
                        answer = True
        return answer, L
        
    # For both of the lists given by "values", determine whether 
    # each of the 24 hours of the day is associated with an
    # average concentration value different from zero.
    hours_with_no_value, L = contains_zero(values)
    # Plot the data using either a continuous line (if all the 24
    # values are different from zero) or points.
    if not(hours_with_no_value):
        ax.plot(x, values[0], c="dodgerblue", label="Working days")
        ax.plot(x, values[1], c="cyan", label="Week-end")
    elif len(L)==1:
        i = 0 if 1 in L else 1
        ax.plot(x, values[i], c=colors[i], label=labels[i])
        ax.scatter(x, values[L[0]], c=colors[L[0]], label=labels[L[0]])
    else:
        ax.scatter(x, values[0], c="dodgerblue", label="Working days")
        ax.scatter(x, values[1], marker="s", c="cyan", label="Week-end")
    unit = ("m" if pollutant == "CO" else "µ")+"g/m³"
    WHO_value = WHO_RECOMMENDATIONS[pollutant]
    thresholds = [(2*x/3)*WHO_value for x in range(1,4)]
    if ax.get_ylim()[1] > WHO_value:
        ax.plot(
            range(24),
            [WHO_value]*24,
            color="violet",
            ls="--",
            lw=1.7,
            label="Recommended daily \naverage (WHO)")
        ax.legend(loc="upper right")
    else:
        ax.text(
            1,
            1,
            f"Recommended daily average (WHO): {WHO_value} {unit}",
            ha="right",
            va="top")
    # Split the graph into three colored zones.
    colors = ["limegreen","orange","red","magenta"]
    j = 0
    y_min = 0
    while thresholds[j] < highest_value:
        ax.fill_between(
            list(range(24)),
            thresholds[j],
            y2=y_min,
            color=colors[j],
            alpha=0.1)
        y_min = thresholds[j]
        j += 1
    ax.fill_between(
        list(range(24)),
        highest_value,
        y2=y_min,
        color=colors[j],
        alpha=0.1)
    ax.set_ylabel(
        "Air"+" "*14+"\nconcentration"+" "*14+
        "\nof "+pollutant+" "*14+"\n("+ unit +") "*14,
        rotation="horizontal",
        size="large")

    return figure
