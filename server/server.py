# Made by Deltaion Lee (MCMi460) on Github
import flask, typing, sqlite3, os, datetime, time, werkzeug.security

app:flask.Flask = flask.Flask(__name__)

local:bool = False
port:int = 6677

###############
### Utility ###
###############
class Gift_Category:
    def __init__(self, **kwargs:dict) -> None:
        self.key = kwargs.get('key')
        self.name = kwargs.get('name')
        self.image_url = kwargs.get('image_url')
        self.description = kwargs.get('description')
        self.key_color = kwargs.get('key_color')
        self.gifts = kwargs.get('gifts')

class Gift:
    def __init__(self, **kwargs:dict) -> None:
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.tags = kwargs.get('tags')
        self.meta = kwargs.get('meta')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
        self.thumbnail_url = kwargs.get('thumbnail_url')
        self.points = kwargs.get('points')
        self.begins_at = kwargs.get('begins_at')
        self.ends_at = kwargs.get('ends_at')

def get_options() -> list:
    with sqlite3.connect('gifts/category.db') as con: # Access database for category
        cursor = con.cursor()
        cursor.execute('SELECT * FROM categories')
        categories:Gift_Category = [ Gift_Category(
            key = category[0],
            name = category[1],
            image_url = category[2],
            description = category[3],
            key_color = category[4],
        ) for category in cursor.fetchall() ]
    return categories

def get_categories(key:str = None) -> typing.List[Gift_Category]:
    categories = get_options()
    if key:
        categories = [ category for category in categories if category.key == key ]
    for i in range(len(categories)):
        key = categories[i].key
        with sqlite3.connect('gifts/%s/%s.db' % (key, key)) as con: # Access database for category
            cursor = con.cursor()
            cursor.execute('SELECT * FROM gifts')
            categories[i].gifts = [ Gift(
                id = gift[0],
                name = gift[1],
                tags = gift[2],
                meta = gift[3],
                created_at = gift[4],
                updated_at = gift[5],
                thumbnail_url = gift[6],
                points = gift[7],
                begins_at = gift[8],
                ends_at = gift[9],
            ) for gift in cursor.fetchall() ]
    return categories

#############
### Pages ###
#############
@app.route('/') # Index
def index() -> flask.Response:
    last = None
    if os.path.isfile('backend.txt'):
        with open('backend.txt', 'r') as file:
            last = str(datetime.timedelta(seconds = int(time.time() - float(file.read())))).split(':')
    last = last[0] + 'h, ' + last[1] + 'm, ' + last[2] + 's ago'

    response = flask.make_response(flask.render_template('pages/index.html', categories = [], options = get_options(), last = last))
    return response

@app.route('/key/<string:key>') # Category
def category(key:str) -> flask.Response:
    last = None
    if os.path.isfile('backend.txt'):
        with open('backend.txt', 'r') as file:
            last = str(datetime.timedelta(seconds = int(time.time() - float(file.read())))).split(':')
    last = last[0] + 'h, ' + last[1] + 'm, ' + last[2] + 's ago'

    response = flask.make_response(flask.render_template('pages/index.html', categories = get_categories(key), options = get_options(), last = last))
    return response

##############
### Static ###
##############
#   Assets   #
@app.route('/favicon.ico') # Favicon
def favicon() -> flask.Response:
    return flask.send_file('static/assets/favicon.ico')

@app.route('/logo.png') # Logo
def logo() -> flask.Response:
    return flask.send_file('static/assets/transparent.png')

@app.route('/gifts/<string:category>/<string:id>.webp') # Image
def gifts_image(category:str, id:str) -> flask.Response:
    return flask.send_from_directory(werkzeug.security.safe_join('gifts', category), id + '.webp')
#    CSS     #
@app.route('/css/style.css') # Stylesheet
def css() -> flask.Response:
    return flask.send_file('static/css/style.css')
#    JS     #
@app.route('/js/script.js') # Scripts
def js() -> flask.Response:
    return flask.send_file('static/js/script.js')

if __name__ == '__main__':
    if local:
        app.run(host = '0.0.0.0', port = port)
    else:
        import gevent.pywsgi
        server = gevent.pywsgi.WSGIServer(('0.0.0.0', port), app)
        server.serve_forever()
