import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone

from library.models import Member, Category, Author, Publisher, Book


class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("🚀 Seeding database..."))

        self.create_members()
        self.create_categories()
        self.create_authors()
        self.create_publishers()
        self.create_books()

        self.stdout.write(self.style.SUCCESS("🎉 Database successfully seeded!"))

    # -------------------------
    # 1. Create Members
    # -------------------------
    def create_members(self):
        members_data = [
            {"user_name": "john_doe", "first_name": "John", "last_name": "Doe"},
            {"user_name": "jane_smith", "first_name": "Jane", "last_name": "Smith"},
            {"user_name": "alice_johnson", "first_name": "Alice", "last_name": "Johnson"},
            {"user_name": "michael_brown", "first_name": "Michael", "last_name": "Brown"},
        ]

        self.members = []
        for data in members_data:
            member, _ = Member.objects.get_or_create(
                username=data["user_name"],
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "user_name": data["user_name"],
                    "email": f"{data['user_name']}@example.com",
                    "password": "pbkdf2_sha256$260000$dummy$dummyhash"
                }
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
    def create_authors(self):
        authors_data = [
            ("George", "Orwell", "george.orwell@example.com"),
            ("J.K.", "Rowling", "jk.rowling@example.com"),
            ("Isaac", "Asimov", "isaac.asimov@example.com"),
            ("Stephen", "King", "stephen.king@example.com"),
            ("Yuval", "Harari", "yuval.harari@example.com"),
        ]

        self.authors = []
        for first, last, email in authors_data:
            author, _ = Author.objects.get_or_create(
                first_name=first,
                last_name=last,
                email=email
            )
            self.authors.append(author)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(self.authors)} authors."))

    # -------------------------
    # 4. Create Publishers
    # -------------------------
    def create_publishers(self):
        publishers_data = [
            ("Penguin Books", "https://www.penguin.co.uk"),
            ("HarperCollins", "https://www.harpercollins.com"),
            ("Simon & Schuster", "https://www.simonandschuster.com"),
            ("Random House", "https://www.randomhouse.com"),
        ]

        self.publishers = []
        for name, url in publishers_data:
            publisher, _ = Publisher.objects.get_or_create(name=name, website=url)
            self.publishers.append(publisher)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(self.publishers)} publishers."))

    # -------------------------
    # 5. Create Books
    # -------------------------
    def create_books(self):
        book_names = [
            "1984", "Harry Potter and the Philosopher's Stone", "Foundation",
            "The Shining", "Sapiens", "Animal Farm", "It", "Homo Deus"
        ]

        self.books = []
        for name in book_names:
            book, _ = Book.objects.get_or_create(
                name=name,
                publisher=random.choice(self.publishers),
                defaults={
                    "published_date": timezone.now() - timedelta(days=random.randint(100, 3000)),
                    "price": round(random.uniform(10, 50), 2),
                    "pages": random.randint(150, 800),
                    "is_available": random.choice([True, True, False]),
                }
            )

            # Add random categories
            random_cats = random.sample(self.categories, k=random.randint(1, 3))
            book.category.set(random_cats)

            # Add random authors
            random_auths = random.sample(self.authors, k=random.randint(1, 2))
            book.authors.set(random_auths)

            # Add random favourites
            random_members = random.sample(self.members, k=random.randint(0, len(self.members)))
            book.favourites.set(random_members)

            self.books.append(book)

        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(self.books)} books."))
