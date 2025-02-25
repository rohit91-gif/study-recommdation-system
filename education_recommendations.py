# -*- coding: utf-8 -*-
"""education Recommendations.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RFFxFL0QsaXSFTn1ibAfAAMyhbJhowdO

```Import Required Libraries
"""

!pip install scikit-surprise

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from surprise import SVD, Dataset, Reader
from surprise.model_selection import cross_validate

"""# load dataset"""

df1 = pd.read_csv("/content/sample_data/student-scores.csv")
df = df1.copy()
df.head()

"""# drop irrelevant columns
#
"""

df.columns

df.columns
df.drop(columns=['id','first_name','last_name','email'],axis=1, inplace=True)

"""# create new features from all score"""

df["total_score"] = df["math_score"] + df["history_score"] + df["physics_score"] + df["chemistry_score"] + df["biology_score"] + df["english_score"] + df["geography_score"]
df["average_score"] = df["total_score"] / 7
df.head()

df.head()

# Step: Create Segment Dataframes
# Split the data into segments based on user segmentation
segments = {}
for segment in user_profiles['segment'].unique():
    # Use the index directly as user_ids instead of relying on a 'userId' column
    user_ids = user_profiles[user_profiles['segment'] == segment].index
    segments[f"segment_{segment}"] = df.loc[user_ids]  # Use .loc to select rows by index

from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate

# Assuming 'df' contains your student data
# Replace 'student_id_column', 'course_id_column', and 'score_column'
# with the actual names of your columns
course_id_column = 'total_score'  # Example: Replace with a column representing courses
score_column = 'average_score'  # Example: Replace with a column representing student scores


reader = Reader(rating_scale=(0.5, 5.0))
for segment, data in segments.items():
    print(f"\nRecommender System for {segment}:")

    # Use the index of the 'data' DataFrame as user IDs
    data_subset = pd.DataFrame({
        'userId': data.index,  # Changed to data.index
        'movieId': data[course_id_column],
        'rating': data[score_column]
    })

    surprise_data = Dataset.load_from_df(data_subset, reader)

    # Train an SVD model
    model = SVD()
    cross_validate(model, surprise_data, cv=3, verbose=True)

"""# Encoding Categorical Columns"""

# from sklearn.preprocessing import LabelEncoder

# # Create a LabelEncoder object
# label_encoder = LabelEncoder()

# # Encode categorical columns using label encoder
# df['gender'] = label_encoder.fit_transform(df['gender'])
# df['part_time_job'] = label_encoder.fit_transform(df['part_time_job'])
# df['extracurricular_activities'] = label_encoder.fit_transform(df['extracurricular_activities'])
# df['career_aspiration'] = label_encoder.fit_transform(df['career_aspiration'])
# Define mapping dictionaries for categorical features
gender_map = {'male': 0, 'female': 1}
part_time_job_map = {False: 0, True: 1}
extracurricular_activities_map = {False: 0, True: 1}
career_aspiration_map = {
        'Lawyer': 0, 'Doctor': 1, 'Government Officer': 2, 'Artist': 3, 'Unknown': 4,
        'Software Engineer': 5, 'Teacher': 6, 'Business Owner': 7, 'Scientist': 8,
        'Banker': 9, 'Writer': 10, 'Accountant': 11, 'Designer': 12,
        'Construction Engineer': 13, 'Game Developer': 14, 'Stock Investor': 15,
        'Real Estate Developer': 16
    }
# Apply mapping to the DataFrame
df['gender'] = df['gender'].map(gender_map)
df['part_time_job'] = df['part_time_job'].map(part_time_job_map)
df['extracurricular_activities'] = df['extracurricular_activities'].map(extracurricular_activities_map)
df['career_aspiration'] = df['career_aspiration'].map(career_aspiration_map)

df.head()

"""# Balance Dataset"""

df['career_aspiration'].unique()

df['career_aspiration'].value_counts()

