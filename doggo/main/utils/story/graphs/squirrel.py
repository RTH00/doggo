from main.utils.story.effect import fitness_cookie_update, magic_bone_update, tennis_ball_update
from main.utils.story.node import Node, NodeLink, Choice

START_SQUIRREL: str = 'START_SQUIRREL'


SQUIRREL_STORY_NODES: [Node] = [
    Node(
        id=START_SQUIRREL,
        text=lambda dog: dog.name + " spot a squirrel in a tree and start barking!",
        choices=[
            Choice("0", lambda dog: "Woof wooOOoof wooof!!!", [
                NodeLink("squirrel_drop_cookie", 3),
                NodeLink("squirrel_steal_cookie", 1)
            ]),
            Choice("1", lambda dog: "Stop barking!", [
                NodeLink("keep_walking", 9),
                NodeLink("squirrel_steal_cookie", 1)
            ])
        ]
    ),
    Node(
        id="squirrel_drop_cookie",
        text=lambda dog: "The squirrel is afraid by " + dog.name + " and drop a cookie!",
        effect=lambda account, dog: fitness_cookie_update(account, 1)
    ),
    Node(
        id="squirrel_steal_cookie",
        text=lambda dog: "Oh no! It was a diversion! Meanwhile another squirrel stole a cookie from your home!",
        effect=lambda account, dog: fitness_cookie_update(account, -1)
    ),
    Node(
        id="keep_walking",
        text=lambda dog: "You and " + dog.name + " keep walking."
    )
]
