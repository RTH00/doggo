from typing import Dict

from main.submodels.events.dog_action_event_type import DogActionEventType


class BreedType:
    GERMAN_SHEPHERD: str = 'GERMAN_SHEPHERD'
    GOLDEN_RETRIEVER: str = 'GOLDEN_RETRIEVER'
    CHICKEN: str = 'CHICKEN'
    CORGI: str = 'CORGI'


def build_decreasing_rate(nbr_of_hours: float) -> float:
    """
    Build a rate which makes a 1.0 value falls to 0.0 in nbr_of_hours hours
    :param nbr_of_hours: How much hours to reach 0 from 1.0
    :return: rate in value.s-1
    """
    return 1.0 / (nbr_of_hours * 3600)


def build_proba(nbr_tries: int) -> float:
    return 1.0 / float(nbr_tries)


class BreedProperties:
    def __init__(self,
                 food_consumption_rate: float,
                 affection_consumption_rate: float,
                 walking_fat_converge_rate: float,
                 walking_affection_converge_rate: float,
                 playing_fat_converge_rate: float,
                 playing_affection_converge_rate: float,
                 eating_food_increase: float,
                 eating_fat_increase: float,
                 walking_action_probability: Dict[str, float],
                 playing_action_probability: Dict[str, float]
                 ):
        self.food_consumption_rate = food_consumption_rate
        self.affection_consumption_rate = affection_consumption_rate
        self.walking_fat_converge_rate = walking_fat_converge_rate
        self.walking_affection_converge_rate = walking_affection_converge_rate
        self.playing_fat_converge_rate = playing_fat_converge_rate
        self.playing_affection_converge_rate = playing_affection_converge_rate
        self.eating_food_increase = eating_food_increase
        self.eating_fat_increase = eating_fat_increase
        self.walking_action_probability = walking_action_probability
        self.playing_action_probability = playing_action_probability


BREED_PROPERTIES: Dict[str, BreedProperties] = {
    BreedType.GERMAN_SHEPHERD: BreedProperties(
        food_consumption_rate=build_decreasing_rate(50),
        affection_consumption_rate=build_decreasing_rate(80),
        walking_fat_converge_rate=0.2,
        walking_affection_converge_rate=0.4,
        playing_fat_converge_rate=0.1,
        playing_affection_converge_rate=0.20,
        eating_food_increase=0.6,
        eating_fat_increase=0.25,
        walking_action_probability={
            DogActionEventType.FIND_FITNESS_COOKIE: build_proba(25),
            DogActionEventType.FIND_MAGIC_BONE: build_proba(80),
            DogActionEventType.FIND_TENNIS_BALL: build_proba(25),
            DogActionEventType.MEET_ANOTHER_DOG: build_proba(5),
            DogActionEventType.GO_STORY: build_proba(10)
        },
        playing_action_probability={
            DogActionEventType.FIND_FITNESS_COOKIE: build_proba(20),
            DogActionEventType.FIND_MAGIC_BONE: build_proba(70),
            DogActionEventType.FIND_TENNIS_BALL: build_proba(20),
            DogActionEventType.MEET_ANOTHER_DOG: build_proba(10)
        }
    ),
    BreedType.GOLDEN_RETRIEVER: BreedProperties(
        food_consumption_rate=build_decreasing_rate(50),
        affection_consumption_rate=build_decreasing_rate(80),
        walking_fat_converge_rate=0.3,
        walking_affection_converge_rate=0.3,
        playing_fat_converge_rate=0.15,
        playing_affection_converge_rate=0.15,
        eating_food_increase=0.6,
        eating_fat_increase=0.25,
        walking_action_probability={
            DogActionEventType.FIND_FITNESS_COOKIE: build_proba(25),
            DogActionEventType.FIND_MAGIC_BONE: build_proba(80),
            DogActionEventType.FIND_TENNIS_BALL: build_proba(25),
            DogActionEventType.MEET_ANOTHER_DOG: build_proba(5),
            DogActionEventType.GO_STORY: build_proba(10)
        },
        playing_action_probability={
            DogActionEventType.FIND_FITNESS_COOKIE: build_proba(20),
            DogActionEventType.FIND_MAGIC_BONE: build_proba(70),
            DogActionEventType.FIND_TENNIS_BALL: build_proba(20),
            DogActionEventType.MEET_ANOTHER_DOG: build_proba(10)
        }
    ),
    BreedType.CORGI: BreedProperties(
        food_consumption_rate=build_decreasing_rate(65),
        affection_consumption_rate=build_decreasing_rate(100),
        walking_fat_converge_rate=0.2,
        walking_affection_converge_rate=0.3,
        playing_fat_converge_rate=0.1,
        playing_affection_converge_rate=0.15,
        eating_food_increase=0.6,
        eating_fat_increase=0.25,
        walking_action_probability={
            DogActionEventType.FIND_FITNESS_COOKIE: build_proba(25),
            DogActionEventType.FIND_MAGIC_BONE: build_proba(80),
            DogActionEventType.FIND_TENNIS_BALL: build_proba(25),
            DogActionEventType.MEET_ANOTHER_DOG: build_proba(5),
            DogActionEventType.GO_STORY: build_proba(10)
        },
        playing_action_probability={
            DogActionEventType.FIND_FITNESS_COOKIE: build_proba(20),
            DogActionEventType.FIND_MAGIC_BONE: build_proba(70),
            DogActionEventType.FIND_TENNIS_BALL: build_proba(20),
            DogActionEventType.MEET_ANOTHER_DOG: build_proba(10)
        }
    ),
    BreedType.CHICKEN: BreedProperties(
        food_consumption_rate=build_decreasing_rate(90),
        affection_consumption_rate=build_decreasing_rate(130),
        walking_fat_converge_rate=0.3,
        walking_affection_converge_rate=0.2,
        playing_fat_converge_rate=0.1,
        playing_affection_converge_rate=0.1,
        eating_food_increase=0.2,
        eating_fat_increase=0.05,
        walking_action_probability={
            DogActionEventType.FIND_FITNESS_COOKIE: build_proba(50),
            DogActionEventType.FIND_MAGIC_BONE: build_proba(160),
            DogActionEventType.FIND_TENNIS_BALL: build_proba(50),
            DogActionEventType.MEET_ANOTHER_DOG: build_proba(10),
            DogActionEventType.GO_STORY: build_proba(10)
        },
        playing_action_probability={
            DogActionEventType.FIND_FITNESS_COOKIE: build_proba(40),
            DogActionEventType.FIND_MAGIC_BONE: build_proba(140),
            DogActionEventType.FIND_TENNIS_BALL: build_proba(40),
            DogActionEventType.MEET_ANOTHER_DOG: build_proba(20)
        }
    )
}
