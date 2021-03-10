# appointment-api


## Launching the API
To launch the API locally run the following commands. This assumes that you have Docker installed locally and port 5000 available.
These commands should be run in the home directory and will run the API on port 5000. 

- `docker build -t appointment-api . `
- `docker `

## Using the API

### Endpoints

_Appointments_

- `/appointments` with all three required parameters of `date`, `time` and `user_id`.
- Accepts only PUT requests
- Dates should be input in the form '2021-03-10'
- Time should be input as '12:30' with times after noon as '14:30' for 2:30 PM. Times must be on the hour or the half hour
- User IDs are all integers
- Example query:
  - `/appointments?date=2021-03-01&time=15:00&user_id=1`
- Return body will include the user id and a list of dictionaries representing all the appointments
- A successful appointment will return a 200 with the scheduled date and time, the 
  
_Users_
- `/user` will only accept `user_id` as a parameter and the `user_id` must be provided
- `user_id` must be an integer 
- Example call:
  - `/user?user_id=1`


## TODOs
- Write tests for validation functions
- Write standalone test suite with function calls, I used the ones below with Postman and visually confirmed the results
  - `http://127.0.0.1:5000/appointments?user_id=1&time=12:30&date=2021-03-01` (POST)
  - `http://127.0.0.1:5000/appointments?user_id=1&time=12:30&date=2021-03-02` (POST)
  - `http://127.0.0.1:5000/appointments?user_id=1&time=11:30&date=2021-03-01`  (POST) (should fail)
  - `http://127.0.0.1:5000/appointments?user_id=1&time=11:30&date=1`  (POST) (should fail)
  - `http://127.0.0.1:5000/appointments?user_id=1&time=11:31&date=2021-03-10` (POST) (should fail)
  - `http://127.0.0.1:5000/user?user_id=1` (GET) 
  - `http://127.0.0.1:5000/user?user_id=2` (GET) (should fail)