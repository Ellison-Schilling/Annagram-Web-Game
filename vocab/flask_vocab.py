"""
Flask web site with vocabulary matching game
(identify vocabulary words that can be made
from a scrambled string)
"""

import flask
from flask import request
import logging
import sys

# Our modules
from src.letterbag import LetterBag
from src.vocab import Vocab
from src.jumble import jumbled
import src.config as config


###
# Globals
###
app = flask.Flask(__name__)

CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY  # Should allow using session variables

#
# One shared 'Vocab' object, read-only after initialization,
# shared by all threads and instances.  Otherwise we would have to
# store it in the browser and transmit it on each request/response cycle,
# or else read it from the file on each request/responce cycle,
# neither of which would be suitable for responding keystroke by keystroke.

WORDS = Vocab(CONFIG.VOCAB)
SEED = CONFIG.SEED
try:
    SEED = int(SEED)
except ValueError:
    SEED = None


###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    """The main page of the application"""
    flask.g.vocab = WORDS.as_list()
    flask.session["target_count"] = min(
        len(flask.g.vocab), CONFIG.SUCCESS_AT_COUNT)
    flask.session["jumble"] = jumbled(
        flask.g.vocab, flask.session["target_count"], seed=None if not SEED or SEED < 0 else SEED)
    flask.session["matches"] = []
    app.logger.debug("Session variables have been set")
    assert flask.session["matches"] == []
    assert flask.session["target_count"] > 0
    app.logger.debug("At least one seems to be set correctly")
    return flask.render_template('vocab.html')


@app.route("/success")
def success():
    """ 
    The referenced route if the player has completed the minimum words needed 
    """
    return flask.render_template('success.html')


#######################
# Form handler.
#   You'll need to change this to a
#   a JSON request handler
#######################

@app.route("/_check")
def check():
    """
    User has submitted the form with a word ('attempt')
    that should be formed from the jumble and on the
    vocabulary list.  We respond depending on whether
    the word is on the vocab list (therefore correctly spelled),
    made only from the jumble letters, and not a word they
    already found.
    MAKE IT A POST REQUEST
    """
    
    text = request.args.get("text", type=str)
   
    # The data we need, from form and from cookie
    jumble = flask.session["jumble"]
    matches = flask.session.get("matches", [])  # Default to empty list
 
    # Is it good?
    in_jumble = LetterBag(jumble).contains(text)
    matched = WORDS.has(text)

    # Respond appropriately
    rslt = { "key" : '' }

    if matched and in_jumble and not (text in matches): # Word typed was correct
        matches.append(text)    # Add word to matches
        flask.session["matches"] = matches     
        if len(matches) >= flask.session["target_count"]:   # Check if they have completed all the needed words
            rslt["key"] = '#'   # Send flag if we have completed the correct number of words
        else:
            rslt["key"] = text + ' ' # Otherwise we simply want to add the word
    elif matched and not in_jumble:     # See if the word is a valid word, but not capable of being made with given letters
        rslt["key"] = '!'   # Send flag for word not in jumble
    else:   # Otherwise the word was not valid
        rslt["key"] = '?'   # Send flag for invalid word
    return flask.jsonify(result = rslt)
    
###############
# AJAX request handlers
#   These return JSON, rather than rendering pages.
###############

@app.route("/_example")
def example():
    """
    Example ajax request handler
    """
    app.logger.debug("Got a JSON request")
    rslt = {"key": "value"}
    return flask.jsonify(result=rslt)


#################
# Functions used within the templates
#################

@app.template_filter('filt')
def format_filt(something):
    """
    Example of a filter that can be used within
    the Jinja2 code
    """
    return "Not what you asked for"

###################
#   Error handlers
###################


@app.errorhandler(404)
def error_404(e):
    app.logger.warning("++ 404 error: {}".format(e))
    return flask.render_template('404.html'), 404


@app.errorhandler(500)
def error_500(e):
    app.logger.warning("++ 500 error: {}".format(e))
    assert not True  # I want to invoke the debugger
    return flask.render_template('500.html'), 500


@app.errorhandler(403)
def error_403(e):
    app.logger.warning("++ 403 error: {}".format(e))
    return flask.render_template('403.html'), 403


#############

if __name__ == "__main__":
    if CONFIG.DEBUG:
        app.debug = True
        app.logger.setLevel(logging.DEBUG)
        app.logger.info(
            "Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0", debug=CONFIG.DEBUG)
