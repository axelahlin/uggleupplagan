import torch, pandas as pd
from transformers import AutoModel
from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer
import numpy as np
import json
import pickle
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.dummy import DummyClassifier
from sklearn.metrics import classification_report


# The JSON module doesn't play very nicely with numpy :(
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def plot_confusion_matrix(y_preds, y_true, labels, title):
    cm = confusion_matrix(y_true, y_preds, normalize="true")
    fig, ax = plt.subplots(figsize=(6, 6))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap="Blues", values_format=".2f", ax=ax, colorbar=False)
    plt.title(title)
    plt.show()


def run(config):
    INPUT_FILE = config["classifier"]["input_file"]
    OUTPUT_LOCATIONS_FILE = config["classifier"]["output_file_locations"]
    OUTPUT_NONLOCATIONS_FILE = config["classifier"]["output_file_nonlocations"]
    model_pickle_file = config["classifier"]["model_pickle_file"]
    classifier_data = config["classifier"]["classifier_data"]
    pickle_model = config["classifier"]["pickle_model"]
    debug = config["debug"]

    df = pd.read_csv(classifier_data)
    train_validation_test = Dataset.from_pandas(df).train_test_split(test_size=0.2)
    data = DatasetDict(
        {
          "train": train_validation_test["train"], 
          "test": train_validation_test["test"]
        }
    )

    # Uncomment this for validation set as well
    valid = data["train"].train_test_split(test_size=0.1)
    data = DatasetDict(
        {
            "train": valid["train"],
            "validation": valid["test"],
            "test": train_validation_test["test"],
        }
    )

    # function for tokenizing the whole corpus
    def tokenize(batch):
        return tokenizer(batch["text"], padding=True, truncation=True)

    # function for extracting all hidden states
    def extract_hidden_states(batch):
        # Place model inputs on the GPU
        inputs = {
            k: v.to(device)
            for k, v in batch.items()
            if k in tokenizer.model_input_names
        }
        # Extract last hidden states
        with torch.no_grad():
            last_hidden_state = model(**inputs).last_hidden_state
        # Return vector for [CLS] token
        return {"hidden_state": last_hidden_state[:, 0].cpu().numpy()}

    model_ckpt = "KB/bert-base-swedish-cased"
    tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
    data_encoded = data.map(tokenize, batched=True, batch_size=None)
    print(data_encoded["train"].column_names)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = AutoModel.from_pretrained(model_ckpt).to(device)

    data_encoded.set_format("torch", columns=["input_ids", "attention_mask"])
    data_hidden = data_encoded.map(extract_hidden_states, batched=True)
    print(data_hidden["train"].column_names)

    # Creating a feature matrix (REMEMBER TO CHANGE back valid and test)
    X_train = np.array(data_hidden["train"]["hidden_state"])
    X_test = np.array(data_hidden["validation"]["hidden_state"])
    y_train = np.array(data_hidden["train"]["is_loc"])
    y_test = np.array(data_hidden["validation"]["is_loc"])
    X_valid = np.array(data_hidden["test"]["hidden_state"])
    y_valid = np.array(data_hidden["test"]["is_loc"])

    if debug:
      print(X_train.shape, X_valid.shape)

    # training classifier
    lr_clf = LogisticRegression(max_iter=3000)
    lr_clf.fit(X_train, y_train)
    if debug:
      print(lr_clf.score(X_test, y_test))

    def predict_loc(s):
        input_sentence = s
        encoded_input = tokenizer(
            input_sentence, padding=True, truncation=True, return_tensors="pt"
        )

        # Extract the hidden states for the input sentence
        with torch.no_grad():
            last_hidden_state = model(
                encoded_input["input_ids"].to(device),
                encoded_input["attention_mask"].to(device),
            ).last_hidden_state
        input_hidden_state = last_hidden_state[:, 0].cpu().numpy()

        # Reshape input_hidden_state to have shape (1, hidden_size)
        input_hidden_state = input_hidden_state.reshape(1, -1)

        # Use the logistic regression model to predict the label
        predicted_label = lr_clf.predict(input_hidden_state)
        return predicted_label[0].flat[0]

    # Use cross-validation to evaluate the performance of the model
    scores = cross_val_score(lr_clf, X_valid, y_valid, cv=20)
    print("Accuracy after cv:", scores.mean())

    # define baseline
    dummy_clf = DummyClassifier(random_state=42)
    dummy_clf.fit(X_train, y_train)
    print("Baseline: ", dummy_clf.score(X_test, y_test))

    if pickle_model:
        pickle.dump(model, open(model_pickle_file, "wb"))





    n = 0
    results_locs = []
    results_nonlocs = []

    with open(INPUT_FILE, "r", encoding="utf8") as i:
        data = json.load(i)

    for entry in data:
        text = entry["text"]
        qid = None
        loc = predict_loc(text)

        if loc:
            new_entry = {
                         "text": text, 
                         "is_loc": loc, 
                         "qid": qid,
                         "latitude": None,
                         "longitude": None
                        }
            results_locs.append(new_entry)
        else:
            new_entry = {
                         "text": text, 
                         "is_loc": loc, 
                         "qid": qid, 
                         "latitude": None,
                         "longitude": None
                        }
            results_nonlocs.append(new_entry)

        n += 1
        if n % 100 == 0:
            print("iteration: " + str(n))

    with open(OUTPUT_LOCATIONS_FILE, "w", encoding="utf8") as o:
        json.dump(results_locs, o, ensure_ascii=False, cls=NpEncoder)

    with open(OUTPUT_NONLOCATIONS_FILE, "w", encoding="utf8") as o:
        json.dump(results_nonlocs, o, ensure_ascii=False, cls=NpEncoder)


def evaluate(config):
    return "" # not implemented
    y_preds = lr_clf.predict(X_test)
    plot_confusion_matrix(
        y_preds,
        y_test,
        ["Location", "Not location"],
        "Normalized confusion matrix for the split test set",
    )

    # Generate the classification report
    # target_names = data.target_names
    report = classification_report(y_test, y_preds)
    print(report)
