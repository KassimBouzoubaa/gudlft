import json
from flask import Flask, render_template, request, redirect, flash, url_for, session, abort
from utils import search_club, search_competition, subtract_places_from_club, subtract_places_from_competition


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/showSummary", methods=["POST"])
def showSummary():
    email = request.form.get("email")
    if not email:
        abort(400)
    matching_clubs = [club for club in clubs if club["email"] == email]
    if matching_clubs:
        club = matching_clubs[0]
        dict(session.pop("_flashes", []))
        return render_template("welcome.html", club=club, competitions=competitions)
    else:
        flash("No club found with the provided email.")
        return redirect(url_for("index"))

@app.route("/book/<string:competition>/<string:club>")
def book(competition, club):
    
    foundClub = search_club(club, clubs)
    foundCompetition = search_competition(competition, competitions)
    
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Club or competition not found - please try again")
        return render_template("welcome.html", club=club, competitions=competitions) 


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
        
    # Récupération des données d'entrée
    club_input = request.form.get("club")
    competition_input = request.form.get("competition")
    places_required_input = request.form.get("places")

    # Vérification des données d'entrée
    if not club_input or not competition_input or not places_required_input:
        abort(400)

    try:
        # Convertir le nombre de places requis en entier
        places_required = int(places_required_input)
    except ValueError:
        # Si une erreur se produit lors de la conversion, renvoyer une erreur 400 (Bad Request)
        abort(400)  # Erreur: places_required_input n'est pas un entier valide

    # Recherche du club et de la compétition
    club = search_club(club_input, clubs)
    competition = search_competition(competition_input, competitions)
    
    if club is None or competition is None:
        flash("Club or competition not found - please try again")
        return render_template("welcome.html", club=club, competitions=competitions) 

    # Vérification de la disponibilité des places et des points du club
    if (
        places_required <= int(club["points"])
        and places_required <= 12
        and places_required <= int(competition["numberOfPlaces"])
    ):
        competition["numberOfPlaces"] = subtract_places_from_competition(competition, places_required)        
        club["points"] = subtract_places_from_club(club, places_required)
        flash(f"Great-booking complete! You bought {places_required} places.")
    elif places_required > int(club["points"]):
        flash(f"Insufficient number of points available")
    elif places_required > 12:
        flash(f"You cannot reserve more than 12 places in a competition")
    else:
        flash(f"There are not enough places available")

    return render_template("welcome.html", club=club, competitions=competitions)

@app.route("/display")
def display():
    return render_template('display.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
