import sys
import csv
from collections import Counter


def main():
    # Get book filenames and validate them (1 or more)
    filenames = get_book_filenames(sys.argv)

    # Create list of lines aggregated from all files
    lines = []
    for filename in filenames:
        lines.extend(get_lines(filename))

    # Create dictionary and list of invalid words (aggregated)
    dictionary, invalid_words = count_words(lines)

    # Create a single invalid words file and a single CSV with merged results
    create_invalid_word_file(invalid_words, output_stem("merged"))
    create_file(dictionary, output_stem("merged"))


# Normalization helper to unify quotes/dashes and remove invisible chars

def normalize_text(s):
    # Map curly single quotes/apostrophes to straight
    s = s.replace("’", "'").replace("‘", "'")
    # Map curly double quotes to straight
    s = s.replace("“", '"').replace("”", '"')
    # Normalize dashes and ellipsis
    s = s.replace("—", "-").replace("–", "-")
    s = s.replace("…", "...")
    # Remove soft hyphen and zero-width space
    s = s.replace("\u00AD", "").replace("\u200b", "")
    return s


def get_book_filenames(args):
    # Check for correct use of program
    if len(args) < 2:
        sys.exit("Too few command-line arguments. Usage: python project file1.txt [file2.txt ...]")

    filenames = args[1:]

    # Validate all files are .txt
    for filename in filenames:
        if not filename.endswith(".txt"):
            sys.exit(f"Not a text file: {filename}")
    return filenames


# This function creates a list of each line in a book file

def get_lines(f):
    try:
        with open(f, encoding="utf-8") as file:
            # line.strip() returns False on whitespace-only lines, so ignore them
            lines = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        sys.exit(f"File does not exist: {f}")
    return lines


# This function creates a dictionary with the word as key and frequency as value
# It also creates a list of words that were not able to be processed

def count_words(lines):
    words_counter = Counter()
    invalid_words = []
    for line in lines:
        line = normalize_text(line)
        words = line.split(" ")
        for word in words:
            # Clean and normalize word
            word = normalize_text(word).strip("\"'()«»—!?¿¡.-:;,©/… \n\t\r‘’").lower()

            # Split at apostrophe
            words_split_apostrophe = word.replace("’", "'").split("'")
            for w in words_split_apostrophe:
                if w.isalpha():
                    words_counter[w] += 1
                else:
                    if w:  # avoid counting empty strings as invalid
                        invalid_words.append(w)

    # Sort by frequency descending then alphabetically for determinism
    sorted_items = sorted(words_counter.items(), key=lambda item: (-item[1], item[0]))
    sorted_dict = dict(sorted_items)
    return sorted_dict, invalid_words


# Utility to pick an output stem (without extension)

def output_stem(name):
    return name


# This function creates the csv file using the provided stem

def create_file(d, stem):
    with open(stem + ".csv", "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        for row in d.items():
            writer.writerow(row)


# This function creates the text file from the list of invalid words

def create_invalid_word_file(invalid_list, stem):
    with open(stem + "_invalid_words.txt", "w", encoding="utf-8-sig") as f:
        f.write("Invalid words: \n")
        for word in invalid_list:
            if not word.isdigit():
                f.write(word + "\n")


if __name__ == "__main__":
    main()
