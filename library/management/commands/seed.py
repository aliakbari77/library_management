import random
import requests
from datetime import timedelta
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from library.models import Member, Category, Author, Publisher, Book

fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with random test data including images"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing data before seeding",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            self.stdout.write(self.style.WARNING("🗑 Clearing old data..."))
            Book.objects.all().delete()
            Author.objects.all().delete()
            Publisher.objects.all().delete()
            Member.objects.all().delete()

        self.stdout.write(self.style.WARNING("🚀 Seeding database..."))

        self.create_members(50)
        self.create_categories()
        self.create_authors(100)
        self.create_publishers(100)
        self.create_books(200)

        self.stdout.write(self.style.SUCCESS("🎉 Database successfully seeded!"))

    # -------------------------
    # 1. Create Members
    # -------------------------
    def create_members(self, count):
        self.members = []
        for _ in range(count):
            username = fake.user_name()
            member, _ = Member.objects.get_or_create(
                username=username,
                defaults={
                    "user_name": username,
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "email": fake.email(),
                    "password": "pbkdf2_sha256$260000$dummy$dummyhash",
                },
            )
            self.members.append(member)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(self.members)} members."))

    # -------------------------
    # 2. Create Categories
    # -------------------------
    def create_categories(self):
        self.categories = []
        for choice in Category.CategoryChoices.choices:
            category, _ = Category.objects.get_or_create(name=choice[0])
            self.categories.append(category)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(self.categories)} categories."))

    # -------------------------
    # 3. Create Authors
    # -------------------------
    def create_authors(self, count):
        self.authors = []
        for _ in range(count):
            author, _ = Author.objects.get_or_create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
            )
            self.authors.append(author)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(self.authors)} authors."))

    # -------------------------
    # 4. Create Publishers
    # -------------------------
    def create_publishers(self, count):
        self.publishers = []
        for _ in range(count):
            publisher, _ = Publisher.objects.get_or_create(
                name=fake.company(),
                website=fake.url(),
            )
            self.publishers.append(publisher)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(self.publishers)} publishers."))

    # -------------------------
    # 5. Create Books
    # -------------------------
    def create_books(self, count):
        self.books = []
        book_titles = set()

        for _ in range(count):
            # Ensure unique titles
            title = fake.sentence(nb_words=4).replace(".", "")
            while title in book_titles:
                title = fake.sentence(nb_words=4).replace(".", "")
            book_titles.add(title)

            # Download a random image from Lorem Picsum
            image_url = f"https://picsum.photos/400/600?random={random.randint(1, 10000)}"
            image_content = requests.get(image_url).content

            book = Book.objects.create(
                title=title,
                publisher=random.choice(self.publishers),
                published_date=timezone.now() - timedelta(days=random.randint(100, 3000)),
                price=round(random.uniform(10, 100), 2),
                pages=random.randint(100, 1000),
                is_available=random.choice([True, True, False]),
                summary=fake.paragraph(nb_sentences=5),
            )

            # Save the image to the picture field
            book.picture.save(f"{title}.jpg", ContentFile(image_content), save=True)

            # Add random categories
            random_cats = random.sample(self.categories, k=random.randint(1, 3))
            book.category.set(random_cats)

            # Add random authors
            random_auths = random.sample(self.authors, k=random.randint(1, 3))
            book.authors.set(random_auths)

            # Add random favourites
            random_members = random.sample(self.members, k=random.randint(0, min(5, len(self.members))))
            book.favourites.set(random_members)

            self.books.append(book)

        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(self.books)} books."))
