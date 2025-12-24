from core.schema import TestCase, TestSuite

sample_test_case = TestCase(
    id="TC_LOGIN_001",
    title="Login with valid credentials",
    priority="high",
    type="functional",
    preconditions=["User has a registered account"],
    steps=[
        "Navigate to the login page",
        "Enter valid username and password",
        "Click the login button"
    ],
    expected_results=[
        "User is successfully logged in and redirected to the dashboard"
    ],
    test_data={
        "username": "valid_user",
        "password": "valid_password"
    },
    tags=["login", "happy-path"]
)

suite = TestSuite(
    feature_name="User Login",
    source_document="login_feature.txt",
    test_cases=[sample_test_case]
)

print(suite.model_dump_json(indent=2))
