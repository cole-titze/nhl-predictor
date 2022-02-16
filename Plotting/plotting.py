import matplotlib.pyplot as plot

def split_into_win_loss(x_curr_season_reduced, y_curr_season):
    i = 0
    losses_x = []
    losses_y = []
    wins_x = []
    wins_y = []
    for match in x_curr_season_reduced:
        if y_curr_season[i] == 0:
            losses_x.append(match[0])
            losses_y.append(match[1])
        elif y_curr_season[i] == 1:
            wins_x.append(match[0])
            wins_y.append(match[1])
        i += 1

    return wins_x, wins_y, losses_x, losses_y

def plot_reduced_dimensionality(x_curr_season_reduced, y_curr_season):
    wins_x, wins_y, losses_x, losses_y = split_into_win_loss(x_curr_season_reduced, y_curr_season)

    plot.scatter(wins_x, wins_y, c="Blue")
    plot.scatter(losses_x, losses_y, c="Orange")
    plot.show()
