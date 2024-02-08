import json

import tqdm

from django.core.management.base import BaseCommand, CommandError

from www.models import Book


class Command(BaseCommand):
    help = 'Loads data from a JSONL file into the Book model'

    def add_arguments(self, parser):
        parser.add_argument(
            'jsonl_file', type=str, help='Path to the JSONL file to be loaded'
        )

    def handle(self, *args, **options):
        jsonl_file_path = options['jsonl_file']

        try:
            with open(jsonl_file_path, 'r') as file:
                for line in tqdm.tqdm(file):
                    data = json.loads(line)

                    # Check if the book already exists to prevent duplicates
                    if not Book.objects.filter(book_id=data['id']).exists():
                        Book.objects.create(
                            title=data['title'],
                            authors=data['authors'],
                            publication_year=data['publication_year'],
                            average_rating=data['average_rating'],
                            image_url=data['image_url'],
                            ratings_count=data['ratings_count'],
                            synopsis=data['synopsis'],
                            book_id=data['id'],
                        )
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Successfully added book: {data['title']}"
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f"Book already exists: {data['title']}")
                        )
        except FileNotFoundError:
            raise CommandError(f"File '{jsonl_file_path}' does not exist")
        except json.JSONDecodeError as e:
            raise CommandError(f'Error decoding JSON: {str(e)}')
