from app.modules.referential.service import ReferentialService, split_hostnames


def test_split_hostnames():
    assert split_hostnames("a,b; c") == ["a", "b", "c"]


def test_master_parser_aliases():
    service = ReferentialService()
    master = service._master(
        {
            "hostname": "nbu01",
            "apiUrl": "https://nbu01",
            "login": "admin",
            "password": "secret",
            "isBaas": True,
        }
    )

    assert master.hostname == "nbu01"
    assert master.base_url == "https://nbu01"
    assert master.username == "admin"
    assert master.is_baas is True
