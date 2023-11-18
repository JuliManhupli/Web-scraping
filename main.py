import json
import re

from conf.models import Author, Quote


def print_quotes(quotes):
    for quote in quotes:
        print(f"Author: {quote['author']}\nTags: {', '.join(quote['tags'])}\nQuote: {quote['quote']}\n")


def search_quotes_by_tags(tags):
    search_tags = []
    for tag in tags:
        search_tags.append(re.compile(f'^{re.escape(tag)}', re.IGNORECASE))
    return Quote.objects(tags__in=search_tags)


def search_quotes_by_author(name):
    regex = re.compile(f'^{re.escape(name)}', re.IGNORECASE)
    authors = Author.objects(fullname=regex)
    quotes = Quote.objects(author__in=authors)
    return quotes


def quotes_to_list(quotes):
    quotes_list = []
    for quote in quotes:
        quotes_list.append({
            "author": quote.author.fullname,
            "tags": quote.tags,
            "quote": quote.quote
        })
    return quotes_list


def search_quotes(command, value):
    if command == 'name':
        quotes = search_quotes_by_author(value)
        quotes = quotes_to_list(quotes)
    elif command in ['tag', 'tags']:
        quotes = search_quotes_by_tags(value.split(","))
        quotes = quotes_to_list(quotes)
    else:
        return "Unknown command"

    if quotes:

        print_quotes(quotes)
        return "Quotes found"
    else:
        return "No quote found"


if __name__ == '__main__':
    while True:
        user_input = input("Enter the query: ").strip().lower()
        if user_input in ["exit", "q", "0"]:
            print("Goodbye!")
            break

        try:
            command, value = user_input.split(":", 1)
            result = search_quotes(command.strip(), value.strip())
            print(result)
        except ValueError:
            print("Incorrect input. Expected \"command: value\"")
