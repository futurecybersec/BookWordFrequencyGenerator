import csv
import sys

# Combines 2 word frequency csv files
def main():
    words_1 = {}
    words_2 = {}

    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")

    filename1 = sys.argv[1]
    filename2 = sys.argv[2]

    if not filename1.endswith(".csv") or not filename2.endswith(".csv"):
        sys.exit("Not a csv file")

    with open(filename1, encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            words_1[row[0]] = int(row[1])

    with open(filename2, encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            words_2[row[0]] = int(row[1])

    words = {k: words_1.get(k, 0) + words_2.get(k, 0) for k in set(words_1) | set(words_2)}

    with open(f'{filename1.split(".")[0]}_{filename2.split(".")[0]}_combined.csv', "w", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        for row in words.items():
            writer.writerow(row)


if __name__ == "__main__":
    main()

