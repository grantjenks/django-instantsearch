"""Process Books

$ curl https://dl.typesense.org/datasets/books.jsonl.gz | gunzip > books.jsonl
$ python process_books.py
$ mv updated_books.json books.jsonl

"""

import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

input_file_path = 'books.jsonl'
output_file_path = 'updated_books.jsonl'


def generate_synopsis_with_llm(book_json_str):
    command = ['llm', '-m', '3.5', 'Generate a synopsis of the book.']
    result = subprocess.run(
        command, input=book_json_str, text=True, capture_output=True
    )
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return 'Synopsis generation failed.'


def process_book(book_line):
    book_json_str = book_line.strip()
    book = json.loads(book_json_str)
    if 'synopsis' not in book:
        book['synopsis'] = generate_synopsis_with_llm(book_json_str)
        updated_book_str = json.dumps(book)
    else:
        updated_book_str = book_json_str
    return updated_book_str


def update_books_with_synopsis(input_path, output_path):
    try:
        with open(output_path, 'r') as file:
            processed_ids = {json.loads(line)['id'] for line in file}
    except FileNotFoundError:
        processed_ids = set()

    with open(input_path, 'r') as input_file:
        books_to_process = [
            line for line in input_file if json.loads(line)['id'] not in processed_ids
        ]

    with ThreadPoolExecutor(max_workers=40) as executor:
        future_to_book = [
            executor.submit(process_book, book) for book in books_to_process
        ]

        with open(output_file_path, 'a') as output_file:
            for future in tqdm(
                as_completed(future_to_book),
                total=len(future_to_book),
                desc='Processing Books',
            ):
                updated_book_str = future.result()
                output_file.write(updated_book_str + '\n')


update_books_with_synopsis(input_file_path, output_file_path)
