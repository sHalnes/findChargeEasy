from django.db import models

# we save user location for statistic. Later we can update db and save also location and info of charging stations
# such as we can use it if we do not have access to API (server is down for example)

class UserLocation(models.Model):
    user_location = models.CharField(max_length=300)

    def __str__(self):
        return self.user_location