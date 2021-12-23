import numpy as np
import pandas as pd

# sklearn will be used to build the model
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# To save the model
import pickle

# For visualization
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
