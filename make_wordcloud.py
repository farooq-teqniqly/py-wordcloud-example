"""
Generate Word Cloud from JSON Files

This script reads multiple JSON files containing documents and generates a word cloud visualization.
Stop words are filtered out using an additional set of custom stop words.

The script requires the 'argparse', 'json', 'os', 'matplotlib', 'requests', and 'wordcloud' modules.

Example usage:
    python word_cloud_generator.py --input-dir /path/to/json/files

"""
import argparse
import json
import os

import matplotlib.pyplot as plt
import requests
from wordcloud import WordCloud


def load_documents_from_json(file_path):
    """Load documents from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list: List of loaded documents.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def download_stop_words(url):
    """Download stop words from a given URL.

    Args:
        url (str): URL to download the stop words file from.

    Returns:
        set: Set of stop words.
    """
    response = requests.get(url, timeout=30)
    return set(response.text.splitlines())


def add_stop_words(stop_words_set: set):
    """Add additional stop words to the existing set.

    Args:
        stop_words_set (set): Existing set of stop words.

    Returns:
        set: Updated set of stop words with additional words added.
    """
    additional_stop_words = {
        "learn", "microsoft", "session", "app", "Azure", "join", "using", "including",
        "application", "please", "rsvp", "build"
    }
    return stop_words_set.union(additional_stop_words)


def main(input_directory):
    """Main function to generate the word cloud from JSON files.

    Args:
        input_directory (str): Path to the folder containing the JSON files.
    """
    documents = []

    for file_name in os.listdir(input_directory):
        if file_name.endswith(".json"):
            file_path = os.path.join(input_directory, file_name)
            loaded_documents = load_documents_from_json(file_path)
            documents.extend(loaded_documents)

    text = " ".join(documents)

    stop_words = download_stop_words(
        "https://gist.githubusercontent.com/larsyencken/1440509/raw/53273c6c202b35ef00194d06751d8ef630e53df2/"
        "stopwords.txt")

    stop_words = add_stop_words(stop_words)
    wordcloud = WordCloud(stopwords=stop_words).generate(text)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Word Cloud diagram from JSON files.")
    parser.add_argument("--input-dir", required=True, help="Path to the folder containing the JSON files.")

    args = parser.parse_args()
    main(args.input_dir)
