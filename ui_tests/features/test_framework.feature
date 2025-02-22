Feature: Test Python Automation Framework

@login
Scenario: Test Invalid Login
    Given I am in the login page
    When I input credentials "invalid_user@test.com" and "InvalidPassword"
    Then I should see the login error message displayed correctly

@login
Scenario: Test Success Login
    Given I am in the login page
    When I input credentials "invalid_user@test.com" and "InvalidPassword"
    Then I should see the login success message

Scenario: Third Test
    Given I am on the google page
    When I search the word "Ash"
    Then I should see that the search is performed correctly
