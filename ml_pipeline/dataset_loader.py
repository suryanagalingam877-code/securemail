import pandas as pd
import glob

def load_dataset():

    files = glob.glob("data/*")
    all_frames = []

    for file in files:
        print(f"Loading: {file}")

        try:
            df = pd.read_csv(
                file,
                encoding="utf-8",
                on_bad_lines="skip",
                engine="python"
            )
        except:
            try:
                df = pd.read_csv(
                    file,
                    encoding="latin-1",
                    on_bad_lines="skip",
                    engine="python"
                )
            except Exception as e:
                print(f"Skipping {file}: {e}")
                continue

        df.columns = [c.lower().strip() for c in df.columns]

        text_cols = ["text","email","content","body","message"]
        label_cols = ["label","class","target","phishing"]

        text_col = next((c for c in df.columns if c in text_cols), None)
        label_col = next((c for c in df.columns if c in label_cols), None)

        if text_col and label_col:
            df = df[[text_col,label_col]].rename(
                columns={text_col:"text", label_col:"label"}
            )
            all_frames.append(df)

    data = pd.concat(all_frames, ignore_index=True)
    data.dropna(inplace=True)

    # -----------------------------
    # LABEL NORMALIZATION
    # -----------------------------
    data["label"] = data["label"].astype(str).str.lower().str.strip()

    phishing_words = [
        "phishing","spam","malicious","1","true","yes"
    ]

    safe_words = [
        "ham","legitimate","safe","0","false","no"
    ]

    def normalize_label(x):
        if x in phishing_words:
            return 1
        elif x in safe_words:
            return 0
        else:
            return None

    data["label"] = data["label"].apply(normalize_label)

    data.dropna(inplace=True)
    data["label"] = data["label"].astype(int)

    print("\nDataset Summary:")
    print(data["label"].value_counts())

    return data