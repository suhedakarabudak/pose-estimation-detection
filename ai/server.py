from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from joblib import load
import cv2
import numpy as np
import pandas as pd
import tempfile
import os
from collections import Counter
from mediapipe import solutions as mp_solutions

app = FastAPI()

# Modeli yükle '/home/suhedata/Desktop/ai/model.pkl'
MODEL_PATH = "/home/suhedata/Desktop/ai/model.pkl"

# Modeli global olarak yükle
pose_estimation = None
mp_pose = mp_solutions.pose.Pose()

@app.on_event("startup")
def load_model():
    global pose_estimation
    pose_estimation = PoseEstimation(MODEL_PATH)

class PoseEstimation:
    def __init__(self, model_path):
        self.model = load(model_path)
    
    def landmarks_to_dataframe(self, landmarks):
        landmarks_list = []
        for landmark in landmarks.landmark:
            landmarks_list.append([landmark.x, landmark.y, landmark.z])
        df = pd.DataFrame(landmarks_list, columns=['X', 'Y', 'Z'])
        return df
    
    def preprocess_data(self, df):
        unwanted_items = ['Inner', 'Outer', 'Nose', 'Shoulder', 'Ear', 'Mouth', 'Pinky', 'Thumb', 'Eye']
        df['Landmark Name'] = ['Landmark {}'.format(i) for i in range(len(df))]
        new_df = df[~df['Landmark Name'].str.contains('|'.join(unwanted_items))]
        return new_df

    def extract_features_from_row(self, row):
        x = row['X']
        y = row['Y']
        z = row['Z']
        return [x, y, z]

    def process(self, frame, pose):
        keypoints = pose.process(frame)
        if keypoints.pose_landmarks:
            ps_lm_df = self.landmarks_to_dataframe(keypoints.pose_landmarks)
            preprocessed_data = self.preprocess_data(ps_lm_df)
            X_new = np.array([self.extract_features_from_row(row) for _, row in preprocessed_data.iterrows()])
            predictions = self.model.predict(X_new)
            return predictions.tolist()
        return None

@app.get("/")
async def root():
    return {"message": "AI Fitness Trainer API"}

@app.post("/predict_frame/")
async def predict_frame(file: UploadFile = File(...)):
    try:
        # Geçici bir dosya oluşturun
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            # Video dosyasını geçici dosyaya yazın
            temp_file.write(await file.read())
            temp_file_path = temp_file.name

        # Video dosyasını açın
        video = cv2.VideoCapture(temp_file_path)

        if not video.isOpened():
            raise HTTPException(status_code=400, detail="Could not open the video file")

        predictions_list = []
        while True:
            ret, frame = video.read()
            if not ret:
                break

            # Tahmin işlemi
            predictions = pose_estimation.process(frame, mp_pose)
            if predictions is not None:
                predictions_list.extend(predictions)

        video.release()
        os.remove(temp_file_path)
        
        if not predictions_list:
            return JSONResponse(content={"message": "No predictions available"})

        # Tahminlerin en sık tekrar eden sonucunu bul
        prediction_counts = Counter(predictions_list)
        most_common_prediction, _ = prediction_counts.most_common(1)[0]
        
        return JSONResponse(content={"final_prediction": most_common_prediction})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
