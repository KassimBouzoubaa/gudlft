import pytest
from flask import Flask, session
from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
        
        
# ----------- TEST CLIENT ---------- #

def test_should_status_code_ok(client):
    """
    Test if the status code of the response from a GET request to '/' is 200 (OK).
    """
    
    response = client.get('/')
    assert response.status_code == 200

# ----------- TEST SHOWSUMMARY ---------- #

def test_show_summary_with_matching_email(client):
    """
    Test if the showSummary route responds correctly with a matching email.
    """
   
    response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert response.status_code == 200
    
    # Assert that the response contains the title of the welcome.html template
    assert b'Summary | GUDLFT Registration' in response.data

def test_show_summary_with_non_matching_email(client):
    """
    Test if the showSummary route handles a non-matching email correctly.
    
    """
    response = client.post('/showSummary', data={'email': 'non_existent@example.com'})
    
    # Redirection
    assert response.status_code == 302  
    
    # We make sure that the flash message is present in the session
    with client.session_transaction() as session:
        flash_messages = dict(session['_flashes'])
        assert 'No club found with the provided email.' in flash_messages.values()

def test_show_summary_with_no_email(client):
    """
    Test if the showSummary route handles a request without an email correctly.
    """
    
    response = client.post('/showSummary')
    
    # Redirection erreur
    assert response.status_code == 400  
# ----------- TEST BOOK ---------- #

def test_book_with_matching_competition_and_club(client):
    """
    Test if the book route responds correctly with a matching competition and club.
    """
    
    # Send a GET request to the book route with a matching competition and club
    response = client.get('/book/Spring%20Festival/Simply%20Lift')
    
    # Ensure that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the response contains the expected title of the book.html template
    assert b'Booking for Spring Festival || GUDLFT' in response.data
    
def test_book_with_non_matching_club_or_competition(client):
    """
    Test if the book route handles missing club or competition correctly.
    """
    
    # Send a GET request to the book route with a nonexistent competition and existing club
    response = client.get('/book/nonexistentcompetition/Simply%20Lift')
    
    # Assuming the route returns a success code even if club or competition is missing
    assert response.status_code == 200  
    
    # Assert that the response contains the expected message indicating the error
    assert b"Club or competition not found - please try again" in response.data

# ----------- TEST PURCHASE PLACES ---------- #

def test_purchase_places_with_insufficient_points(client):
    """
    Test if the purchasePlaces route handles cases where the club has insufficient points.
    """
        
    # Assuming the route returns a success code even if the data is invalid
    response = client.post('/purchasePlaces', data={'competition': 'Spring Festival', 'club': 'Simply Lift', 'places': '20'})
    
    # Ensure that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the flash message indicating the competition is full is present in the response
    assert b"Insufficient number of points available" in response.data
    
def test_purchase_places_with_more_than_12_places(client):
    """
    Test if the purchasePlaces route handles cases where the club has insufficient points.
    """
        
    # Assuming the route returns a success code even if the data is invalid
    response = client.post('/purchasePlaces', data={'competition': 'Spring Festival', 'club': 'Simply Lift', 'places': '13'})
    
    # Ensure that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the flash message indicating the competition is full is present in the response
    assert b"You cannot reserve more than 12 places in a competition" in response.data

def test_purchase_places_with_insufficient_competition_places(client):
    """
    Test if the purchasePlaces route handles cases where there are insufficient places in the competition.
    """
    # Données de la requête POST
    post_data = {
        'competition': 'Super Compete',
        'club': 'Simply Lift',
        'places': '9'
    }

    # Envoi de la requête POST
    response = client.post('/purchasePlaces', data=post_data)

    # Vérification du code de statut de la réponse
    assert response.status_code == 200

    # Vérification de la présence du message d'erreur de places insuffisantes dans la réponse
    assert b"There are not enough places available" in response.data

def test_purchase_places_with_invalid_competition(client):
    """
    Test if the purchasePlaces route handles cases where the competition is not found.
    """
    # Données de la requête POST avec une compétition inexistante
    post_data = {
        'competition': 'Nonexistent Competition',
        'club': 'Simply Lift',
        'places': '4'
    }

    # Envoi de la requête POST
    response = client.post('/purchasePlaces', data=post_data)

    # Vérification du code de statut de la réponse
    assert response.status_code == 200

    # Vérification de la présence du message d'erreur de compétition non trouvée dans la réponse
    assert b"Club or competition not found - please try again" in response.data

def test_purchase_places_with_invalid_club(client):
    """
    Test if the purchasePlaces route handles cases where the club is not found.
    """
    # Données de la requête POST avec un club inexistant
    post_data = {
        'competition': 'Spring Festival',
        'club': 'Nonexistent Club',
        'places': '4'
    }

    # Envoi de la requête POST
    response = client.post('/purchasePlaces', data=post_data)

    # Vérification du code de statut de la réponse
    assert response.status_code == 200

    # Vérification de la présence du message d'erreur de club non trouvé dans la réponse
    assert b"Club or competition not found - please try again" in response.data

def test_purchase_places_with_valid_data(client):
    """
    Test if the purchasePlaces route handles valid data correctly.
    """
        
    # Assuming the route returns a success code even if the data is valid
    response = client.post('/purchasePlaces', data={'competition': 'Spring Festival', 'club': 'Simply Lift', 'places': '4'})
    
    # Ensure that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the flash message indicating successful booking is present in the response
    assert b"Great-booking complete! You bought 4 places." in response.data

# ----------- TEST DISPLAY ---------- #


def test_display_route(client):
    """
    Test the display route.
    """
   
    # Simulate accessing the display route
    response = client.get("/display")
    
    # Check if the status code is 200 (OK)
    assert response.status_code == 200
    
    # Check if the response contains the expected HTML content
    assert b"<h1>Table of number of points by clubs</h1>" in response.data
  