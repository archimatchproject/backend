from django.db import models
from app.users.models.ArchimatchUser import ArchimatchUser
from app.models import BaseModel


class Client(BaseModel):

    user = models.OneToOneField(ArchimatchUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
