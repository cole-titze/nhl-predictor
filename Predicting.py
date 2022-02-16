import csv
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
import Models.models as models

def get_games(file_path: str) -> list:
    games = []
    with open(file_path, 'r') as read_obj:
        csv_reader = list(csv.reader(read_obj))
        for row in csv_reader:
            if row[13] == "False":
                games.append(row)
    return games

def get_independent(games: list) -> list:
    x = []
    for game in games:
        x.append(game[2:12])
    return x

def get_dependent(games: list) -> list:
    y = []
    for game in games:
        y.append(game[12])
    replacements = {"Home": 0, "Away": 1}
    replacer = replacements.get
    y = [replacer(n, n) for n in y]

    return y

def get_info(games: list) -> list:
    info = []
    for game in games:
        info.append(game[0:3])
    return info

def split_data():
    training_games = get_games("Data/PregameStats.csv")
    x_training = get_independent(training_games)
    y_training = get_dependent(training_games)
    # info_training = get_info(training_games)

    # Current Season data
    test_games = get_games("Data/TestingPregameStats.csv")
    x_curr_season = get_independent(test_games)
    y_curr_season = get_dependent(test_games)

    # Standardize all data
    x_training = StandardScaler().fit_transform(x_training)
    x_curr_season = StandardScaler().fit_transform(x_curr_season)

    return x_training, y_training, x_curr_season, y_curr_season


def predict_results(classifier, x, y):
    y_prediction = classifier.predict(x)
    print(accuracy_score(y, y_prediction))

def clean_x(x):
    cleaned_x = []
    for row in x:
        row.pop(-3)
        row.pop(2)
        row.pop(1)

        cleaned_x.append(row)

    return cleaned_x


# Best is 55% with forrest and no data standardization
def train_model():
    x_training_headers = ['win_ratio_5', 'draw_ratio_5', 'loss_ratio_5', 'h2h_w_d_l_ratio', 'current_goals_avg',
                  'current_goals_avg_h_a', 'conceded_goals_avg', 'conceded_goals_avg_h_a', 'goal_average_5',
                  'conceded_average_5']
    x_train, y_train, x_curr_season, y_curr_season = split_data()

    # Look into cleaning data and what is best for each predictor
    # Combine predictions (sensor fusion)

    # Make predictions on original Dimensionality
    forrest_classifier = models.train_forrest_classifier(x_train, y_train)
    predict_results(forrest_classifier, x_curr_season, y_curr_season)
    print("----------------------------------------------")
    neural_net_classifier = models.train_neural_net(x_train, y_train)
    predict_results(neural_net_classifier, x_curr_season, y_curr_season)
    print("----------------------------------------------")
    kmeans = models.train_kmeans(x_train, y_train)
    predict_results(kmeans, x_curr_season, y_curr_season)
    print("----------------------------------------------")

    # Reduce Dimensionality
    pca = PCA(n_components=2)
    x_train_reduced = pca.fit_transform(x_train)
    x_curr_season_reduced = pca.fit_transform(x_curr_season)

    # Predict Reduced Dimensionality
    kmeans = models.train_kmeans(x_train_reduced, y_train)
    predict_results(kmeans, x_curr_season_reduced, y_curr_season)

train_model()
