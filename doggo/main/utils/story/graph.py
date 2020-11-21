from typing import Dict

from main.utils.story.effect import fitness_cookie_update
from main.utils.story.graphs.anubis import ANUBIS_STORY_NODES, START_ANUBIS
from main.utils.story.graphs.squirrel import START_SQUIRREL, SQUIRREL_STORY_NODES
from main.utils.story.node import Node, NodeLink, Choice

START_WALK_NODE: str = "START_WALK"


STORY_NODES: [Node] = [
    Node(
        id=START_WALK_NODE,
        text=lambda dog: "What a beautiful day for a walk with " + dog.name + "!",
        choices=[
            Choice("0", lambda dog: "Yes!", [
                NodeLink(START_SQUIRREL, 1),
                NodeLink(START_ANUBIS, 7)
            ])
        ]
    )
]

STORY_NODES += ANUBIS_STORY_NODES
STORY_NODES += SQUIRREL_STORY_NODES


def build_story_graph() -> Dict[str, Node]:
    ret: Dict[str, Node] = {}
    for node in STORY_NODES:
        ret[node.id] = node
    return ret


STORY_GRAPH: Dict[str, Node] = build_story_graph()


def graph_sanity_check() -> bool:
    """
    Check:
    - choices have a different id
    - all link are pointing to a valid node
    :return:
    """
    if len(STORY_NODES) != len(STORY_GRAPH):
        raise Exception('Some node have duplicated id')
    for key, node in STORY_GRAPH.items():
        if node.choices_sanity_check():
            for choice in node.choices:
                for link in choice.links:
                    if STORY_GRAPH[link.node_id] is None:
                        return False
        else:
            return False
    return True