from imblearn.over_sampling import SMOTE

# Create SMOTE object
smote = SMOTE(random_state=42)

# Separate features and target variable
X = df.drop('career_aspiration', axis=1)
y = df['career_aspiration']

# Apply SMOTE to the data
X_resampled, y_resampled = smote.fit_resample(X, y)

"""# Train test Split"""

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X_resampled,y_resampled,test_size=0.2, random_state=42)

X_train.shape

"""# Feature Scalling"""

from sklearn.preprocessing import StandardScaler

# Initialize the StandardScaler
scaler = StandardScaler()

# Fit the scaler to the training data and transform both training and testing data
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

X_train_scaled.shape

"""# Models Training (Multiple Models)"""

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings("ignore")

# Define models
models = {
    "Logistic Regression": LogisticRegression(),
    "Support Vector Classifier": SVC(),
    "Random Forest Classifier": RandomForestClassifier(),
    "K Nearest Neighbors": KNeighborsClassifier(),
    "Decision Tree Classifier": DecisionTreeClassifier(),
    "Gaussian Naive Bayes": GaussianNB(),
    "AdaBoost Classifier": AdaBoostClassifier(),
    "Gradient Boosting Classifier": GradientBoostingClassifier(),
    "XGBoost Classifier": XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
}

# Train and evaluate each model
for name, model in models.items():
    print("="*50)
    print("Model:", name)
    # Train the model
    model.fit(X_train_scaled, y_train)

    # Predict on test set
    y_pred = model.predict(X_test_scaled)

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)

    # Print metrics
    print("Accuracy:", accuracy)
    print("Classification Report:\n", classification_rep)
    print("Confusion Matrix:\n", conf_matrix)

"""# Model Selection (Random Forest)"""

model = RandomForestClassifier()

model.fit(X_train_scaled, y_train)
# Predict on test set
y_pred = model.predict(X_test_scaled)

# Calculate metrics
print("Accuracy: ",accuracy_score(y_test, y_pred))
print("Report: ",classification_report(y_test, y_pred))
print("Confusion Matrix: ",confusion_matrix(y_test, y_pred))

"""# Single Input Predictions"""

# test 1
print("Actual Label :", y_test.iloc[10])
print("Model Prediction :",model.predict(X_test_scaled[10].reshape(1,-1))[0])
if y_test.iloc[10]==model.predict(X_test_scaled[10].reshape(1,-1)):
    print("Wow! Model doing well.....")
else:
    print("not sure......")

# test 2
print("Actual Label :", y_test.iloc[300])
print("Model Prediction :",model.predict(X_test_scaled[300].reshape(1,-1))[0])
if y_test.iloc[10]==model.predict(X_test_scaled[10].reshape(1,-1)):
    print("Wow! Model doing well.....")
else:
    print("not sure......")

# test 2
print("Actual Label :", y_test.iloc[23])
print("Model Prediction :",model.predict(X_test_scaled[23].reshape(1,-1))[0])
if y_test.iloc[10]==model.predict(X_test_scaled[10].reshape(1,-1)):
    print("Wow! Model doing well.....")
else:
    print("not sure......")

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

# Assuming 'df' contains your user data with relevant features
# You may need to adjust the column selection based on your actual data
user_profiles = df[['gender', 'part_time_job', 'extracurricular_activities',
                    'weekly_self_study_hours', 'total_score', 'average_score']]

# Create a LabelEncoder object
label_encoder = LabelEncoder()

# Encode the 'gender' column
user_profiles['gender'] = label_encoder.fit_transform(user_profiles['gender'])

# Now you can proceed with KMeans clustering
kmeans = KMeans(n_clusters=3, random_state=42)
user_profiles['segment'] = kmeans.fit_predict(user_profiles)
print("User Segmentation:\n", user_profiles.head())

