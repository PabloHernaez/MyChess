
import json
from django.core.mail import message
from django.test.testcases import ValidationError
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChessMove, ChessGame, Player
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.authtoken.models import Token
from asgiref.sync import sync_to_async


#from django.contrib.auth.models import AnonymousUser


class ChessConsumer(AsyncWebsocketConsumer):
    """
     async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['gameID']
        self.token = self.scope['query_string'].decode()
        self.game_group_name = f"game_{self.game_id}"

        await self.accept()

        # Verificar si el token es válido
        self.user = await self.is_valid_token()

        if not self.user.is_active:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid token. Connection not authorized.'
            }))
            await self.close()
        else:
            # Verificar si el juego existe y el par (usuario, juego) es válido
            game_exists = await self.game_exists()
            valid_pair = await self.is_valid_user_game_pair()
            
            if not game_exists or not valid_pair:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': f'Invalid game with id {self.game_id}'
                }))
                await self.close()
            else:
                await self.send(text_data=json.dumps({
                    'type': 'game',
                    'message': 'OK'
                }))
                
                await self.channel_layer.group_add(
                    self.game_group_name,
                    self.channel_name
                )
    
    """
        
    async def game_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['gameID']
        self.game = await self.from_id(self.game_id)      

        token = self.scope['query_string'].decode()      

        self.user = await self.get_user_by_token(token)
        await self.accept()

        
        if self.game is None:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Invalid game with id {self.game_id}',
                'status': None,
                'playerID': None,
            }))
            await self.close()
            return



        if self.user is None or not await self.is_valid_user_game_pair(self.user, self.game):
            
            if self.user is not None:
                message = f'Invalid game with id {self.game_id}'
            else:
                message = f'Invalid token. Connection not authorized.'

            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': message, 
                'status': self.game.status.upper(),
                'playerID': None,
            }))
            await self.close()
        else:
            await self.channel_layer.group_add(str(self.game_id), self.channel_name)

            await self.game_cb('game', 'OK', self.game.status.upper(), self.user.id)


    async def receive(self, text_data):
        data = json.loads(text_data)
        m_from = ''
        m_to = ''
        id_player = ''
        promotion = ''
        if data['type'] == 'move':
            try:
                m_from = data['from']
                m_to = data['to']
                id_player = data['playerID']
                promotion = None
                promotion = data['promotion']
                # crea un nuevo movimiento, se llama a save con la creación y en ese método se comprueba la validez del movimiento
                await sync_to_async(ChessMove.objects.create)(
                    game=self.game,
                    player=self.user,
                    move_from=m_from,
                    move_to=m_to,
                    promotion=promotion
                )
                await self.move_cb('move', m_from, m_to, id_player, promotion, None)

                #COMPROBACIONES
            except ValidationError:
                message = f"Error: invalid move (game is not active)"
                await self.move_cb('error', m_from, m_to, id_player, promotion, message)
            except ValueError:
                message = f'Error: invalid move {m_from}{m_to}' 
                await self.move_cb('error', m_from, m_to, id_player, promotion, message)
            except Exception:
                await self.move_cb('error', m_from, m_to, id_player, promotion, None)
        else:
            return


        """
        async def receive(self, text_data):
            data = json.loads(text_data)
            m_from = ''
            m_to = ''
            playerID = ''
            promotion = ''
            if data['type'] == 'move':
                try:
                    m_from = data['from']
                    m_to = data['to']
                    playerID = data['playerID']
                    promotion = data.get('promotion', None)  # Usa data.get() para obtener el valor opcional
                    await self.create_and_send_move(m_from, m_to, playerID, promotion)
                except (ValidationError, ValueError):
                    message = f"Error: invalid move {m_from}{m_to}"
                    await self.move_cb('error', m_from, m_to, playerID, promotion, message)
                except Exception:
                    await self.move_cb('error', m_from, m_to, playerID, promotion, None)
            else:
                return
        """     

    async def game_cb(self, _type, message, status, player_id):
        await self.channel_layer.group_send(
            str(self.game_id),
            {
                'type': 'game.message',  
                'message': {
                    'type': _type,
                    'message': message,
                    'status': status,
                    'playerID': player_id,
                }
            }
        )

    async def move_cb(self, _type, m_from, m_to, player_id, promotion, _message):
        await self.channel_layer.group_send(str(self.game_id),{
                'type': 'move.message',  

                'message': {
                    'type': _type,
                    'from': m_from,
                    'to': m_to,
                    'playerID': player_id,
                    'promotion': promotion,
                    'message': _message, 
                }
            }
        )

    async def move_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(str(self.game_id), self.channel_name)

    @database_sync_to_async
    def get_user_by_token(self, token_key):
        try:
            token = Token.objects.get(key=token_key)

            return token.user
        except Token.DoesNotExist:
            return None
    
    """
            @database_sync_to_async
        def is_valid_token(self):

            try:
                self.token = Token.objects.get(key=self.token)
                return self.token.user
            except Token.DoesNotExist:
                return AnonymousUser()
    """


    @database_sync_to_async
    def from_id(self, game_id): #GET GAME FROM ID
        try:
            game = ChessGame.objects.get(id=game_id)
            return game
        except ChessGame.DoesNotExist:
            return None

    @database_sync_to_async
    def is_valid_user_game_pair(self, user, game):
        return ChessGame.objects.filter(id=self.game_id, whitePlayer_id=self.user.id).exists() or \
            ChessGame.objects.filter(id=self.game_id, blackPlayer_id=self.user.id).exists()
    

    """
            
        @database_sync_to_async
        def game_exists(self):
            # Función para verificar si el juego existe
            return ChessGame.objects.filter(id=self.game_id).exists()
        
        @database_sync_to_async

        def is_valid_user_game_pair(self):
            # Función para verificar si el par (usuario, juego) es válido
            return ChessGame.objects.filter(id=self.game_id, whitePlayer_id=self.user.id).exists() or \
                ChessGame.objects.filter(id=self.game_id, blackPlayer_id=self.user.id).exists()

    """