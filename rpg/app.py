from flask import Flask, render_template, request, session, redirect, url_for
from game_logic import Character, Enemy, Gadget  # Import your existing game classes
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/new_game', methods=['GET', 'POST'])
def new_game():
    if request.method == 'POST':
        name = request.form['name']
        class_type = request.form['class']
        player = Character(name, class_type)
        session['player'] = player.__dict__
        return redirect(url_for('main_game'))
    return render_template('new_game.html')

@app.route('/main_game')
def main_game():
    if 'player' not in session:
        return redirect(url_for('home'))
    player_data = session['player']
    return render_template('game.html', player=player_data)

@app.route('/combat')
def combat():
    if 'player' not in session:
        return redirect(url_for('home'))
    player_data = session['player']
    enemy = Enemy("Goblin", 30, 5, 20, 15)  # Example enemy
    return render_template('combat.html', player=player_data, enemy=enemy.__dict__)