import pytest
import sys
from io import StringIO
from project import get_book_filename, get_lines, count_words, create_file, create_invalid_word_file

def test_get_book_filename(monkeypatch):
    # Test with correct arguments
    monkeypatch.setattr(sys, 'argv', ['project.py', 'book.txt'])
    assert get_book_filename(sys.argv) == 'book.txt'

    # Test with too few arguments
    monkeypatch.setattr(sys, 'argv', ['project.py'])
    with pytest.raises(SystemExit):
        get_book_filename(sys.argv)

    # Test with too many arguments
    monkeypatch.setattr(sys, 'argv', ['project.py', 'book.txt', 'extra.txt'])
    with pytest.raises(SystemExit):
        get_book_filename(sys.argv)

    # Test with incorrect file type
    monkeypatch.setattr(sys, 'argv', ['project.py', 'book.pdf'])
    with pytest.raises(SystemExit):
        get_book_filename(sys.argv)

def test_get_lines(monkeypatch):
    # Test with a valid file
    monkeypatch.setattr('builtins.open', lambda f: StringIO("line1\nline2\n\nline3\n"))
    assert get_lines('book.txt') == ['line1', 'line2', 'line3']

    # Test with a non-existent file
    monkeypatch.setattr('builtins.open', lambda f: (_ for _ in ()).throw(FileNotFoundError))
    with pytest.raises(SystemExit):
        get_lines('book.txt')

def test_count_words():
    lines = ["Hello world", "Hello again", "world world"]
    dictionary, invalid_words = count_words(lines)
    assert dictionary == {'world': 3, 'hello': 2, 'again': 1}
    assert invalid_words == []

    lines = ["Hello world!", "Hello again.", "world world123"]
    dictionary, invalid_words = count_words(lines)
    assert dictionary == {'hello': 2, 'world': 2, 'again': 1}
    assert invalid_words == ['world123']

def test_create_file(tmp_path):
    d = {'hello': 2, 'world': 3}
    n = tmp_path / "book.txt"
    create_file(d, str(n))
    expected_output = "hello,2\nworld,3\n"
    with open(str(n).replace(".txt", ".csv"), encoding="utf-8-sig") as f:
        assert f.read() == expected_output

def test_create_invalid_word_file(tmp_path):
    i = ['world123', '123']
    n = tmp_path / "book.txt"
    create_invalid_word_file(i, str(n))
    expected_output = "Invalid words: \nworld123\n"
    with open(str(n).replace(".txt", "_invalid_words.txt"), encoding="utf-8-sig") as f:
        assert f.read() == expected_output