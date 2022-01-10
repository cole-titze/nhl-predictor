import csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


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
    replacements = {"Home": 0, "Draw": 1, "Away": 2}
    replacer = replacements.get
    y = [replacer(n, n) for n in y]

    return y


def get_info(games: list) -> list:
    info = []
    for game in games:
        info.append(game[0:3])
    return info


def train_model():
    training_games = get_games("Data/PregameStats.csv")
    x_training = get_independent(training_games)
    x_training.extend(x_training)
    y_training = get_dependent(training_games)
    y_training.extend(y_training)
    info_training = get_info(training_games)
    info_training.extend(info_training)

    # Split into training and testing data
    x_train, x_test, y_train, y_test, info_train, info_test = train_test_split(x_training, y_training, info_training,
                                                                               test_size=0.2, stratify=y_training, random_state=21)

    # Feature Scaling
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    # Train Model
    # Fitting Random Forest Classification to the Training set
    rf = RandomForestClassifier(n_estimators=100, criterion='entropy', random_state=42)
    rf.fit(x_train, y_train)

    y_pred_rf = rf.predict(x_test)
    y_pred_rf_prob = rf.predict_proba(x_test)

    print(classification_report(y_test, y_pred_rf))

    # Predict 2020 season
    test_games = get_games("Data/TestingPregameStats.csv")
    x_testing = get_independent(test_games)
    y_testing = get_dependent(test_games)
    info_testing = get_info(test_games)

    #x_test = scaler.transform(x_test)

    # Test with fresh year data
    y_pred_rf = rf.predict(x_testing)

    print(classification_report(y_testing, y_pred_rf))


train_model()
