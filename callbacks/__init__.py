from .artist import callback_artist
from .song import callback_song
from .score import callback_score
from .record import callback_record


def register_callbacks(dash_app1):

    callback_artist(dash_app1)

    callback_song(dash_app1)

    callback_score(dash_app1)

    callback_record(dash_app1)

        







