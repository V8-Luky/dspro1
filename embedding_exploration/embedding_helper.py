import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer

nltk.download('punkt')

def process_games_data(source):
    # Read the CSV file
    games = pd.read_csv(source)

    # Select relevant columns
    games = games[['AppID', 'Name', 'About the game', 'Supported languages', 'Genres']]

    # Rename columns
    games.columns = ['id', 'name', 'description', 'languages', 'genres']

    # Drop rows with missing descriptions
    games = games.dropna(subset=['description'])

    # Filter games with English available
    #games['english_available'] = games['languages'].apply(lambda x: 'english' in x.lower())
    #games = games[games['english_available']]
    #Remove not needed columns
    #games = games.drop(columns=['languages', 'english_available'])

    return games


def string_to_sentences(input_string):
    """
    Transforms an English input string into a list of sentences.

    Args:
        input_string (str): The input text in English.

    Returns:
        list: A list of sentences from the input string.
    """
    # Tokenize the input string into sentences
    sentences = sent_tokenize(input_string)
    return sentences