# Step: Create Segment Dataframes
# Split the data into segments based on user segmentation
segments = {}
for segment in user_profiles['segment'].unique():
    # Use the index directly as user_ids instead of relying on a 'userId' column
    user_ids = user_profiles[user_profiles['segment'] == segment].index
    segments[f"segment_{segment}"] = df.loc[user_ids]  # Use .loc to select rows by index



"""# Saving & Load Files"""

import os
import pickle

# Create the 'Models' directory if it doesn't exist
os.makedirs("Models", exist_ok=True)

# SAVE FILES
pickle.dump(scaler, open("Models/scaler.pkl", 'wb'))
pickle.dump(model, open("Models/model.pkl", 'wb'))

# Load the scaler, label encoder, and model
scaler = pickle.load(open("Models/scaler.pkl", 'rb'))
model = pickle.load(open("Models/model.pkl", 'rb'))

"""# Recommendation System"""

import pickle
import numpy as np

# Load the scaler, label encoder, model, and class names
scaler = pickle.load(open("Models/scaler.pkl", 'rb'))
model = pickle.load(open("Models/model.pkl", 'rb'))
class_names = ['Lawyer', 'Doctor', 'Government Officer', 'Artist', 'Unknown',
               'Software Engineer', 'Teacher', 'Business Owner', 'Scientist',
               'Banker', 'Writer', 'Accountant', 'Designer',
               'Construction Engineer', 'Game Developer', 'Stock Investor',
               'Real Estate Developer']

def Recommendations(gender, part_time_job, absence_days, extracurricular_activities,
                    weekly_self_study_hours, math_score, history_score, physics_score,
                    chemistry_score, biology_score, english_score, geography_score,
                    total_score,average_score):

    # Encode categorical variables
    gender_encoded = 1 if gender.lower() == 'female' else 0
    part_time_job_encoded = 1 if part_time_job else 0
    extracurricular_activities_encoded = 1 if extracurricular_activities else 0

    # Create feature array
    feature_array = np.array([[gender_encoded, part_time_job_encoded, absence_days, extracurricular_activities_encoded,
                               weekly_self_study_hours, math_score, history_score, physics_score,
                               chemistry_score, biology_score, english_score, geography_score,total_score,average_score]])

    # Scale features
    scaled_features = scaler.transform(feature_array)

    # Predict using the model
    probabilities = model.predict_proba(scaled_features)

    # Get top five predicted classes along with their probabilities
    top_classes_idx = np.argsort(-probabilities[0])[:5]
    top_classes_names_probs = [(class_names[idx], probabilities[0][idx]) for idx in top_classes_idx]

    return top_classes_names_probs

# Example usage 1
final_recommendations = Recommendations(gender='female',
                                        part_time_job=False,
                                        absence_days=2,
                                        extracurricular_activities=False,
                                        weekly_self_study_hours=7,
                                        math_score=65,
                                        history_score=60,
                                        physics_score=97,
                                        chemistry_score=94,
                                        biology_score=71,
                                        english_score=81,
                                        geography_score=66,
                                        total_score=534,
                                        average_score=76.285714)

print("Top recommended studies with probabilities:")
print("="*50)
for class_name, probability in final_recommendations:
    print(f"{class_name} with probability {probability}")



# Example usage 2
final_recommendations = Recommendations(gender='female',
                                        part_time_job=False,
                                        absence_days=2,
                                        extracurricular_activities=False,
                                        weekly_self_study_hours=4,
                                        math_score=87,
                                        history_score=73,
                                        physics_score=98,
                                        chemistry_score=91,
                                        biology_score=79,
                                        english_score=60,
                                        geography_score=77,
                                        total_score=583,
                                        average_score=83.285714)

print("Top recommended studies with probabilities:")
print("="*50)
for class_name, probability in final_recommendations:
    print(f"{class_name} with probability {probability}")

# sklear version in pychar production
import sklearn
print(sklearn.__version__)
# in pycharm env install
# pip install scikit-learn==1.3.2

"""we can identify the result of our student based on the performce and marks"""



