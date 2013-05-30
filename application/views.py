import json
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect

from flask_cache import Cache
import tramway.srt as srt
from application import app
from decorators import login_required, admin_required
from models import DictionaryWord, Mention, Quote
import re
from collections import Counter
import logging
import dbmaster
import os

SRT_DIR = './application/srt/'

# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)


def parser(word):
    """ individual word into array of dicts
    of quotes """
    dict_match = DictionaryWord.query(
            DictionaryWord.word == word).fetch()
    if dict_match:
        mentions = Mention.query(Mention.word == dict_match[0].key).fetch()
        yeild_text = []
        for mention in mentions:
            quote = mention.quote.get()
            quote_dict = {'line':quote.line,
                        'context': quote.context,
                        'movie':quote.movie
                        }
            yeild_text.append(quote_dict)
        return yeild_text
    else:
        return []


def prioritize(words):
    counters = {}
    for word in words:
        dict_match = DictionaryWord.query(
            DictionaryWord.word == word).fetch()
        if dict_match:
            mentions = Mention.query(Mention.word == dict_match[0].key).fetch()
            for mention in mentions:
                if mention.quote in counters:
                    counters[mention.quote] += 1
                else:
                    counters.update(dict([(mention.quote, 1)]))
    ordered = sorted(counters.items(), key=lambda x: x[1]).copy()
    logging.debug(" ====================================== ")
    logging.debug(ordered)
    logging.debug(" ====================================== ")
    return ordered


def retriever(keys):
    yeild_dicts = []

    for key in keys:
        quote = key.get()
        quote_dict = {'line':quote.line,'context':quote.context,'movie':quote.movie}
        yeild_dicts.append(quote_dict)
    return yeild_dicts


def say_hello():
    query = json.loads(request.data)
    words = tramway.texter.words_from_string(query["query"])
    #keys = parser(word)
    #out = retriever(keys)
    out = []
    for word in words:
        out += parser(word)
    if not out:
        out = [{'line': '', 'context': '<h1>:/</h1>Nothing found', 'movie': ''}]
    return json.dumps(out)


def manual_write():
    all_files = os.listdir(SRT_DIR)
    movie_titles = [{'title':title[:-4]} for title in all_files if title[-3:] == 'srt']

    for movie in movie_titles:
        movie['number'] = len (Quote.query( Quote.movie ==  movie['title']).fetch())
        filepath = SRT_DIR + movie['title'] + '.srt'
        content = open(filepath, 'rb').readlines()
        movie['total'] = len(srt.srt2movie_lines(content))

    return render_template('db_master.html', movies=movie_titles)


def tester_toast(title):
    filepath = SRT_DIR + title + '.srt'
    already_in = len (Quote.query( Quote.movie ==  title).fetch())
    lines = srt.srt2movie_lines(open(filepath, 'rb').readlines())
    indices = [i for i in range(already_in, already_in+20)]
    for i in indices:
        new_entry = Quote()
        new_entry.line_number = i
        new_entry.line = lines[i]
        context_indices = [x for x in range(i-3,i+4) if  x >= 0 and x < len(lines)]
        context = "<br> -".join([lines[x] for x in context_indices])
        context = context.replace(new_entry.line, '<b>'+new_entry.line+'</b>')
        new_entry.context = context
        new_entry.movie = title
        new_entry.put()
    return redirect(url_for('manual_write'))


def flush_toast(title):
    already_in = Quote.query(Quote.movie == title).fetch()
    for line in already_in:
        line.key.delete()
    return redirect(url_for('manual_write'))

def index_some():
    return 'The did is done'



def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

