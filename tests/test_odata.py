from app.shared.odata import combine_odata, netbackup_cursor_params, simple_filters_to_odata


def test_simple_filters_to_odata():
    assert simple_filters_to_odata({"policy_name": "daily", "policy_type": "VMware"}) == (
        "policyName eq 'daily' and policyType eq 'VMware'"
    )


def test_combine_odata():
    assert combine_odata("active eq true", "policyName eq 'daily'") == (
        "policyName eq 'daily' and active eq true"
    )


def test_cursor_params():
    assert netbackup_cursor_params(100, "abc", "state eq 'DONE'") == {
        "page[limit]": 100,
        "page[after]": "abc",
        "filter": "state eq 'DONE'",
    }
