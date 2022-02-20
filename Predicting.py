import Models.models as math_models
import DataRetrieval.get_prediction_data as data
import Plotting.plotting as plt
from sklearn.metrics import log_loss
import DataRetrieval.teams as team

x_training_headers = ['home_win_ratio_5', 'home_current_goals_avg', 'home_current_goals_avg',
                      'home_current_goals_avg_h', 'home_conceded_goals_avg', 'home_conceded_goals_avg_h',
                      'home_goal_average_5', 'home_conceded_average_5', 'h2h_w_d_l_ratio', 'away_win_ratio_5',
                      'away_current_goals_avg', 'away_current_goals_avg', 'away_current_goals_avg_h',
                      'away_conceded_goals_avg', 'away_conceded_goals_avg_h', 'away_goal_average_5',
                      'away_conceded_average_5']

def get_models(x_train, y_train, x_test_season, y_test_season):
    models = math_models.Models(x_train, y_train, x_test_season, y_test_season)

    # Train Models
    models.train_models()

    # Make predictions on original Dimensionality
    print("Forrest Prediction: ")
    models.predict_results(models.forrest)
    print(models.prediction)

    print("Neural Network Prediction: ")
    models.predict_results(models.neural_net)
    models.predict_results(models.neural_net)
    print(models.prediction)
    x_test_season_prob = models.neural_net.predict_proba(x_test_season)
    lg_log_loss = log_loss(y_test_season, x_test_season_prob)
    print("Neural Network Log Loss: " + str(lg_log_loss))

    # Plot lower dimensionality
    # plt.plot_reduced_dimensionality(models.x_test_reduced, y_test)

    # Predict Reduced Dimensionality
    print("PCA K-Means Prediction: ")
    models.predict_results(models.pca_kmeans)
    print(models.prediction)

    print("PCA Neural Network Prediction: ")
    models.predict_results(models.pca_neural_net)
    print(models.prediction)

    print("PCA Nearest Neighbors Prediction: ")
    models.predict_results(models.pca_nearest_neighbors)
    print(models.prediction)

    return models

# Look into cleaning data and what is best for each predictor
# Combine predictions (sensor fusion)
# Train with 2021 year and 2022 partial matches, try less years
# Best is 60% with kmeans
def run_models(away_team: str, home_team: str):
    x_train, y_train, x_test_season, y_test_season = data.split_data()

    models = get_models(x_train, y_train, x_test_season, y_test_season)

    # Predict Current Season Games
    x_current_game = data.get_single_game(home_team, away_team)
    x_current_game = [x_current_game]
    print(away_team + "     " + home_team + " Percentage Chance")
    print(models.neural_net.predict_proba(x_current_game))

def main():
    teams = team.Teams()
    run_models(teams.Kraken, teams.Flames)

main()
