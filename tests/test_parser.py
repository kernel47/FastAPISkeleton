from app.modules.netbackup.parser import parse_job, parse_policy


def test_policy_parser_raw():
    parsed = parse_policy({"attributes": {"policyName": "daily", "policyType": "VMware"}}, raw=True)

    assert parsed["policy_name"] == "daily"
    assert parsed["policy_type"] == "VMware"
    assert parsed["raw"]["policy_name"] == "daily"


def test_job_parser_status_zero():
    parsed = parse_job({"attributes": {"jobId": 10, "statusCode": 0, "clientName": "srv01"}})

    assert parsed["job_id"] == 10
    assert parsed["status_code"] == 0
    assert parsed["client_name"] == "srv01"
