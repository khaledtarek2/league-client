from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import datetime
from django.core.cache import cache

class Rank(models.Model):
    class Types(models.IntegerChoices):
        Solo_Duo = 0
        FLEX = 1
        TFT = 2

    class Level(models.TextChoices):
        UNRANKED = 'UNRANKED'
        IRON = 'IRON'
        BRONZE = 'BRONZE'
        SILVER = 'SILVER'
        GOLD = 'GOLD'
        PLAT = 'PLAT'
        DIAMOND = 'DIAMOND'
        MASTER = 'MASTER'
        GRANDMASTER = 'GRANDMASTER'
        CHALENGER = 'CHALENGER'

    type = models.IntegerField(
        choices=Types.choices,
        default=Types.Solo_Duo,
    )
    rank = models.CharField(
        max_length=11,
        choices=Level.choices,
        default=Level.UNRANKED,
    )
    
    def __str__(self) -> str:
        return f'{self.rank}'


def validate_less_than_5(value):
        if value > 5:
            raise ValidationError(
                ('%(value)s is more than 5'),
                params={'value': value},
            )
   
class RankImage(models.Model):
    rank = models.ForeignKey(Rank, related_name='images', on_delete=models.CASCADE)
    icon = models.ImageField(null=True, blank=True)
    border = models.ImageField(null=True, blank=True)

    
class Profile(models.Model):
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE)
    honor_level = models.IntegerField(default=2, validators=[validate_less_than_5])
    
    
    def __str__(self) -> str:
        return f'{self.rank}'

class ProfileImage(models.Model):
    profile = models.ForeignKey(Profile, related_name='images', on_delete=models.CASCADE)
    background_pick = models.ImageField(null=True, blank=True)
    trophy = models.ImageField(null=True, blank=True)
    banner = models.ImageField(null=True, blank=True)


class Player(AbstractUser):
    class Server(models.IntegerChoices):
        EUW = 0
        NA = 1
        CHINA = 2
        KOREA = 3
        RUSSIA = 4
    class PaymentCurrency(models.IntegerChoices):
        RP = 0
        BE = 1

    is_online = models.BooleanField(default=False)
    level = models.IntegerField(default=1)
    server = models.IntegerField(choices=Server.choices, null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='player')
    friends = models.ManyToManyField(
        'Player', related_name= '+'
    )

    def __str__(self) -> str:
        return f'{self.username}'
    
    def last_seen(self):
        return cache.get('last_seen_%s' % self.username)
    
    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > (self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)):
                return False
            else:
                return True
        else: 
            return False

class PlayerImage(models.Model):
    player = models.ForeignKey(Player, related_name='images', on_delete=models.CASCADE)
    icon = models.ImageField(null=True, blank=True)
    
    
    
  
class PlayerSeasonGrade(models.Model):
    class SeasonGrade(models.IntegerChoices):
        C_PLUS = 0
    
        B_MINUS = 1
        B = 2
        B_PLUS = 3
        
        A_MINUS = 4
        A = 5
        A_PLUS = 6

        S_MINUS = 7
        S = 8
        S_PLUS = 9

    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='season_grades')
    champion = models.ForeignKey('champions.Champion', on_delete=models.CASCADE, null=True, blank=True, related_name='season_grades')
    grade = models.IntegerField(choices=SeasonGrade.choices)
    obtained_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.player} got {self.grade} by playing {self.champion}'

class Message(models.Model):
     sender = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='sender')        
     receiver = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='receiver')        
     message = models.CharField(max_length=1200)
     timestamp = models.DateTimeField(auto_now_add=True)
     is_read = models.BooleanField(default=False)
     def __str__(self):
           return self.message
     class Meta:
           ordering = ('timestamp',)