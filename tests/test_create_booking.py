import allure
import pytest
import requests


@allure.feature('Test Create Booking')
@allure.story('Create booking success')
def test_create_booking(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data
    response = api_client.create_booking(booking_data)

    assert "bookingid" in response
    booking = response["booking"]
    assert booking["firstname"] == booking_data["firstname"]
    assert booking["lastname"] == booking_data["lastname"]
    assert booking["totalprice"] == booking_data["totalprice"]
    assert booking["depositpaid"] == booking_data["depositpaid"]
    assert booking["additionalneeds"] == booking_data["additionalneeds"]


@allure.feature('Test Create Booking')
@allure.story('Create booking with empty JSON')
def test_create_booking_empty_json(api_client):
    empty_data = {}
    with pytest.raises(requests.exceptions.HTTPError):
        api_client.create_booking(empty_data)

@allure.feature('Test Create Booking')
@allure.story('Test invalid data types')
def test_create_booking_invalid_data_types(api_client):
    data = {
        "firstname": 123456,
        "lastname": [],
        "totalprice": "number",
        "depositpaid": "yes",
        "bookingdates": "254582",
        "additionalneeds": "Breakfast"
    }
    with pytest.raises(requests.exceptions.HTTPError):
        api_client.create_booking(data)

@allure.feature('Test Create Booking')
@allure.story('Create booking without required field')
def test_create_booking_without_required_field(api_client, booking_dates):
    data = {
    "firstname" : "Joe",
    "lastname" : "Perl",
    "totalprice" : 111,
    "depositpaid" : True,
    "additionalneeds" : "Breakfast"
    }
    with pytest.raises(requests.exceptions.HTTPError):
        api_client.create_booking(data)
