
"""
This file contains manager of Favorite model
"""
from django.db import models


class FavoriteManager(models.Manager):
    """
        This class is the manager of the favorite model
    """

    def get_favorites_from_user(self, user):
        """
        This method returns favorite of a user
        """
        return self.filter(user=user)