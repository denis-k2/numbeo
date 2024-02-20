import json
import sys
from pathlib import Path
from types import NoneType

import pytest
from fastapi.testclient import TestClient

sys.path = ["", ".."] + sys.path[1:]


def test_cities(client: TestClient):
    response = client.get("/cities")
    r_json = response.json()
    assert response.status_code == 200
    assert len(r_json) == r_json[-1]["city_id"]
    assert r_json[0]["city_id"] == 1
    assert r_json[18]["city"] == "Boston"
    assert r_json[19]["state_code"] == "US-CA"
    assert r_json[201]["country_code"] == "CAN"


@pytest.mark.parametrize(
    ("country", "quantity", "status_code"),
    [
        ("ARG", 1, 200),
        ("can", 29, 200),
        ("Rus", 8, 200),
        ("usA", 58, 200),
        ("A", 20, 422),
        ("AB", 20, 422),
        ("ABC", 20, 404),
        ("ABCD", 20, 422),
        (123, 20, 404),
        (1, 20, 422),
    ],
)
def test_cities_by_country(
    country: str, quantity: int, status_code: int, client: TestClient
):
    response = client.get(f"/cities?country_code={country}")
    r_json = response.json()
    assert response.status_code == status_code
    if response.status_code == 200:
        assert len(r_json) == quantity


def test_countries(client: TestClient):
    response = client.get("/countries")
    r_json = response.json()
    assert response.status_code == 200
    assert len(r_json) == 249
    assert r_json[43]["country_code"] == "CHN"
    assert r_json[43]["country"] == "China"


@pytest.mark.parametrize(
    (
        "city_id",
        "city",
        "state_code",
        "country",
        "cost",
        "idx",
        "climate",
        "status_code",
    ),
    [
        (1, "Hamilton", None, "Bermuda", False, True, True, 200),
        (1, "Hamilton", None, "Bermuda", "any_str", True, True, 422),
        (1, "Hamilton", None, "Bermuda", True, "any_str", False, 422),
        (1, "Hamilton", None, "Bermuda", False, False, 123, 422),
        ("any_str", "Hamilton", None, "Bermuda", False, False, False, 422),
        (50, "Nashville", "US-TN", "United States of America", True, False, False, 200),
        (273, "Tokyo", None, "Japan", True, False, True, 200),
        (534, "Karachi", None, "Pakistan", True, False, True, 200),  # the last city
        (535, "Any", None, "Any", True, True, True, 404),
    ],
)
def test_city_id_full(
    city_id: int,
    city: str,
    state_code: str,
    country: str,
    cost: bool,
    idx: bool,
    climate: bool,
    status_code: int,
    client: TestClient,
    token: str,
):
    response = client.get(
        f"/city/{city_id}?numbeo_cost={cost}&numbeo_indices={idx}&avg_climate={climate}",
        headers={"accept": "application/json", "Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status_code

    if response.status_code == 200:
        r_json = response.json()
        assert r_json["city_id"] == city_id
        assert r_json["city"] == city
        assert r_json["state_code"] == state_code
        assert r_json["country"] == country
        if cost:
            assert isinstance(r_json["numbeo_cost"], dict)
        else:
            assert isinstance(r_json["numbeo_cost"], NoneType)
        if idx:
            assert isinstance(r_json["numbeo_indices"], dict)
        else:
            assert isinstance(r_json["numbeo_indices"], NoneType)
        if climate:
            assert isinstance(r_json["avg_climate"], dict)
        else:
            assert isinstance(r_json["avg_climate"], NoneType)


@pytest.mark.parametrize(
    ("country_code", "country", "numbeo", "legatum", "status_code"),
    [
        ("AUS", "Australia", True, True, 200),
        ("deu", "Germany", True, False, 200),
        ("Mex", "Mexico", False, True, 200),
        ("vNm", "Viet Nam", False, False, 200),
        ("A", "Any", True, True, 422),
        ("AB", "Any", True, True, 422),
        ("ABC", "Any", True, True, 404),
        ("ABCD", "Any", True, True, 422),
        ("123", "Any", True, True, 404),
        (12, "Any", True, True, 422),
    ],
)
def test_country_full(
    country_code: str,
    country: str,
    numbeo: bool,
    legatum: bool,
    status_code: int,
    client: TestClient,
    token: str,
):
    response = client.get(
        f"/country/{country_code}?numbeo_indices={numbeo}&legatum_indices={legatum}",
        headers={"accept": "application/json", "Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status_code
    if response.status_code == 200:
        r_json = response.json()
        assert r_json["country_code"] == country_code.upper()
        assert r_json["country"] == country
        if numbeo:
            assert isinstance(r_json["numbeo_indices"], dict)
        else:
            assert isinstance(r_json["numbeo_indices"], NoneType)
        if legatum:
            assert isinstance(r_json["legatum_indices"], dict)
        else:
            assert isinstance(r_json["legatum_indices"], NoneType)


@pytest.mark.parametrize(
    ("city_id", "city"),
    [
        (14, "San Francisco"),
        (83, "Vancouver"),
        (464, "Moscow"),
    ],
)
def test_city_json(city_id, city, client: TestClient, token: str):
    response = client.get(
        f"/city/{city_id}?numbeo_cost=true&numbeo_indices=true&avg_climate=true",
        headers={"accept": "application/json", "Authorization": f"Bearer {token}"},
    )
    with Path(f"tests/integration/jsons/{city}.json").open() as file:
        json_file = json.load(file)
    assert response.json() == json_file
