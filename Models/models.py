from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPClassifier

def train_forrest_classifier(x, y):
    # Train Model: Fitting Random Forest Classification to the Training set
    rf = RandomForestClassifier(n_estimators=100, criterion='entropy', random_state=42)
    rf.fit(x, y)

    return rf


def train_neural_net(x, y):
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    clf.fit(x, y)
    return clf


def train_kmeans(x, y):
    kmeans = KMeans(n_clusters=2, random_state=0).fit(x, y)
    return kmeans