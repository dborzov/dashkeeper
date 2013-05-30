import models
import re

SOURCE_PATH = "sub/"
TARGET = "mp.srt"


def srt2movie_lines(sub_text):
    """
    Clears off meta/non-text strings in the .str file format.
    Yields movie lines as a text.
     """
    out=[]
    for each_line in sub_text:
        if "-->" not in each_line:
            if not re.search(r'\w', each_line) is None:
                if re.search(r'^\d', each_line) is None:
                    out.append(each_line)
    return out


def fill_quotes():
    sub_text = open(SOURCE_PATH+TARGET, 'r').readlines()
    out = srt2movie_lines(sub_text)
    for n, line in enumerate(out):
        indices = [x for x in range(n-3,n+4) if  x >= 0 and x < len(out)]
        context = "<br> -".join([out[x] for x in indices])
        context = context.replace(line, '<b>'+line.split('\n')[0]+'</b>\n')
        new_entry = models.Quote()
        new_entry.line = line
        new_entry.context = context
        new_entry.movie = "Monty Python and the Holy Grail"
        new_entry.put()



def fill_quotes2():
    sub_text = open(SOURCE_PATH+TARGET, 'r').readlines()
    out = srt2movie_lines(sub_text)
    for n, line in enumerate(out):
        indices = [x for x in range(n-3,n+4) if  x >= 0 and x < len(out)]
        context = "<br> -".join([out[x] for x in indices])
        context = context.replace(line, '<b>'+line.split('\n')[0]+'</b>\n')
        new_entry = models.Quote()
        new_entry.line = line
        new_entry.context = context
        new_entry.movie = "Monty Python and the Holy Grail"
        new_entry.put()

