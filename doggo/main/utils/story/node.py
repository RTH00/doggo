import random
from typing import Callable, Set, Optional, List

from main.submodels.account import Account
from main.submodels.dog import Dog


class NodeLink:
    def __init__(self,
                 node_id: str,
                 probability_weight: int):
        self.node_id = node_id
        self.probability_weight = probability_weight

    def sanity_check(self) -> bool:
        if self.probability_weight <= 0:
            raise Exception("probability_weight should be >= 1 value: " + str(self.probability_weight))
        return True


class Choice:
    def __init__(self,
                 id: str,
                 text: Callable[[Dog], str],
                 links: [NodeLink]):
        self.id = id
        self.text = text
        self.links = links

    def sanity_check(self) -> bool:
        if self.id == '' or not self.id.isdigit:
            raise Exception("Invalid id:`" + self.id + "`")
        if len(self.links) <= 0:
            raise Exception("No link")
        for link in self.links:
            link.sanity_check()
        return True


class Node:
    def __init__(self,
                 id: str,
                 text: Callable[[Dog], str],
                 choices=None,
                 effect: Callable[[Account, Dog], None] = lambda account, dog: None
                 ):
        if choices is None:
            choices = list()
        self.id = id
        self.text = text
        self.choices = choices
        self.effect = effect

    def choices_sanity_check(self) -> bool:
        """
        Throw an exception if:
        - two choices have the same id
        - the recursive sanity_check throws an exception
        :return:
        """
        id_set: Set[str] = set()
        for choice in self.choices:
            choice.sanity_check()
            id: str = choice.id
            if id in id_set:
                raise Exception("Duplicated id: `" + id + "`")
            else:
                id_set.add(id)
        return True

# TODO sanity check for Node links and tests


def sample_node_links(links: [NodeLink]) -> str:
    """
    Sample a link proportionally to its probability_weight
    :param links:
    :return: node_id (str)
    """
    total: int = 0
    for link in links:
        total += link.probability_weight
    sample: int = random.randrange(total) + 1
    for link in links:
        sample -= link.probability_weight
        if sample <= 0:
            return link.node_id
    raise Exception('Should not reach, a probability_weight is probably negative')


def find_choice(choice_id: str, choices: List[Choice]) -> Optional[Choice]:
    for choice in choices:
        if choice.id == choice_id:
            return choice
    return None





