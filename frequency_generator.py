import sys
import csv


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


def main():

    # Get book filename and validate it
    filename = get_book_filename(sys.argv)

    # Create list of lines
    lines = get_lines(filename)

    # Create dictionary and list of invalid words
    dictionary, invalid_words = count_words(lines)

    create_invalid_word_file(invalid_words, filename)

    create_file(dictionary, filename)


def get_book_filename(args):
    # Check for correct use of program
    if len(args) < 2:
        sys.exit("Too few command-line arguments. Usage: python project bookname.txt")
    elif len(args) > 2:
        sys.exit("Too many command-line arguments. Usage: python project bookname.txt")

    filename = args[1]
    # Check that book file is correct file type
    if not filename.endswith(".txt"):
        sys.exit("The book not text file")
    return filename


# This function creates a list of each line in the book file


def get_lines(f):
    try:
        with open(f) as file:
            # line.strip() return False on whitespace characters so will ignore
            # lines with only whitespace
            lines = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        sys.exit("File does not exist")
    return lines

# This function creates a dictionary with the word as key and frequency as value
# It also creates a list of words that were not able to be processed


def count_words(lines):
    wordsdic = {}
    invalid_words = []
    for line in lines:
        line = normalize_text(line)
        words = line.split(" ")
        for word in words:
            # Found some weird invisible characters in the middle of some words removed with replace("­", "")
            word = normalize_text(word).strip("\"'()«»—!?¿¡.-:;,©/… \n\t\r‘’").lower()
            
            # Split at apostrophe
            
            words_split_apostrophe = word.replace("’", "'").split("'")
            for word_split_apostrophe in words_split_apostrophe:
                if word_split_apostrophe.isalpha():
                    wordsdic[word_split_apostrophe] = wordsdic.get(word_split_apostrophe, 0) + 1
                else:
                    invalid_words.append(word_split_apostrophe)

    # This sorts the dictionary by values in descending order
    sorted_dict = dict(sorted(wordsdic.items(), key=lambda item: item[1], reverse=True))
    return sorted_dict, invalid_words

# This function creates the csv file using the name of the bookfile


def create_file(d, n):
    filename = n.split(".")[0]
    with open(filename + ".csv", "w", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        for row in d.items():
            writer.writerow(row)

# This function creates the text file from the list of invalid words


def create_invalid_word_file(i, n):
    filename = n.split(".")[0]
    with open(filename + "_invalid_words.txt", "w", encoding="utf-8-sig") as f:
        f.write("Invalid words: \n")
        for word in i:
            if not word.isdigit():
                f.write(word + "\n")


if __name__ == "__main__":
    main()
