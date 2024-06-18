from django.db import models
from app.users.models.ArchimatchUser import ArchimatchUser
from app.utils.models import BaseModel


class Client(BaseModel):
    user = models.OneToOneField(ArchimatchUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
    def delete(self, *args, **kwargs):
        self.user.delete() 
        super().delete(*args, **kwargs)