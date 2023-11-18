import json
import pathlib

from conf.models import Author, Quote

authors_path = pathlib.Path(__file__).parent.joinpath('data').joinpath('authors.json')
quotes_path = pathlib.Path(__file__).parent.joinpath('data').joinpath('quotes.json')


def load_data_from_json(path):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


# Функція для нормалізації рядків
def normalize_string(s):
    s = s.replace('-', ' ')
    return s


authors_data = load_data_from_json(authors_path)
for author_data in authors_data:
    normalized_fullname = normalize_string(author_data['fullname'])
    author = Author(
        fullname=normalized_fullname,
        born_date=author_data['born_date'],
        born_location=author_data['born_location'],
        description=author_data['description'],
    )
    author.save()

quotes_data = load_data_from_json(quotes_path)
for quote_data in quotes_data:
    normalized_author_fullname = normalize_string(quote_data['author'])
    author = Author.objects(fullname=normalized_author_fullname).first()
    if author:
        quote = Quote(
            tags=quote_data['tags'],
            author=author,
            quote=quote_data['quote'],
        )
        quote.save()
    else:
        print(f"Author '{quote_data['author']}' not found.")
