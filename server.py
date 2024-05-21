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


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
