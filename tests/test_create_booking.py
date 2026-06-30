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
@allure.story('Server unavailable')
def test_create_booking_server_unavailable(api_client, mocker, generate_random_booking_data):
    mocker.patch.object(api_client.session, 'post', side_effect=Exception("Server unavailable"))
    with pytest.raises(Exception, match="Server unavailable"):
        api_client.create_booking(generate_random_booking_data)

@allure.feature('Test Create Booking')
@allure.story('Test wrong HTTP method')
def test_create_booking_wrong_method(api_client, mocker, generate_random_booking_data):
    mock_response = mocker.Mock()
    mock_response.status_code = 405
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 200 but got 405"):
        api_client.create_booking(generate_random_booking_data)

@allure.feature('Test Create Booking')
@allure.story('Test server error')
def test_create_booking_internal_server_error(api_client, mocker, generate_random_booking_data):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 200 but got 500"):
        api_client.create_booking(generate_random_booking_data)

@allure.feature('Test Create Booking')
@allure.story('Test wrong URL')
def test_create_booking_not_found(api_client, mocker, generate_random_booking_data):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 200 but got 404"):
        api_client.create_booking(generate_random_booking_data)

@allure.feature('Test Create Booking')
@allure.feature('Test timeout')
def test_create_booking_timeout(api_client, mocker, generate_random_booking_data):
    mocker.patch.object(api_client.session, 'post', side_effect=requests.Timeout)
    with pytest.raises(requests.Timeout):
        api_client.create_booking(generate_random_booking_data)