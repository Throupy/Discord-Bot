"""Constant variables or static texts."""


class Consts:
    """Class containing values."""

    welcomeDMMessage = """
Welcome, {} to the server.
If you have any problems with bots or have any complains please
contact one of the server owners or administrators.
"""

    ytdl_format_options = {
        'format': 'bestaudio/best',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'
    }

    ffmpeg_options = {
        'options': '-vn'
    }

    channels = {
        'welcome': 563820994188541967,
        'announcements': 431933100122046470,
        'general': 563471753242738698,
        'cesspit': 424237366723477506,
        'computing': 406586420468252673
    }

    administrators = [403586211849175040, 547040529511088129]

    userInfo = {
        'joined_at': None,
        'nick': None,
        'status': None,
        'is_on_mobile': None,
        'mention': None,
        'top_role': None
    }

    spanishLetters = ['ñ', 'í', 'ó', 'é', 'á', '¿']
