from flask import Flask, render_template, request
from flask_restful import reqparse, Api, Resource, abort
import redis

app = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379, db=0)



# User Interface Section-----------------------------------------------------------
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/userdetail', methods=['GET', 'POST'])
def user_detail():
    if request.method == 'GET':
        return render_template('add_user.html')
    elif request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        city = request.form['city']
        problem = request.form['problem']

        r.set(name+':name', name)
        r.set(name+':year', year)
        r.set(name+':city', city)
        r.set(name+':problem', problem)

        if request.form['name'] and request.form['year'] and request.form['city'] and request.form['problem']:
            message = 'User added successfully.'
            return render_template('home.html', message=message)
        else:
            return render_template('add_user.html', message='All field are required!!!')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    elif request.method == 'POST':
        name = request.form['search']
        if name:
            name1 = r.get(name+':name').decode()
            year1 = r.get(name + ':year').decode()
            city1 = r.get(name + ':city').decode()
            problem1 = r.get(name + ':problem').decode()
            return render_template('user_detail.html', name=name1, year=year1, city=city1, problem=problem1)
        else:
            return render_template('search.html', message='Field are required!!!')




@app.route('/error')
def error():
    return render_template('no_user.html')

# Rest Api section-----------------------------------------------------------------


api = Api(app)

r = redis.StrictRedis(host='localhost', port=6379, db=0)

name1 = 'Vikram'
name = r.get(name1+':name').decode()
year = r.get(name1+':year').decode()
city = r.get(name1+':city').decode()
problem = r.get(name1+':problem').decode()


languages = {
    'name': {'name': name},
    'year': {'year': year},
    'city': {'city': city},
    'problem': {'problem': problem}
}



parser = reqparse.RequestParser()
parser.add_argument('work')

def abort_if_language_does_not_exists(language_id):
    if language_id not in languages:
        abort(404, message='Language {} Does not exists'.format(language_id))

class Language(Resource):
    def get(self, language_id):
        abort_if_language_does_not_exists(language_id)
        return languages[language_id]

    def delete(self, language_id):
        abort_if_language_does_not_exists(language_id)
        del languages[language_id]
        return '', 204

    def put(self, language_id):
        args = parser.parse_args()
        work = {'work': args['work']}
        languages[language_id] = work
        return work, 201

class LanguageList(Resource):
    def get(self):
        return languages

    def post(self):
        args = parser.parse_args()
        language_id = int(max(languages.keys()).lstrip('language')) + 1
        language_id = 'language%i' % language_id
        languages[language_id] = {'work': args['work']}
        return languages[language_id], 201

api.add_resource(LanguageList, '/language')
api.add_resource(Language, '/languages/<language_id>')


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
