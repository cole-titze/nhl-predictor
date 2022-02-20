from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
import Models.models as models
import DataRetrieval.get_prediction_data as data
import Plotting.plotting as plt
from sklearn.metrics import log_loss

x_training_headers = ['home_win_ratio_5', 'home_current_goals_avg', 'home_current_goals_avg',
                      'home_current_goals_avg_h', 'home_conceded_goals_avg', 'home_conceded_goals_avg_h',
                      'home_goal_average_5', 'home_conceded_average_5', 'h2h_w_d_l_ratio', 'away_win_ratio_5',
                      'away_current_goals_avg', 'away_current_goals_avg', 'away_current_goals_avg_h',
                      'away_conceded_goals_avg', 'away_conceded_goals_avg_h', 'away_goal_average_5',
                      'away_conceded_average_5']

def predict_results(classifier, x, y):
    y_prediction = classifier.predict(x)
    print(accuracy_score(y, y_prediction))

# Look into cleaning data and what is best for each predictor
# Combine predictions (sensor fusion)
# Best is 60% with kmeans
def run_models(away_team: str, home_team: str):
    x_train, y_train, x_test_season, y_test_season = data.split_data()

    # Make predictions on original Dimensionality
    print("Forrest Prediction: ")
    forrest_classifier = models.train_forrest_classifier(x_train, y_train)
    predict_results(forrest_classifier, x_test_season, y_test_season)
    print("Neural Network Prediction: ")
    neural_net_classifier = models.train_neural_net(x_train, y_train)
    predict_results(neural_net_classifier, x_test_season, y_test_season)

    # Reduce Dimensionality
    pca = PCA(n_components=2)
    x_train_reduced = pca.fit_transform(x_train)
    x_test_season_reduced = pca.fit_transform(x_test_season)

    # Plot lower dimensionality
    plt.plot_reduced_dimensionality(x_test_season_reduced, y_test_season)

    # Predict Reduced Dimensionality
    print("PCA K-Means Prediction: ")
    kmeans = models.train_kmeans(x_train_reduced, y_train)
    predict_results(kmeans, x_test_season_reduced, y_test_season)
    x_test_season_prob = neural_net_classifier.predict_proba(x_test_season)
    lg_log_loss = log_loss(y_test_season, x_test_season_prob)
    print("Log Loss: " + str(lg_log_loss))
    print("PCA Neural Network Prediction: ")
    net = models.train_neural_net(x_train_reduced, y_train)
    predict_results(net, x_test_season_reduced, y_test_season)

    # Predict Current Season Games
    x_current_game = data.get_single_game(home_team, away_team)
    x_current_game = [x_current_game]
    print(neural_net_classifier.predict_proba(x_current_game))

run_models("Seattle Kraken", "Calgary Flames")
