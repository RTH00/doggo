from django.test import TestCase

# Create your tests here.
from .subtests.submodels.account import *
from .subtests.submodels.story import *
from .subtests.submodels.dog import *
from .subtests.submodels.dog_updater import *
from .subtests.submodels.breed import *
from .subtests.submodels.events.dog_event import *
from .subtests.submodels.events.dog_action_event import *
from .subtests.subviews.account import *
from .subtests.subviews.home import *
from .subtests.subviews.dog import *
from .subtests.utils.story.node import *
from .subtests.utils.story.graph import *
