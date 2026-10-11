import nltk

# Download these resources once if they are not already installed.
for resource, package in [
    ('tokenizers/punkt', 'punkt'),
    ('tokenizers/punkt_tab', 'punkt_tab'),
    ('corpora/stopwords', 'stopwords'),
    ('corpora/wordnet', 'wordnet'),
    ('corpora/omw-1.4', 'omw-1.4'),
]:
    try:
        nltk.data.find(resource)
    except LookupError:
        nltk.download(package, quiet=True)

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

text = """A neural network is a computational model inspired by the structure of the human brain. It consists of interconnected processing units called neurons, which are arranged in layers. The input layer receives data, hidden layers transform the data, and the output layer produces a prediction.

During training, a neural network learns by adjusting the weights of connections between neurons. The learning algorithm calculates an error, propagates the error backward through the network, and updates the weights to reduce the error. This process is called backpropagation.

Neural networks can recognize patterns in images, speech, and text. With enough training examples and a suitable architecture, they can solve classification and regression problems. However, a network may overfit the training data, so validation data and regularization are often used to improve generalization."""

# 1. Sentence tokenization
sentences = sent_tokenize(text)

# 2. Word tokenization
words = word_tokenize(text)

# Keep alphabetic words for linguistic preprocessing.
word_tokens = [word for word in words if word.isalpha()]

# 3. Stop-word removal
stop_words = set(stopwords.words('english'))
filtered_words = [word for word in word_tokens
                  if word.lower() not in stop_words]

# 4. Stemming
stemmer = PorterStemmer()
stemmed_words = [stemmer.stem(word.lower()) for word in filtered_words]

# 5. Lemmatization
lemmatizer = WordNetLemmatizer()
lemmatized_words = [lemmatizer.lemmatize(word.lower())
                    for word in filtered_words]

if __name__ == '__main__':
    print('=' * 70)
    print(' NLTK TEXT PROCESSING: NEURAL NETWORK TOPIC')
    print('=' * 70)
    print('\n1. Original text:\n')
    print(text)
    print('\n2. Sentence tokens:')
    for i, sentence in enumerate(sentences, 1):
        print(f'{i}. {sentence}')
    print('\n3. Word tokens:')
    print(words)
    print('\n4. After stop-word removal:')
    print(filtered_words)
    print('\n5. After stemming:')
    print(stemmed_words)
    print('\n6. After lemmatization:')
    print(lemmatized_words)
