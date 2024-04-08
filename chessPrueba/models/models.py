from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.


class Player(AbstractUser):

    rating = models.IntegerField( help_text="The rate of the player", default=0)

    class Meta:
        ordering = ["rating"]

    def __str__(self):

        return self.name
   



class ChessGame(models.Model):

    LOAN_STATUS = (
        ('p', 'Pending'),
        ('a', 'Active'),
        ('f', 'Finished'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Disponibilidad del libro')
    board_state = models.CharField(max_length=1000, default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", help_text="El estado del tablero actualmente")
    start_time = models.DateField(max_length=11, help_text="La fecha a la que se creo la partida")
    end_time = models.DateField(max_length=11, help_text="La fecha a la que se creo la partida", null=True, blank=True)
    timeControl = models.IntegerField(help_text="The ammount of time that each player have to make a move")
    blackPlayer = models.ForeignKey('Player', on_delete=models.RESTRICT, related_name="black_layer")
    whitePlayer =  models.ForeignKey('Player', on_delete=models.RESTRICT, related_name="white_player")
    winner = models.ForeignKey('Player', null=True, on_delete=models.RESTRICT, related_name="winner")

    def __str__(self):
        return self.board_state

class ChessMove(models.Model):
    
    PROMOTIONS = (
        ('q', 'queen'),
        ('r', 'rook'),
        ('n', 'knight'),
        ('b', 'bishop'),
    )

    game = models.ForeignKey('ChessGame', on_delete=models.RESTRICT)
    player = models.ForeignKey('Player', on_delete=models.RESTRICT)
    move_from = models.CharField(max_length=2, help_text="The coords from where the figure is moved from")
    move_to = models.CharField(max_length=2, help_text="The coordenates where the figure is moved to")
    promotion = models.CharField(max_length=8, help_text="The figure that is promoted to", choices=PROMOTIONS, null=True)

    def __str__(self):
        if(self.promotion):
            return "From " + self.move_from + " to " + self.move_to