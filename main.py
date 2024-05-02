import pandas as pd
from pyvis.network import Network
import math
from tkinter import Tk, messagebox

# position_colors sözlüğünü tanımlayın
position_colors = {'CF': 'red', 'RW': 'yellow', 'ST': 'red', 'LW': 'yellow', 'CAM': 'yellow',
                   'CDM': 'yellow', 'CM': 'yellow', 'RM': 'yellow', 'LM': 'yellow', 'LWB': 'blue',
                   'RWB': 'blue', 'LB': 'blue', 'RB': 'blue', 'CB': 'blue', 'GK': 'green'}

df = pd.read_excel(r"C:\Users\okank\Desktop\database.xlsx")

players_with_85_rating = df[df['overall_rating'] == 85]
players_with_90_rating = df[df['overall_rating'] == 90]

num_players_85 = len(players_with_85_rating)
num_players_90 = len(players_with_90_rating)

radius_85 = 200  # Daha iyi görselleştirme için yarıçapı ayarlayın
radius_90 = 200  # Daha iyi görselleştirme için yarıçapı ayarlayın

# Pyvis ağ nesnesini oluşturun
G = Network(height='750px', width='100%', bgcolor='#222222', font_color='white', notebook=True)

def show_player_info(player_name):
    player_info = df[df['name'] == player_name]
    if not player_info.empty:
        messagebox.showinfo("Player Info", f"Name: {player_info['name'].values[0]}\nOverall Rating: {player_info['overall_rating'].values[0]}")
    else:
        messagebox.showerror("Error", "Player not found")

# "85" ve "90" düğümlerini ekleyin
G.add_node("85", label="85", color='blue')
G.add_node("90", label="90", color='blue')

# 85 puan alan oyuncular için düğümler ve kenarlar ekleyin
for i, player in players_with_85_rating.iterrows():
    angle = 2 * math.pi * i / num_players_85
    x = radius_85 * math.cos(angle)
    y = radius_85 * math.sin(angle)
    primary_position = player['positions'].split(',')[0]
    G.add_node(player['name'], label=player['name'], color=position_colors.get(primary_position, 'lightblue'), x=x, y=y)
    G.add_edge("85", player['name'])
    # Düğümlere tıklandığında bilgi ekranını aç
    G.add_node(player['name'], onclick=show_player_info)

# 90 puan alan oyuncular için düğümler ve kenarlar ekleyin
for i, player in players_with_90_rating.iterrows():
    angle = 2 * math.pi * i / num_players_90
    x = radius_90 * math.cos(angle)
    y = radius_90 * math.sin(angle)
    primary_position = player['positions'].split(',')[0]
    G.add_node(player['name'], label=player['name'], color=position_colors.get(primary_position, 'lightblue'), x=x, y=y)
    G.add_edge("90", player['name'])
    # Düğümlere tıklandığında bilgi ekranını aç
    G.add_node(player['name'], onclick=show_player_info)

# Ağı göster
G.show('Player_Ağı.html')