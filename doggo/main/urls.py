from django.urls import path

from . import views
from .middleware.cookie_consent import COOKIE_CONSENT_PATH, PRIVACY_POLICY_PATH, TERMS_AND_CONDITIONS_PATH, CONTACT_PATH
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.render_index, name='index'),
    path('create_dog', views.render_create_dog, name='create_dog'),
    path(COOKIE_CONSENT_PATH, views.cookie_consent, name='cookie_consent'),
    path('home', views.render_home, name='home'),
    path('account', views.render_account, name='account'),
    path('change_account/<str:account_secret_id>', views.render_change_account, name='change_account'),
    path('delete_account', views.render_delete_account, name='delete_account'),
    path('dogs', views.render_dogs, name='dogs'),
    # dog actions
    path('dog/<str:id>', views.render_dog, name='dog'),
    path('feed_dog/<str:id>', views.render_feed_dog, name='feed_dog'),
    path('walk_dog/<str:id>', views.render_walk_dog, name='walk_dog'),
    path('play_dog/<str:id>', views.render_play_dog, name='play_dog'),
    path('use_magic_bone/<str:id>', views.render_use_magic_bone, name='use_magic_bone'),
    path('use_fitness_cookie/<str:id>', views.render_use_fitness_cookie, name='use_fitness_cookie'),
    path('use_tennis_ball/<str:id>', views.render_use_tennis_ball, name='use_tennis_ball'),
    # story mode
    path('story_choice/<str:dog_id>/<str:choice_id>', views.render_story_choice, name='story_choice'),
    path('cancel_story/<str:dog_id>', views.render_cancel_story, name='cancel_story'),
    # legal
    path(PRIVACY_POLICY_PATH, views.render_privacy_policy, name='privacy_policy'),
    path(TERMS_AND_CONDITIONS_PATH, views.render_terms_and_conditions, name='terms_and_conditions'),
    path(CONTACT_PATH, views.render_contact, name='contact')
]

urlpatterns += staticfiles_urlpatterns()
