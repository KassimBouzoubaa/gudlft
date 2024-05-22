import pytest
from utils import search_club, search_competition, subtract_places_from_competition, subtract_places_from_club

# ----------- TEST SEARCH CLUB ---------- #

def test_search_club_with_existing_club():
    clubs = [{"name": "Club A"}, {"name": "Club B"}, {"name": "Club C"}]
    club_name = "Club B"
    expected_result = {"name": "Club B"}
    assert search_club(club_name, clubs) == expected_result

def test_search_club_with_non_existing_club():
    clubs = [{"name": "Club A"}, {"name": "Club B"}, {"name": "Club C"}]
    club_name = "Club D"
    assert search_club(club_name, clubs) is None

def test_search_club_with_empty_club_list():
    clubs = []
    club_name = "Club A"
    assert search_club(club_name, clubs) is None
    
# ----------- TEST SEARCH COMPETITION ---------- #

def test_search_competition_with_existing_competition():
    competitions = [{"name": "Competition A"}, {"name": "Competition B"}, {"name": "Competition C"}]
    competition_name = "Competition B"
    expected_result = {"name": "Competition B"}
    assert search_competition(competition_name, competitions) == expected_result

def test_search_competition_with_non_existing_competition():
    competitions = [{"name": "Competition A"}, {"name": "Competition B"}, {"name": "Competition C"}]
    competition_name = "Competition D"
    assert search_competition(competition_name, competitions) is None

def test_search_competition_with_empty_competition_list():
    competitions = []
    competition_name = "Competition A"
    assert search_competition(competition_name, competitions) is None
    
# ----------- TEST SUBSTRACT COMPETITION ---------- #

def test_subtract_places_with_sufficient_places():
    # Competition avec 10 places disponibles
    competition = {"numberOfPlaces": 10}
    places_required = 3  # Supprimer 3 places
    expected_result = 7  # Résultat attendu après soustraction
    assert subtract_places_from_competition(competition, places_required) == expected_result

def test_subtract_places_with_insufficient_places():
    # Competition avec seulement 2 places disponibles
    competition = {"numberOfPlaces": 2}
    places_required = 5  # Supprimer 5 places, mais il n'y en a que 2 disponibles
    with pytest.raises(ValueError):
        subtract_places_from_competition(competition, places_required)

def test_subtract_places_with_negative_places_required():
    # Competition avec 10 places disponibles
    competition = {"numberOfPlaces": 10}
    places_required = -3  # Tentative de supprimer -3 places
    with pytest.raises(ValueError):
        subtract_places_from_competition(competition, places_required)
        
# ----------- TEST SUBSTRACT CLUB ---------- #

def test_subtract_places_with_sufficient_points():
    # Club avec 100 points disponibles
    club = {"points": 100}
    places_required = 30  # Supprimer 30 places
    expected_result = 70  # Résultat attendu après soustraction
    assert subtract_places_from_club(club, places_required) == expected_result

def test_subtract_places_with_insufficient_points():
    # Club avec seulement 20 points disponibles
    club = {"points": 20}
    places_required = 50  # Supprimer 50 places, mais il n'y en a que 20 disponibles
    with pytest.raises(ValueError):
        subtract_places_from_club(club, places_required)

def test_subtract_places_with_negative_places_required():
    # Club avec 100 points disponibles
    club = {"points": 100}
    places_required = -30  # Tentative de supprimer -30 places
    with pytest.raises(ValueError):
        subtract_places_from_club(club, places_required)

