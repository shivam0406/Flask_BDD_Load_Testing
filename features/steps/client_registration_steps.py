import csv
import random
import time
from behave import given, when, then
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://127.0.0.1:5000"
MAX_CONCURRENT_REQUESTS = 10  # Simulate 10 concurrent requests at a time
results = []  # Store successful registration data for in-memory checks


# Generate random user data with timestamp
def generate_random_user():
    timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
    return {
        "fullName": f"Test User {random.randint(1, 1000)}",
        "userName": f"user_{timestamp}_{random.randint(1, 1000)}",
        "email": f"user_{timestamp}_{random.randint(1, 1000)}@example.com",
        "password": "password123",
        "phone": f"{random.randint(1000000000, 9999999999)}",
    }


@given('the registration endpoint "{endpoint}"')
def step_given_registration_endpoint(context, endpoint):
    context.endpoint = f"{BASE_URL}{endpoint}"


@when('I send registration requests with total load {total_load:d} over a ramp-up time of {rampup_time:d} seconds')
def step_when_send_registration_requests(context, total_load, rampup_time):
    def send_request():
        user = generate_random_user()
        start_time = time.time()  # Start timer
        response = requests.post(context.endpoint, data=user)
        end_time = time.time()  # End timer

        response_time = (end_time - start_time) * 1000  # Response time in milliseconds
        status_code = response.status_code

        # Log response metrics
        with open("load_test_results.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                user["userName"],
                status_code,
                response_time,
                "Success" if status_code == 200 else "Failed"
            ])

        # Save successful registrations to `registered_users.csv`
        if status_code == 200 and "User Registered" in response.text:
            results.append(user)
            with open("registered_users.csv", "a", newline="") as userfile:
                writer = csv.writer(userfile)
                writer.writerow([user["userName"], user["email"], user["password"]])

        return status_code

    # Prepare the CSV file for metrics
    with open("load_test_results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["userName", "statusCode", "responseTime(ms)", "result"])

    # Batch processing with ramp-up logic
    batch_size = MAX_CONCURRENT_REQUESTS
    delay_between_batches = rampup_time / (total_load / batch_size)

    responses = []
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_REQUESTS) as executor:
        for batch_start in range(0, total_load, batch_size):
            futures = [executor.submit(send_request) for _ in range(batch_size)]
            for future in as_completed(futures):
                responses.append(future.result())
            time.sleep(delay_between_batches)

    context.responses = responses


@then('all requests should respond with status code {status_code:d}')
def step_then_check_status_code(context, status_code):
    assert all(
        response == status_code for response in context.responses
    ), f"Not all requests responded with status code {status_code}"


@then('the response message should be "{message}"')
def step_then_check_response_message(context, message):
    print(f"Expected response message: {message}")