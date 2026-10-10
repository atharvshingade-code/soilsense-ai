import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
from urllib.request import urlopen

URL = (
    "https://raw.githubusercontent.com/"
    "niteshwayakar/Crop-Recommendation/"
    "main/Crop_recommendation.csv"
)

print("Downloading dataset...")

try:
    df = pd.read_csv(URL)
except Exception as e:
    raise SystemExit(
        f"Dataset download failed: {e}\n"
        "Download a compatible Crop_recommendation.csv "
        "dataset manually and place it in this folder."
    )

print("Dataset shape:", df.shape)
print(df.head())

features = [
    "N", "P", "K", "temperature",
    "humidity", "ph", "rainfall"
]

target = "label"

missing = set(features + [target]) - set(df.columns)

if missing:
    raise SystemExit(f"Dataset is missing columns: {missing}")

df = df.dropna(subset=features + [target])

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

with open("crop_model.pkl", "wb") as file:
    pickle.dump(model, file)

with open("model_info.txt", "w") as file:
    file.write(f"Test accuracy: {accuracy:.4f}\n")
    file.write(f"Dataset records: {len(df)}\n")

print(f"Model trained. Test accuracy: {accuracy:.2%}")
print("Saved model to crop_model.pkl")