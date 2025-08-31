from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Member(AbstractUser):
    user_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    class CategoryChoices(models.TextChoices):
        BIOGRAPHIE = "BIO", _("Biographie")
        BUSINESS = "BUSI", _("Business")
        COMICS = "COMI", _("Comics")
        TECHNOLOGY = "TECH", _("Technology")
        COOKING = "COOK", _("Cooking")
        EDUCATIONAL = "EDU", _("Educational")
        ENTERTAINMENT = "ENT", _("Entertainment")
        HEALTH = "HEA", _("Health")
        HISTORY = "HIS", _("History")
        ROMANCE = "ROM", _("Romance")
        SPORT = "SPO", _("Sport")
        SCIFI = "SCI", _("Science Fiction")

    name = models.CharField(max_length=100, 
                            choices=CategoryChoices.choices, 
                            default=CategoryChoices.BIOGRAPHIE)
    
    def __str__(self):
        return self.name

 
class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    email = models.EmailField(verbose_name="Email Address")

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    category = models.ManyToManyField(Category, related_name='book')
    authors = models.ManyToManyField(Author, related_name='book')
    publisher = models.ForeignKey(Publisher, 
                                  on_delete=models.CASCADE, 
                                  related_name="publisher",
                                  default=None)
    favourites = models.ManyToManyField(Member, 
                                        related_name="favourite", 
                                        default=None, 
                                        blank=True)
    title = models.CharField(max_length=100)
    published_date = models.DateField(default=None)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.FloatField(null=True, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    summary = models.TextField(default=None, blank=True, null=True)
    picture = models.FileField(upload_to='uploads/images/library/', 
                               blank=True, 
                               null=True, 
                               default=None)

    def __str__(self):
        return self.title
