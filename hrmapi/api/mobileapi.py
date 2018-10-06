from flask import Flask
from flask import jsonify
from flask_restful import Resource, Api, request
from flask_restful import reqparse
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'hrmdbuser'
app.config['MYSQL_DATABASE_PASSWORD'] = 'hrmdbuser'
app.config['MYSQL_DATABASE_DB'] = 'hrmdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

api = Api(app)


class AuthenticateEmployee(Resource):
    def post(self):
        try:
            # Parse the arguments

            parser = reqparse.RequestParser()
            parser.add_argument('first_name', type=str, help='Email address for Authentication')
            parser.add_argument('last_name', type=str, help='Password for Authentication')
            parser.add_argument('mobile_number', type=str, help='Password for Authentication')
            args = parser.parse_args()

            _empFirstName = args['first_name']
            _empLastName = args['last_name']
            _empMobileNumber = args['mobile_number']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_AuthenticateEmployee', (_empFirstName, _empLastName, _empMobileNumber))
            data = cursor.fetchall()
            print(data)
            print(data[0][2])

            if len(data) > 0:
                if str(data[0][1]) == _empMobileNumber and str(data[0][2]) == 'Active':
                    return {'status': 200, 'employee_id': str(data[0][0])}
                elif str(data[0][1]) == _empMobileNumber and str(data[0][2]) == 'Terminated':
                    return {'status': 200, 'message': 'Employee Not Active'}
                else:
                    return {'status': 100, 'message': 'Authentication Failure'}
            if len(data) == 0:
                return {'status': 202, 'message': 'Employee Details Mismatch'}

        except Exception as e:
            return {'error': str(e)}


class GetEmployeeDetails(Resource):
    def post(self):
        try:
            # Parse the arguments

            parser = reqparse.RequestParser()
            parser.add_argument('employee_id', type=str, help='Employee Id For Verification')
            args = parser.parse_args()

            _empEmployeeId = args['employee_id']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_EmployeeDetails', (_empEmployeeId,))
            data = cursor.fetchall()

            if len(data) > 0:
                items_list = []
                for item in data:
                    i = {
                        'employee_id': item[0],
                        'first_name': item[1],
                        'middle_name': item[2],
                        'last_name': item[3],
                        'nationality': item[4],
                        'dob': item[5],
                        'gender': item[6],
                        'city': item[7],
                        'marital_status': item[8],
                        'job_title': item[9],
                        'mobile_phone': item[10],
                        'joined_date': item[11],
                        'status': item[12]
                    }
                items_list.append(i)
                return {'StatusCode': '200', 'Items': items_list}

            if len(data) == 0:
                return {'status': 202, 'message': 'Employee Details Not Found'}

        except Exception as e:
            return {'error': str(e)}


class GetAllEntries(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str)
            args = parser.parse_args()

            _userId = args['id']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_GetAllAttendance', (_userId,))
            data = cursor.fetchall()

            items_list = []
            for item in data:
                i = {
                    'in_date': item[0],
                    'out_date': item[1],
                    'note': item[2]
                }
                items_list.append(i)

            return {'StatusCode': '200', 'Items': items_list}

        except Exception as e:
            return {'error': str(e)}


class AddItem(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str)
            parser.add_argument('item', type=str)
            args = parser.parse_args()

            _userId = args['id']
            _item = args['item']

            print _userId

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_AddItems', (_userId, _item))
            data = cursor.fetchall()

            conn.commit()
            return {'StatusCode': '200', 'Message': 'Success'}

        except Exception as e:
            return {'error': str(e)}


class CheckIn(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('employee', type=str, help='Employee ID Required')
            parser.add_argument('in_time', type=str, help='Employee In Time Required')
            parser.add_argument('note', type=str, help='Employee Note')
            args = parser.parse_args()

            _employeeId = args['employee']
            _empInTime = args['in_time']
            _empNote = args['note']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spAttendance', (_employeeId, _empInTime, _empNote))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'StatusCode': '200', 'Message': 'Employee Checked In'}
            else:
                return {'StatusCode': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}


class CheckOut(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('employee', type=str, help='Employee ID Required')
            parser.add_argument('in_time', type=str, help='Employee In Time Required')
            parser.add_argument('out_time', type=str, help='Employee Out Time Required')
            parser.add_argument('note', type=str, help='Employee Note')
            args = parser.parse_args()

            _employeeId = args['employee']
            _empInTime = args['in_time']
            _empOutTime = args['out_time']
            _empNote = args['note']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spAttendanceOut', (_employeeId, _empInTime, _empOutTime, _empNote))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'StatusCode': '200', 'Message': 'Employee Checked Out'}
            else:
                return {'StatusCode': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}


# api.add_resource(CheckIn, '/CheckIn')  # WORKING
api.add_resource(CheckOut, '/CheckOut')  # WORKING
api.add_resource(GetAllEntries, '/GetAllEntries')  # WORKING
api.add_resource(AuthenticateEmployee, '/AuthenticateEmployee')  # WORKING
api.add_resource(GetEmployeeDetails, '/EmployeeDetails')  # WORKING
api.add_resource(AddItem, '/AddItem')


@app.route('/')
def index():
    return jsonify("demo")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print(request.method)
        user = request.get_json()
        print(user)
        return jsonify('success')
    else:
        user = request.args.get('nm')
        print(user)
        return jsonify("deepankar")


if __name__ == '__main__':
    app.run(debug=True)
