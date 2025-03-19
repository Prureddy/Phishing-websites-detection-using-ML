# Purpose - Receive the call for testing a page from the Chrome extension and return the result (SAFE/PHISHING)
# for display. This file calls all the different components of the project (The ML model, features_extraction) and
# consolidates the result.

import chardet
import joblib
import features_extraction
import sys
import numpy as np

from features_extraction import LOCALHOST_PATH, DIRECTORY_NAME


def get_prediction_from_url(test_url):
    features_test = features_extraction.main(test_url)
    # Due to updates to scikit-learn, we now need a 2D array as a parameter to the predict function.
    features_test = np.array(features_test).reshape((1, -1))

    clf = joblib.load(LOCALHOST_PATH + DIRECTORY_NAME + '/random_forest_model.pkl')

    pred = clf.predict(features_test)
    return int(pred[0])


def main():
    f = open("data.txt", "r")
    url = f.read().strip()  # Ensure no extra spaces
    f.close()
    

    with open("PhishLinks.txt", "rb") as file:
        raw_data = file.read()
        detected_encoding = chardet.detect(raw_data)['encoding']
        url_phish_list = raw_data.decode(detected_encoding).splitlines()

    print("URL being checked:", url)  # Debug
    print("Loaded phishing URLs:", url_phish_list[:5], "...")  # Print first 5 entries for debugging

    try:
        prediction = get_prediction_from_url(url)
        print("ML Prediction:", prediction)  # Debug
    except Exception as e:
        print(f"Error in prediction: {e}")
        prediction = 1

    if url in url_phish_list:
        print(f"{url} is in the phishing list")  # Debug
        prediction = -1

    if prediction == 1:
        print("SAFE")
    elif prediction == -1:
        print("PHISHING")
    else:
        print(f"Unknown prediction result: {prediction}")

    return prediction


# if __name__ == "__main__":
#     main()
