from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA

class Models:
    neural_net = None
    forrest = None
    pca_kmeans = None
    pca_neural_net = None
    pca_nearest_neighbors = None
    prediction = None

    def __init__(self, x_training, y_training, x_testing, y_testing):
        pca = PCA(n_components=2)
        self.x_train = x_training
        self.y_train = y_training
        self.x_test = x_testing
        self.y_test = y_testing
        self.x_train_reduced = pca.fit_transform(self.x_train)
        self.x_test_reduced = pca.fit_transform(self.x_test)

    def train_models(self):
        self.train_forrest_classifier()
        self.train_neural_net()
        self.train_pca_neural_net()
        self.train_pca_nearest_neighbors()
        self.train_pca_kmeans()

    def train_forrest_classifier(self):
        rf = RandomForestClassifier(n_estimators=100, criterion='entropy', random_state=0)
        rf.fit(self.x_train, self.y_train)
        self.forrest = rf

    def train_neural_net(self):
        clf = MLPClassifier(max_iter=1000, solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
        clf.fit(self.x_train, self.y_train)
        self.neural_net = clf

    def train_pca_neural_net(self):
        cnn = MLPClassifier(max_iter=1000, solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
        cnn.fit(self.x_train, self.y_train)
        self.pca_neural_net = cnn

    def train_pca_kmeans(self):
        kmeans = KMeans(n_clusters=2, random_state=42)
        kmeans.fit(self.x_train, self.y_train)
        self.pca_kmeans = kmeans

    def train_pca_nearest_neighbors(self):
        nearest_neighbors = KNeighborsClassifier(n_neighbors=15)
        nearest_neighbors.fit(self.x_train, self.y_train)
        self.pca_nearest_neighbors = nearest_neighbors

    def predict_results(self, model):
        y_prediction = model.predict(self.x_test)
        self.prediction = accuracy_score(self.y_test, y_prediction)
