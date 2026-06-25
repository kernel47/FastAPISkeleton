from app.shared.parser import extract_next_after


def test_extract_next_after_from_netbackup_next_cursor():
    payload = {"meta": {"pagination": {"next": "2323544545:45454545", "limit": 100}}}

    assert extract_next_after(payload) == "2323544545:45454545"
