Feature: Load Testing for Client Login

  Scenario: Load testing with registered user data
    Given the login endpoint "/client_login"
    And the user data file "registered_users.csv"
    When I send login requests with total load 100 over a ramp-up time of 10 seconds
    Then all requests should respond with status code 200
    And the response message should include "token"