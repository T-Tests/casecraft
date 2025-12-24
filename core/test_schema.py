from core.schema import TestCase, TestSuite

sample_test_case = TestCase(
    use_case="User Login",
    test_case="Login with valid credentials",
    preconditions=[
        "User has a registered account",
        "User is on the login page"
    ],
    test_data={
        "username": "valid_user",
        "password": "valid_password"
    },
    steps=[
        "Enter username in the username field",
        "Enter password in the password field",
        "Click the login button"
    ],
    priority="high",
    tags=["authentication", "happy-path"],
    expected_results=[
        "User is successfully authenticated",
        "User is redirected to the dashboard"
    ],
    actual_results=[]
)

suite = TestSuite(
    feature_name="Authentication",
    source_document="login_feature.txt",
    test_cases=[sample_test_case]
)

print(suite.model_dump_json(indent=2))
