from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import  login_required, current_user
from .models import Note, Player
from . import db
import json
from bs4 import BeautifulSoup
import requests

views = Blueprint('views', __name__)


@views.route('/', methods={'GET', 'POST'})
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")

        if len(note) < 1:
            flash("Name is too short", category ='error')
        else:
            new_note = Note(text=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Player added", category ='success')

    return render_template("home.html", user=current_user)


@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})




@views.route('/stats', methods={'GET', 'POST'})
@login_required
def stats():

    passurl= "https://www.pro-football-reference.com/leaders/pass_yds_career.htm"
    rushurl="https://www.pro-football-reference.com/leaders/rush_yds_career.htm"
    recurl="https://www.pro-football-reference.com/leaders/rec_yds_career.htm"
    defurl="https://www.pro-football-reference.com/leaders/tackles_solo_career.htm"


    return render_template("stats.html", runners=getplayers(rushurl, "rush_yds"), passers=getplayers(passurl, "pass_yds"), WRs=getplayers(recurl, "rec_yds"), Tacks=getplayers(defurl, "tackles_solo") ,user=current_user)




def getplayers(url, stat_type):
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    rows = doc.select('tbody tr')

    players = []

    for row in rows[:10]:
        rank = row.select_one('th[data-stat="rank"]').text.strip()
        name = row.select_one('td[data-stat="player"] a').text.strip()
        yards = row.select_one(f'td[data-stat="{stat_type.lower().replace(" ", "_")}"]').text.strip()
        years = row.select_one('td[data-stat="years"]').text.strip()
        team = row.select_one('td[data-stat="team"]').text.strip()

        player = Player(rank=rank, name=name, yards=yards, years=years, team=team)
        players.append(player)

    return players
