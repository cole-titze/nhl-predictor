from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
import Models.models as models
import DataRetrieval.get_prediction_data as data
import Plotting.plotting as plt

x_training_headers = ['win_ratio_5', 'draw_ratio_5', 'loss_ratio_5', 'h2h_w_d_l_ratio', 'current_goals_avg',
                      'current_goals_avg_h_a', 'conceded_goals_avg', 'conceded_goals_avg_h_a', 'goal_average_5',
                      'conceded_average_5']

def predict_results(classifier, x, y):
    y_prediction = classifier.predict(x)
    print(accuracy_score(y, y_prediction))


# Look into cleaning data and what is best for each predictor
# Combine predictions (sensor fusion)
# Best is 55% with forrest and no data standardization
def run_models():
    x_train, y_train, x_curr_season, y_curr_season = data.split_data()

    # Make predictions on original Dimensionality
    print("Forrest Prediction: ")
    forrest_classifier = models.train_forrest_classifier(x_train, y_train)
    predict_results(forrest_classifier, x_curr_season, y_curr_season)
    print("Neural Network Prediction: ")
    neural_net_classifier = models.train_neural_net(x_train, y_train)
    predict_results(neural_net_classifier, x_curr_season, y_curr_season)
    print("K-Means Prediction: ")
    kmeans = models.train_kmeans(x_train, y_train)
    predict_results(kmeans, x_curr_season, y_curr_season)

    # Reduce Dimensionality
    pca = PCA(n_components=2)
    x_train_reduced = pca.fit_transform(x_train)
    x_curr_season_reduced = pca.fit_transform(x_curr_season)

    # Plot lower dimensionality
    plt.plot_reduced_dimensionality(x_curr_season_reduced, y_curr_season)

    # Predict Reduced Dimensionality
    print("PCA K-Means Prediction: ")
    kmeans = models.train_kmeans(x_train_reduced, y_train)
    predict_results(kmeans, x_curr_season_reduced, y_curr_season)
    print("PCA Classifier Prediction: ")

run_models()
