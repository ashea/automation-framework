# automation-framework
This is a python project to contribute to a base for building automation projects

# Start installing packages and dependencies
pip install -r requirements.txt

# Run specific tests using tags
behave --tags=login  ui_tests/features/test_framework.feature

# Run test using allure reporting
behave -f allure_behave.formatter:AllureFormatter -o allure-results features/


