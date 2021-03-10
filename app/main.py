from flask_api import status
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

DATE_PARAM = 'date'
TIME_PARAM = 'time'
USER_PARAM = 'user_id'
ALLOWED_APPOINTMENT_PARAMETERS = [DATE_PARAM, TIME_PARAM, USER_PARAM]
ALLOWED_DATE_FORMAT = '%Y-%m-%d'
ALLOWED_TIME_FORMAT = '%H:%M'
ALLOWED_MINUTES = [0, 30]

USER_DICT = {}


# Validation scripts
def is_int(potential_int):
    """
    Checks if the passed parameter is an integer
    :param potential_int:
    :return: boolean
    """
    try:
        float(potential_int).is_integer() and float(potential_int) > 0
        return True
    except ValueError:
        return False


def is_valid_date(potential_date, allowed_format=ALLOWED_DATE_FORMAT):
    """
    Checks if the passed string is a date
    :param potential_date:
    :param allowed_format: Format for datetime
    :return: date object
    """
    try:
        datetime.strptime(potential_date, allowed_format)
        return True
    except ValueError:
        return False


def is_valid_time(potential_time: str, allowed_form: str = ALLOWED_TIME_FORMAT):
    """
    Checks that the input time is valid and that it is either on the hour or the half hour
    :param potential_time: time string passed from user
    :param allowed_form: Allowed datetime format
    :return: boolean
    """
    try:
        time = datetime.strptime(potential_time, allowed_form).time()
        minutes = time.minute
        if minutes in ALLOWED_MINUTES:
            return True
        else:
            return False
    except ValueError:
        return False


class Appointment:
    """
    Class representing the Appointment with a call for a JSON representation
    """

    def __init__(self, date, time, user):
        self._date = date
        self._time = time
        self._user = user

    def get_appointment_json(self):
        """
        Returns dict representation of the appointment without the
        :return:
        """
        appt_dict = {DATE_PARAM: self._date,
                     TIME_PARAM: self._time,
                     USER_PARAM: self._user}
        return appt_dict


class User:
    """
    User class with a dictionary keyed with dates to store appointments
    """
    
    def __init__(self, user_id):
        self._user_id = user_id
        self.appointment_dict = {}

    def add_appointment(self, date, time):

        # Assume that date and time have already been checked and rounded

        # If date has already been added return False so handler can send the appropriate error message

        if date in self.appointment_dict:
            return False
        # Otherwise add the appointment
        else:
            new_appointment = Appointment(date=date, time=time, user=self._user_id)
            self.appointment_dict[date] = new_appointment
            return True

    def get_user_info(self):
        """
        Creates a JSON object with all data about the user
        :return:
        """
        ## TODO
        # Order appointments by time
        appointment_json_list = [appt.get_appointment_json() for appt in self.appointment_dict.values()]
        return_dict = {USER_PARAM: self._user_id,
                       'appointment_list': appointment_json_list}

        return jsonify(return_dict)

## TODO
# Add more helpful error methods for calls to the root and unused methods

@app.route('/user', methods=['GET'])
def get_user():

    # Get user id from requests
    request_args = request.args
    if set([USER_PARAM]) != set(request_args.keys()):
        error_message = {'message': f'{USER_PARAM} is a required parameter and no other parameters may be added.'}
        return error_message, status.HTTP_400_BAD_REQUEST
    user_id = request_args.get(USER_PARAM)

    # Either get the user data as it is stored or return an error that the user was not found
    if user_id in USER_DICT:
        user_object = USER_DICT[user_id]
        user_json = user_object.get_user_info()
        return user_json, status.HTTP_200_OK
    else:
        not_found_message = {'message': f"user {user_id} not found"}
        return not_found_message, status.HTTP_404_NOT_FOUND


@app.route('/appointments', methods=['POST'])
def process_appointment_call():
    request_args = request.args

    # Check that appointment date, appointment time and user ID are all included in the requests
    if set(request_args.keys()) != set(ALLOWED_APPOINTMENT_PARAMETERS):
        bad_param_message = {'message': f'{",".join(ALLOWED_APPOINTMENT_PARAMETERS)} are all required and no other parameters are allowed '}
        return bad_param_message, status.HTTP_400_BAD_REQUEST
    date = request_args.get(DATE_PARAM)
    time = request_args.get(TIME_PARAM)
    user_id = request_args.get(USER_PARAM)

    ## TODO
    # Refactor validations to a separate function
    # Validate parameters
    is_allowed_date = is_valid_date(date)
    if not is_allowed_date:
        date_message = {'message':f'Date must be in form 2021-03-10, {date} was passed'}
        return date_message, status.HTTP_400_BAD_REQUEST

    is_allowed_time = is_valid_time(time)
    if not is_allowed_time:
        time_message = {'message':f'Time must be in form 13:30 and needs to be either on the hour or the half hour. {time} was passed'}
        return time_message, status.HTTP_400_BAD_REQUEST

    is_allowed_id = is_int(user_id)
    if not is_allowed_id:
        user_message = {'message': f'User ID must be an integer, {user_id} was passed'}
        return user_message, status.HTTP_200_OK

    # Create a user if one does not already exist
    if user_id in USER_DICT:
        user = USER_DICT[user_id]
    else:
        user = User(user_id=user_id)
        USER_DICT[user_id] = user

    # Attempt to create a new appointment, if it is successful, return the information, if it is not, return an error.
    is_successful_appointment = user.add_appointment(date=date, time=time)
    if is_successful_appointment:
        success_message = {'message': f'appointment created on {date} at {time}'}
        return success_message, status.HTTP_201_CREATED
    else:
        duplicate_appointment_message = {'message': f'invalid date {date}, user id {user_id} already has an appointment on that date'}
        return duplicate_appointment_message, status.HTTP_409_CONFLICT


if __name__ == "__main__":
    # Ensure app is running locally and is on the docker port
    app.run(host='0.0.0.0', debug=True, port=80)
