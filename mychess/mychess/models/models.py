from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.


class Player(AbstractUser):

    rating = models.IntegerField(max_length=4, help_text="The rate of the player")

    class Meta:
        ordering = ["rating"]

    def __str__(self):

        return "Este jugador tiene un rating de: " + self.rating + " se ecnuentra " + str(2830 - self.rating)  + " puntos por debajo de Carlsen"


class ChessGame():

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda la biblioteca")

    LOAN_STATUS = (
        ('p', 'Pending'),
        ('a', 'Active'),
        ('f', 'Finished'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Disponibilidad del libro')
    board_state = models.CharField(max_length=1000, default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", help_text="El estado del tablero actualmente")
    start_time = models.DateField(max_length=11, help_text="La fecha a la que se creo la partida")
    end_time = models.DateField(max_length=11, help_text="La fecha a la que se creo la partida", null=True, blank=True)

class ChessMove():



AUTH_USER_MODEL = "models.Player"
