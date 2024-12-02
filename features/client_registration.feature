Feature: Load Testing for Client Registration

  Scenario: Load testing with controlled concurrency
    Given the registration endpoint "/client_registeration"
    When I send registration requests with total load 100 over a ramp-up time of 30 seconds
    Then all requests should respond with status code 200
    And the response message should be "User Registered"