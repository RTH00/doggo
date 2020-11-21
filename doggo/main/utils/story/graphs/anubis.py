from typing import Dict, List

from main.utils.story.effect import fitness_cookie_update, magic_bone_update, tennis_ball_update
from main.utils.story.node import Node, NodeLink, Choice

START_ANUBIS: str = 'START_ANUBIS'

GOOD_ANSWERS: List[NodeLink] = [
    NodeLink('GOOD_ANSWER_FITNESS_COOKIE', 10),
    NodeLink('GOOD_ANSWER_TENNIS_BALL', 5),
    NodeLink('GOOD_ANSWER_MAGIC_BONE', 1)
]
BAD_ANSWERS: List[NodeLink] = [
    NodeLink('BAD_ANSWER_NOTHING', 31),
    NodeLink('BAD_ANSWER_FITNESS_COOKIE', 20),
    NodeLink('BAD_ANSWER_TENNIS_BALL', 10),
    NodeLink('BAD_ANSWER_MAGIC_BONE', 1)
]


ANUBIS_STORY_NODES: [Node] = [
    Node(
        id=START_ANUBIS,
        text=lambda dog: 'You and ' + dog.name + ' are walking on the sidewalk. Suddenly, a bright light appears '
                         'in the sky. The ancient Egyptian god Anubis (with a dog head) slowly descends from the sky. '
                         'He asks you "Are you ready for a riddle ?"',
        choices=[
            Choice("0", lambda dog: "Yes!", [
                NodeLink("riddle_1", 1),
                NodeLink("riddle_2", 1),
                NodeLink("riddle_3", 1),
                NodeLink("riddle_4", 1),
                NodeLink("riddle_5", 1),
                NodeLink("riddle_6", 1),
                NodeLink("riddle_7", 1),
                NodeLink("riddle_8", 1),
                NodeLink("riddle_9", 1),
                NodeLink("riddle_10", 1)
            ])
        ]
    ),
    # good answers
    Node(
        id='GOOD_ANSWER_FITNESS_COOKIE',
        text=lambda dog: 'That\'s right! Here, get a fitness cookie!',
        effect=lambda account, dog: fitness_cookie_update(account, 1)
    ),
    Node(
        id='GOOD_ANSWER_TENNIS_BALL',
        text=lambda dog: 'That\'s right! ' + dog.name + ' deserves another tennis ball, take one!',
        effect=lambda account, dog: tennis_ball_update(account, 1)
    ),
    Node(
        id='GOOD_ANSWER_MAGIC_BONE',
        text=lambda dog: "That\'s right! I'm feeling generous today! Have a magic bone!",
        effect=lambda account, dog: magic_bone_update(account, 1)
    ),
    # bad answers
    Node(
        id='BAD_ANSWER_NOTHING',
        text=lambda dog: "Wrong! I'm disappointed...",
    ),
    Node(
        id='BAD_ANSWER_FITNESS_COOKIE',
        text=lambda dog: "Wrong! I'm taking one of your fitness cookies!",
        effect=lambda account, dog: fitness_cookie_update(account, -1)
    ),
    Node(
        id='BAD_ANSWER_TENNIS_BALL',
        text=lambda dog: "Wrong! I'm taking one of your tennis ball!",
        effect=lambda account, dog: tennis_ball_update(account, -1)
    ),
    Node(
        id='BAD_ANSWER_MAGIC_BONE',
        text=lambda dog: "Wrong! You made Anubis very angry, I'm taking one of your magic bones!",
        effect=lambda account, dog: magic_bone_update(account, -1)
    ),
    # riddles
    Node(
        id="riddle_1",
        text=lambda dog: "Why aren't dogs good dancers?",
        choices=[
            Choice("0", lambda dog: "Because they have two left feet!", GOOD_ANSWERS),
            Choice("1", lambda dog: "Because ...", BAD_ANSWERS),
            Choice("2", lambda dog: "Because dogs cannot dance.", BAD_ANSWERS),
        ]
    ),
    Node(
        id="riddle_2",
        text=lambda dog: "Who's the best?",
        choices=[
            Choice("0", lambda dog: dog.name + "!", GOOD_ANSWERS),
            Choice("1", lambda dog: "Me", BAD_ANSWERS)
        ]
    ),
    Node(
        id="riddle_3",
        text=lambda dog: "Who's the Egysptian god with a dog head?",
        choices=[
            Choice("0", lambda dog: "Anubis", GOOD_ANSWERS),
            Choice("1", lambda dog: "Osiris", BAD_ANSWERS),
            Choice("2", lambda dog: "Hathor", BAD_ANSWERS),
            Choice("3", lambda dog: "Seth", BAD_ANSWERS),
        ]
    ),
    Node(
        id="riddle_4",
        text=lambda dog: "Which of this dog is a symbol of loyalty?",
        choices=[
            Choice("0", lambda dog: "Hachikō", GOOD_ANSWERS),
            Choice("1", lambda dog: "Smoky", BAD_ANSWERS),
            Choice("2", lambda dog: "Bunkō", BAD_ANSWERS),
            Choice("3", lambda dog: "Rin Tin Tin", BAD_ANSWERS),
        ]
    ),
    Node(
        id="riddle_5",
        text=lambda dog: "Which of this 'German' dog breeds doesn't exist?",
        choices=[
            Choice("0", lambda dog: "German Bulldog", GOOD_ANSWERS),
            Choice("1", lambda dog: "German Spitz", BAD_ANSWERS),
            Choice("2", lambda dog: "German Spaniel", BAD_ANSWERS),
            Choice("3", lambda dog: "German Shepherd", BAD_ANSWERS),
        ]
    ),
    Node(
        id="riddle_6",
        text=lambda dog: "What is " + dog.name + "'s favorite band?",
        choices=[
            Choice("0", lambda dog: "The Beagles!", GOOD_ANSWERS),
            Choice("1", lambda dog: "What?", BAD_ANSWERS),
            Choice("2", lambda dog: "Doggo something?", BAD_ANSWERS),
            Choice("3", lambda dog: "...", BAD_ANSWERS),
        ]
    ),
    Node(
        id="riddle_7",
        text=lambda dog: "What is the job of a dog with a camera?",
        choices=[
            Choice("0", lambda dog: "pup-arazzi", GOOD_ANSWERS),
            Choice("1", lambda dog: "???", BAD_ANSWERS),
            Choice("2", lambda dog: "bone fetcher", BAD_ANSWERS),
            Choice("3", lambda dog: "...", BAD_ANSWERS),
        ]
    ),
    Node(
        id="riddle_8",
        text=lambda dog: "What do you call a magic dog?",
        choices=[
            Choice("0", lambda dog: "A Labracadabrador!", GOOD_ANSWERS),
            Choice("1", lambda dog: "A magic dog!", BAD_ANSWERS),
            Choice("2", lambda dog: "A magic bone!", BAD_ANSWERS),
            Choice("3", lambda dog: "wait.. what?", BAD_ANSWERS),
        ]
    ),
    Node(
        id="riddle_9",
        text=lambda dog: "What happen when " + dog.name + " go to a flea circus?",
        choices=[
            Choice("0", lambda dog: dog.name + " steals the show!", GOOD_ANSWERS),
            Choice("1", lambda dog: "It's a bad idea", BAD_ANSWERS),
            Choice("2", lambda dog: "oh gosh...", BAD_ANSWERS),
            Choice("3", lambda dog: "what?", BAD_ANSWERS),
        ]
    ),
    Node(
        id="riddle_10",
        text=lambda dog: "Woof, woof, woof?",
        choices=[
            Choice("0", lambda dog: "Woof, woof, woof, woof.", GOOD_ANSWERS),
            Choice("1", lambda dog: "Woof?", GOOD_ANSWERS),
            Choice("2", lambda dog: "Woof, woof...?", GOOD_ANSWERS),
            Choice("3", lambda dog: "Woof", GOOD_ANSWERS),
        ]
    )
]
