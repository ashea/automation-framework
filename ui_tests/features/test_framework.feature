Feature: Test Python Automation Framework

Scenario: First Test
    Given I am on the google page
    When I search the word "Rosario"
    Then I should see that the search is performed correctly

Scenario: Second Test
    Given I am on the google page
    When I search the word "Bad"
    Then I should see that the search is performed wrongly

Scenario: Third Test
    Given I am on the google page
    When I search the word "Ash"
    Then I should see that the search is performed correctly
