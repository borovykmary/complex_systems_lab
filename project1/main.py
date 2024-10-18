import string
import os
from nltk.tokenize import word_tokenize
from collections import Counter
import matplotlib.pyplot as plt
def tokenize_text(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        clear_data = data.translate(str.maketrans('', '', string.punctuation + '“”‘’"')).lower()
        tokenized_text = word_tokenize(clear_data)
    return tokenized_text

def count_frequencies(book_path):  # returns a dictionary with words as keys and their frequencies as values
    tokenized_text = tokenize_text(book_path)
    total = sum(1 for word in tokenized_text)
    dictionary = Counter(tokenized_text)
    frequencies = {word: count / total for word, count in dictionary.items()}
    sorted_dict = dict(sorted(frequencies.items(), key=lambda item: item[1], reverse=True))
    return sorted_dict, dictionary, total

def count_ranks(book_path):  # returns a dictionary with words as keys and their ranks as values
    frequencies, dictionary, total = count_frequencies(book_path)
    sorted_frequencies = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)
    ranks = {}
    for rank, (word, frequency) in enumerate(sorted_frequencies, start=1):
        ranks[word] = rank
    return ranks, dictionary, total

def save_analysis_to_file(book_path, ranks, dictionary, total, output_dir='output'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    book_title = os.path.basename(book_path).replace('.txt', '')
    file_name = f"{book_title}_{total}_words_analysis.txt"
    file_path = os.path.join(output_dir, file_name)

    with open(file_path, 'w') as file:
        file.write("Rank\tWord\tCount\tFrequency\n")
        for word, rank in ranks.items():
            count = dictionary[word]
            frequency = count / total
            file.write(f"{rank}\t{word}\t{count}\t{frequency:.6f}\n")

def plot_graph(book_paths, scale):
    plt.figure(figsize=(12, 6))
    plt.style.use('seaborn-v0_8-deep')
    colors = ['r', 'g', 'b', 'm']

    for i, book_path in enumerate(book_paths):
        frequencies, dictionary, total = count_frequencies(book_path)
        ranks, _, _ = count_ranks(book_path)

        sorted_frequencies = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)
        sorted_ranks = sorted(ranks.items(), key=lambda item: item[1])

        freq_values = [freq for word, freq in sorted_frequencies]
        rank_values = [rank for word, rank in sorted_ranks]

        book_title = os.path.basename(book_path).replace('.txt', '')

        if scale == 'log-log':
            plt.loglog(rank_values, freq_values, marker='o', markersize=1, linestyle='-', color=colors[i % len(colors)],
                       label=f'Empirical for {book_title}')
            C = freq_values[0]  # constant for Zipf's Law
            zipf_values = [C / (rank) for rank in rank_values]
            plt.loglog(rank_values, zipf_values, linestyle='--', color=colors[i % len(colors)],
                       label=f'Theoretical Zipf for {book_title}')
        elif scale == 'linear':
            plt.plot(rank_values, freq_values, marker='o', markersize=1, linestyle='-', color=colors[i % len(colors)],
                     label=f'Empirical for {book_title}')
            C = freq_values[0]
            zipf_values = [C / (rank) for rank in rank_values]
            plt.plot(rank_values, zipf_values, linestyle='--', color=colors[i % len(colors)],
                     label=f'Theoretical Zipf for {book_title}')

    if scale == 'log-log':
        plt.ylim(0.000001, 0.1)
    elif scale == 'linear':
        plt.ylim(0, 0.05)
        plt.xlim(0, 5000)

    plt.xlabel('Rank', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.title(f'Rank-Frequency Plot with Zipf\'s Law ({scale.capitalize()} Scale)', fontsize=16)
    plt.legend(loc='best', fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()

book_paths = ['project1/Middlemarch.txt', 'project1/The-Adventures-of-Roderick-Random.txt', 'project1/The-Castle-of-Otranto.txt','project1/Ulysses.txt']
""" for book_path in book_paths:
    ranks, dictionary, total = count_ranks(book_path)
    save_analysis_to_file(book_path, ranks, dictionary, total)"""

plot_graph(book_paths, scale='log-log')
plot_graph(book_paths, scale='linear')


