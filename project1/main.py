import string
from nltk.tokenize import word_tokenize
def tokenize_text(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        clear_data = data.translate(str.maketrans('', '', string.punctuation + '“”‘’"'))
        tokenized_text = word_tokenize(clear_data)
    return tokenized_text

file_path = 'project1/Middlemarch.txt'
print(tokenize_text(file_path))
