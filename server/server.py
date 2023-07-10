# Made by Deltaion Lee (MCMi460) on Github
import flask, typing, sqlite3

app:flask.Flask = flask.Flask(__name__)

local:bool = False
port:str = '6677'

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

def get_categories() -> typing.List[Gift_Category]:
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
    categories = []

    response = flask.make_response(flask.render_template('pages/index.html', categories = get_categories()))
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
    return flask.send_file('gifts/%s/%s.webp' % (category, id))
#    CSS     #
@app.route('/css/style.css') # Logo
def css() -> flask.Response:
    return flask.send_file('static/css/style.css')

if __name__ == '__main__':
    if local:
        app.run(host = '0.0.0.0', port = port)
    else:
        import gevent.pywsgi
        server = gevent.pywsgi.WSGIServer(('0.0.0.0', port), app)
        server.serve_forever()
