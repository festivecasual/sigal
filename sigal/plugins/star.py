# -*- coding: utf-8 -*-

"""Plugin to process only photos that are starred in Picasa (using .picasa.ini)."""

import logging
import os.path
import configparser
from collections import defaultdict

from sigal import signals

logger = logging.getLogger(__name__)


def filter_stars(album):
    logger.debug('Filtering starred photos for album: %r', album.name)

    ini = configparser.ConfigParser()
    path = os.path.join(album.settings['source'], album.path, '.picasa.ini')
    ini.read(path)
    starred = [name for (name, s) in ini.items() if s.get('star')]
    logger.debug('%d starred photo(s) identified in .picasa.ini', len(starred))

    # Will contain the filtered set of medias
    result = []

    # Cycle through all originally-identified medias
    for media in album.medias:
        if not media.filename in starred:
            # This media will not be in the final list, so decrement the count
            album.medias_count[media.type] -= 1
        else:
            # Since this media will survive, copy it to the results list
            result.append(media)
    album.medias = result

def register(settings):
    signals.album_initialized.connect(filter_stars)
