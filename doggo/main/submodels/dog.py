from datetime import timedelta, datetime
from typing import Optional, Tuple

from django.db import models

from main.submodels.account import Account
from main.submodels.breed import BreedType

DEFAULT_FOOD: float = 0.5
DEFAULT_FAT: float = 0.0
DEFAULT_AFFECTION: float = 0.5

WALKING_TIME: timedelta = timedelta(seconds=15*60)
EATING_TIME: timedelta = timedelta(seconds=10)
PLAYING_TIME: timedelta = timedelta(minutes=4)

# it takes LEFT_TIME to delete a dog after he left
LEFT_TIME: timedelta = timedelta(hours=24)


class DogStatus:
    AVAILABLE = 'AVAILABLE'  # dog does nothing
    WALKING = 'WALKING'  # dog is walking
    EATING = 'EATING'  # dog is eating
    PLAYING = 'PLAYING'  # dog is playing
    LEFT = 'LEFT'  # dog has left


class UIStatus:
    VERY_HAPPY = 'VERY_HAPPY'
    HAPPY = 'HAPPY'
    SAD = 'SAD'
    VERY_SAD = 'VERY_SAD'
    WALKING = DogStatus.WALKING
    LEFT = DogStatus.LEFT
    EATING = DogStatus.EATING
    PLAYING = DogStatus.PLAYING


class Dog(models.Model):
    class Meta:
        db_table = 'dogs'

    id = models.BigAutoField(auto_created=True, primary_key=True)
    account: Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    id_public: str = models.TextField(null=True, unique=True)
    created_at: datetime = models.DateTimeField(null=True)
    name: str = models.TextField(null=True)
    breed: str = models.TextField(default=BreedType.GERMAN_SHEPHERD)

    last_refresh: datetime = models.DateTimeField(null=True)
    status: str = models.TextField(default=DogStatus.AVAILABLE)
    status_set_at: datetime = models.DateTimeField(null=True)

    food: float = models.FloatField(default=DEFAULT_FOOD)  # between 0 and 1
    fat: float = models.FloatField(default=DEFAULT_FAT)  # between 0 and 1
    affection: float = models.FloatField(default=DEFAULT_AFFECTION)  # between 0 and 1

    def set_status(self, new_status: str, status_set_at: datetime):
        self.status = new_status
        self.status_set_at = status_set_at

    def happiness(self) -> float:  # between 0 and 1
        return min(
            self.food,
            1.0 - self.fat,
            self.affection
        )

    def description_status(self) -> str:
        ui_status: str = self.ui_status()

        description: str = ''
        if ui_status == UIStatus.LEFT:
            description: str = ' has left.'
        elif ui_status == UIStatus.WALKING:
            description: str = ' is walking.'
        elif ui_status == UIStatus.EATING:
            description: str = ' is eating.'
        elif ui_status == UIStatus.PLAYING:
            description: str = ' is playing.'
        elif ui_status == UIStatus.VERY_SAD:
            description: str = ' is very sad!'
        elif ui_status == UIStatus.SAD:
            description: str = ' is sad!'
        elif ui_status == UIStatus.HAPPY:
            description: str = ' is Happy!'
        elif ui_status == UIStatus.VERY_HAPPY:
            description: str = ' is very happy!'
        return self.name + description

    def extended_description_status(self, now: datetime) -> Optional[Tuple[str, float]]:
        if self.status == DogStatus.WALKING:
            return 'Back in ', (self.status_set_at + WALKING_TIME - now).total_seconds()
        elif self.status == DogStatus.EATING:
            return 'Back in ', (self.status_set_at + EATING_TIME - now).total_seconds()
        elif self.status == DogStatus.PLAYING:
            return 'Back in ', (self.status_set_at + PLAYING_TIME - now).total_seconds()
        elif self.status == DogStatus.LEFT:
            return 'Forgotten in ', (self.status_set_at + LEFT_TIME - now).total_seconds()
        else:
            return None

    def ui_status(self) -> str:
        if self.status == DogStatus.LEFT:
            return UIStatus.LEFT
        elif self.status == DogStatus.WALKING:
            return UIStatus.WALKING
        elif self.status == DogStatus.EATING:
            return UIStatus.EATING
        elif self.status == DogStatus.PLAYING:
            return UIStatus.PLAYING
        happiness: float = self.happiness()
        if happiness < 0.25:
            return UIStatus.VERY_SAD
        elif happiness < 0.5:
            return UIStatus.SAD
        elif happiness < 0.75:
            return UIStatus.HAPPY
        else:
            return UIStatus.VERY_HAPPY

    def image_path(self) -> str:
        return '/static/' + self.breed.lower() + '/' + self.ui_status().lower() + '.jpg'

    def age(self, now: datetime) -> int:
        """
        :return: Age in days
        """
        if now >= self.created_at:
            return int((now - self.created_at).total_seconds() / 86400.0)
        else:
            return 0

    def is_owner(self, account: Account) -> bool:
        return account is not None and account.id == self.account.id


def fetch_dog(id_public: str) -> Optional[Dog]:
    return Dog.objects.filter(id_public=id_public).first()


def create_dog(account: Account, id_public: str, created_at: datetime, name: str, breed: str) -> Dog:
    return Dog(
        account=account,
        id_public=id_public,
        created_at=created_at,
        name=name,
        breed=breed,
        last_refresh=created_at
    )


def fetch_dog_close_id_public(id_public: str) -> Optional[Dog]:
    """
    Return a dog which has a close id_public (not necessarily the closest one)
    :param id_public: any string
    :return:
    """
    dog: Optional[Dog] = Dog.objects.filter(id_public__gte=id_public).order_by('id_public').first()
    if dog is None:
        return Dog.objects.filter(id_public__lte=id_public).order_by('-id_public').first()
    else:
        return dog
