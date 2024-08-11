import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow
import mlflow.sklearn
import joblib

# Veri setini yükle
df = pd.read_csv('new_merged_squat_data.csv')

# Veri ön işleme
unwanted_items = ['Inner', 'Outer','Nose','Shoulder','Ear','Mouth','Pinky ', 'Thumb','Eye']
new_df = df[~df['Landmark Name'].str.contains('|'.join(unwanted_items))]
columns_drop = ['Landmark ID', 'Frame No.']
new_df = new_df.drop(columns=columns_drop)

# Özellik çıkarımı
def extract_features_from_row(row):
    x = row['X']
    y = row['Y']
    z = row['Z']
    return [x, y, z]

X = np.array([extract_features_from_row(row) for _, row in new_df.iterrows()])
y = new_df['Squat Type']

# Train ve test setlerine ayırın
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# MLflow deneyini başlatın
with mlflow.start_run():

    # Random Forest sınıflandırma modelini oluşturun ve eğitin
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Test seti üzerinde modeli değerlendirin
    y_pred = model.predict(X_test)

    # Model performansını kaydedin
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, pos_label='Correct')
    recall = recall_score(y_test, y_pred, pos_label='Correct')
    f1 = f1_score(y_test, y_pred, pos_label='Correct')

    # MLflow'a metrikleri kaydedin
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1", f1)

    # Modeli MLflow ile kaydet
    mlflow.sklearn.log_model(model, "model")

print("Accuracy :", accuracy)
print("precision: ", precision)
print("recall: ", recall)
print("f1_score: ", f1)

# Modeli kaydet
joblib.dump(model, "model.pkl")
