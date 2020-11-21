from main.utils.story.effect import fitness_cookie_update, magic_bone_update, tennis_ball_update
from main.utils.story.node import Node, NodeLink, Choice

START_CAVERN: str = 'START_CAVERN'


CAVERN_STORY_NODES: [Node] = [
    Node(
        id="cavern_found",
        text=lambda dog: "As you're walking with " + dog.name + " you notice a cavern on the side of the road.",
        choices=[
            Choice("0", lambda dog: "Enter", [
                NodeLink("cavern_2_1", 1)
            ])
        ]
    ),
    Node(
        id="cavern_1_1",
        text=lambda dog: "You are in a cavern.",
        choices=[
            Choice("0", lambda dog: "Go North", [NodeLink("cavern_1_2", 1)]),
            Choice("1", lambda dog: "Go East", [NodeLink("cavern_2_1", 1)])
        ]
    ),
    Node(
        id="cavern_2_1",
        text=lambda dog: "You are in a cavern. A sign says 'Welcome, or not'.",
        choices=[
            Choice("0", lambda dog: "Go North", [NodeLink("cavern_2_2", 1)]),
            Choice("1", lambda dog: "Go East", [NodeLink("cavern_3_1", 1)]),
            Choice("2", lambda dog: "Go West", [NodeLink("cavern_1_1", 1)])
        ]
    ),
    Node(
        id="cavern_3_1",
        text=lambda dog: "You are in a cavern.",
        choices=[
            Choice("0", lambda dog: "Go North", [NodeLink("cavern_3_2", 1)]),
            Choice("1", lambda dog: "Go West", [NodeLink("cavern_2_1", 1)])
        ]
    ),
    Node(
        id="cavern_1_2",
        text=lambda dog: "You are in a cavern.",
        choices=[
            Choice("0", lambda dog: "Go North", [NodeLink("cavern_1_3", 1)]),
            Choice("1", lambda dog: "Go East", [NodeLink("cavern_2_2", 1)]),
            Choice("2", lambda dog: "Go South", [NodeLink("cavern_1_1", 1)]),
        ]
    ),
    Node(
        id="cavern_2_2",
        text=lambda dog: "You are in a cavern.",
        choices=[
            Choice("0", lambda dog: "Go North", [NodeLink("cavern_2_3", 1)]),
            Choice("1", lambda dog: "Go South", [NodeLink("cavern_2_1", 1)]),
            Choice("2", lambda dog: "Go West", [NodeLink("cavern_1_2", 1)]),
        ]
    ),
    Node(
        id="cavern_3_2",
        text=lambda dog: "You are in a cavern.",
        choices=[
            Choice("0", lambda dog: "Go North", [NodeLink("cavern_3_3", 1)]),
            Choice("1", lambda dog: "Go South", [NodeLink("cavern_3_1", 1)])
        ]
    ),
    Node(
        id="cavern_1_3",
        text=lambda dog: "You and " + dog.name + " keep walking."
    ),
    Node(
        id="cavern_2_3",
        text=lambda dog: "You and " + dog.name + " keep walking."
    ),
    Node(
        id="cavern_3_3",
        text=lambda dog: "You and " + dog.name + " keep walking."
    )
]
