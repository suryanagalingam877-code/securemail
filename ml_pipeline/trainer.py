from dataset_loader import load_dataset
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

print("Loading dataset...")
data = load_dataset()

# FAST TRAINING SAMPLE (remove later if desired)
data = data.sample(60000, random_state=42)

X = data["text"].astype(str)
y = data["label"]

print("Splitting dataset...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Vectorizing text...")

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=12000,
    ngram_range=(1,1),
    min_df=5,
    max_df=0.9
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print("Training model...")

model = LogisticRegression(
    solver="saga",
    max_iter=300,
    n_jobs=-1,
    verbose=1
)

model.fit(X_train_vec, y_train)

print("\nEvaluating model...\n")

y_pred = model.predict(X_test_vec)

print(classification_report(y_test, y_pred))

joblib.dump(model, "ml_pipeline/model.pkl")
joblib.dump(vectorizer, "ml_pipeline/vectorizer.pkl")

print("\n✅ Model saved successfully")