from app.shared.case import camel_to_snake, params_to_camel, snake_to_camel


def test_case_conversion():
    assert snake_to_camel("policy_name") == "policyName"
    assert camel_to_snake("policyName") == "policy_name"
    assert params_to_camel({"policy_name": "daily"}) == {"policyName": "daily"}
