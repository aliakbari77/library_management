import random
from django.core.management.base import BaseCommand
from faker import Faker
from library.models import Category, Book

fake = Faker()

class Command(BaseCommand):
    help = "Fill categories with fake data and randomly assign them to books"

    def handle(self, *args, **kwargs):
        categories = [
            "Biographie",
            "Business",
            "Comics",
            "Technology",
            "Cooking",
            "Educational",
            "Entertainment",
            "Health",
            "History",
            "Romance",
            "Sport",
            "Science Fiction",
        ]
        for category in categories:
            Category.objects.create(name=category)

        categories_list = list(Category.objects.all())

        # Step 2: Assign random categories to each book
        books = Book.objects.all()
        for book in books:
            # Select between 1 and 3 random categories per book
            random_categories = random.sample(categories_list, k=random.randint(1, 3))
            book.category.set(random_categories)
            book.save()

        self.stdout.write(self.style.SUCCESS(f"✅ Assigned random categories to {books.count()} books."))
