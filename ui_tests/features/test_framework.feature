Feature: Test Python Automation Framework

Scenario: First Test
    Given I am on the google page
    When I search the word "Rosario"
    Then I should see that the search is performed correctly
