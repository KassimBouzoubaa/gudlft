def search_club(club_name, clubs):
    """
    Search for a club by its name.

    Args:
        club_name (str): The name of the club to search for.

    Returns:
        dict or None: Details of the club if found, otherwise None.
    """
    found_club = next((c for c in clubs if c["name"] == club_name), None)
    return found_club

def search_competition(competition_name, competitions):
    """
    Search for a competition by its name.

    Args:
        competition_name (str): The name of the competition to search for.

    Returns:
        dict or None: Details of the competition if found, otherwise None.
    """
    found_competition = next((c for c in competitions if c["name"] == competition_name), None)
    return found_competition

def subtract_places_from_competition(competition, places_required):
    """
    Subtract the required number of places from a competition.

    Args:
        competition (dict): Details of the competition.
        places_required (int): The number of places required.

    Returns:
        int: The remaining number of places after subtraction.

    Raises:
        ValueError: If the number of places required is greater than the available places in the competition.
        ValueError: If places_required is negative.
    """
    if places_required < 0:
        raise ValueError("Number of places required cannot be negative")
    
    remaining_places = int(competition["numberOfPlaces"]) - int(places_required)
    if remaining_places < 0:
        raise ValueError("Not enough places available in the competition")
    return remaining_places

def subtract_places_from_club(club, places_required):
    """
    Subtract the required number of places from the club's total points.

    Args:
        club (dict): Details of the club.
        places_required (int): The number of places required.

    Returns:
        int: The club's total points after subtraction.

    Raises:
        ValueError: If the number of places required is greater than the available points in the club.
        ValueError: If places_required is negative.
    """
    if places_required < 0:
        raise ValueError("Number of places required cannot be negative")
    
    remaining_points = int(club["points"]) - int(places_required)
    if remaining_points < 0:
        raise ValueError("Insufficient number of points available in the club")
    return remaining_points

