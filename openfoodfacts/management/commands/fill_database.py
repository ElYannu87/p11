from django.core.management.base import BaseCommand
from django.db import transaction

from products.models import Category, Product


class Command(BaseCommand):
    """
    This class contains custom commands to fill the database with the help of manage.py
    """
    help = "command wich fills the database"

    def handle(self, *args, **options):
        """
        This method is executed when we call the command and this command
        fills the database if empty
        """
        if len(Product.objects.all()) > 0:
            self.stdout.write("La base de données est déjà remplie")
        else:
            with transaction.atomic():

                Category.objects.fill_categories()
                Product.objects.fill_products()

            self.stdout.write("Commande effectuée avec succès")