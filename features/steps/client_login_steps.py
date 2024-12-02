import csv
import time
from behave import given, when, then
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://127.0.0.1:5000"
MAX_CONCURRENT_REQUESTS = 10  # Simulate 10 concurrent requests at a time
login_results = []  # Store login results for in-memory checks


@given('the login endpoint "{endpoint}"')
def step_given_login_endpoint(context, endpoint):
    context.endpoint = f"{BASE_URL}{endpoint}"


@given('the user data file "{file}"')
def step_given_user_data_file(context, file):
    context.user_data_file = file
    # Read the user data from the file
    context.users = []
    try:
        with open(file, "r") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            context.users = [row for row in reader]
    except FileNotFoundError:
        raise Exception(f"File {file} not found. Run the registration test first.")


@when('I send login requests with total load {total_load:d} over a ramp-up time of {rampup_time:d} seconds')
def step_when_send_login_requests(context, total_load, rampup_time):
    def send_login_request(user):
        start_time = time.time()  # Start timer
        payload = {
            "userName": user[0],  # userName from CSV
            "email": user[1],     # email from CSV
            "password": user[2],  # password from CSV
        }
        response = requests.post(context.endpoint, data=payload)
        end_time = time.time()  # End timer

        response_time = (end_time - start_time) * 1000  # Response time in milliseconds
        status_code = response.status_code

        # Log response metrics
        with open("login_test_results.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                payload["userName"],
                status_code,
                response_time,
                "Success" if status_code == 200 and "token" in response.text else "Failed"
            ])

        return status_code

    # Prepare the CSV file for login metrics
    with open("login_test_results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["userName", "statusCode", "responseTime(ms)", "result"])

    # Batch processing with ramp-up logic
    batch_size = MAX_CONCURRENT_REQUESTS
    delay_between_batches = rampup_time / (total_load / batch_size)

    responses = []
    users = context.users  # Use the user data from the CSV file

    if not users:
        raise Exception("No registered users available for login.")

    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_REQUESTS) as executor:
        for batch_start in range(0, total_load, batch_size):
            # Pick a random subset of users for each batch
            batch_users = users[batch_start:batch_start + batch_size]
            futures = [executor.submit(send_login_request, user) for user in batch_users]
            for future in as_completed(futures):
                responses.append(future.result())
            time.sleep(delay_between_batches)

    context.responses = responses


@then('all requests should respond with status code {status_code:d}')
def step_then_check_status_code(context, status_code):
    assert all(
        response == status_code for response in context.responses
    ), f"Not all requests responded with status code {status_code}"


@then('the response message should include "{message}"')
def step_then_check_response_message(context, message):
    print(f"Expected response message to include: {message}")