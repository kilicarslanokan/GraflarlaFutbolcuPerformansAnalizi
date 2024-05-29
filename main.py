import pandas as pd
from pyvis.network import Network
import math

# Veritabanını yükleyin
df = pd.read_excel(r"C:\Users\okank\Desktop\önemli\DERSLER\3.2\Ağ Programlama\database.xlsx")

# Pozisyon renklerini tanımlayın
position_colors = {'CF': 'red', 'RW': 'yellow', 'ST': 'red', 'LW': 'yellow', 'CAM': 'yellow',
                   'CDM': 'yellow', 'CM': 'yellow', 'RM': 'yellow', 'LM': 'yellow', 'LWB': 'blue',
                   'RWB': 'blue', 'LB': 'blue', 'RB': 'blue', 'CB': 'blue', 'GK': 'green'}

# Oyuncuları genel değerlere göre filtreleyin
rating_groups = [85, 86, 87, 88, 89, 90, 91, 92, 94]
players_by_rating = {rating: df[df['overall_rating'] == rating] for rating in rating_groups}

# Pyvis ağ nesnesini oluşturun
G = Network(height='750px', width='100%', bgcolor='#000000', font_color='white')

# Rating düğümlerini ekleyin
for rating in rating_groups:
    G.add_node(str(rating), label=str(rating), color='blue')

# Her bir rating grubu için düğümler ve kenarlar ekleyin
for rating, players in players_by_rating.items():
    num_players = len(players)
    radius = 200  # Daha iyi görselleştirme için yarıçapı ayarlayın

    for i, player in players.iterrows():
        angle = 2 * math.pi * i / num_players
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        primary_position = player['positions'].split(',')[0]
        G.add_node(player['name'], label=player['name'], title=f"Name: {player['name']}<br>Age: {player['age']}<br>Positions: {player['positions']}<br>Nationality: {player['nationality']}<br>Preferred Foot: {player['preferred_foot']}<br>Value: {player['value_euro']}", color=position_colors.get(primary_position, 'lightblue'), x=x, y=y)
        G.add_edge(str(rating), player['name'])

# Düğüm ve kenar verilerini JSON formatına dönüştürme
nodes_json = G.nodes
edges_json = G.edges

# HTML içeriğini oluşturma
html_content = f'''
<!doctype html>
<html>
<head>
  <title>Oyuncu Overall Network</title>
  <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" rel="stylesheet" type="text/css" />
  <style>
    body, html {{
      height: 100%;
      margin: 0;
      padding: 0;
      background-color: black;  /* Arka plan rengini siyah yapar */
      color: white;
    }}
    #mynetwork {{
      width: 100%;
      height: 90%;
      background-color: black;  /* Ağın arka plan rengini siyah yapar */
    }}
    #searchBox {{
      width: 100%;
      height: 10%;
      background-color: black;
      display: flex;
      justify-content: center;
      align-items: center;
    }}
    .info-box {{
      position: absolute;
      background-color: white;
      color: black;
      border: 1px solid black;
      padding: 10px;
      z-index: 1000;
    }}
    input[type="text"] {{
      width: 200px;
      padding: 10px;
      border-radius: 5px;
      border: 1px solid white;
      background-color: black;
      color: white;
    }}
    input[type="text"]::placeholder {{
      color: white;
    }}
  </style>
</head>
<body>
<div id="searchBox">
  <input type="text" id="searchInput" placeholder="Oyuncu ismi girin">
</div>
<div id="mynetwork"></div>
<script type="text/javascript">
  var nodes = new vis.DataSet({nodes_json});
  var edges = new vis.DataSet({edges_json});

  var container = document.getElementById('mynetwork');
  var data = {{
    nodes: nodes,
    edges: edges
  }};
  var options = {{
    nodes: {{
      shape: 'dot',
      size: 20,
      font: {{
        size: 15,
        color: 'white'
      }},
      borderWidth: 2
    }},
    edges: {{
      width: 2,
      color: {{
        color: 'white'
      }}
    }},
    physics: {{
      stabilization: true
    }}
  }};
  var network = new vis.Network(container, data, options);

  // Oyuncu düğümüne tıklama olayı
  network.on("click", function (params) {{
    if (params.nodes.length > 0) {{
      var nodeId = params.nodes[0];
      var node = nodes.get(nodeId);
      if (node.title) {{
        var infoBox = document.createElement("div");
        infoBox.className = "info-box";
        infoBox.innerHTML = node.title;
        infoBox.style.left = params.pointer.DOM.x + 'px';
        infoBox.style.top = params.pointer.DOM.y + 'px';
        document.body.appendChild(infoBox);
        setTimeout(function () {{
          infoBox.parentNode.removeChild(infoBox);
        }}, 5000);
      }}
    }}
  }});

  // Arama kutusuna olay dinleyici ekleyin
  document.getElementById('searchInput').addEventListener('input', function() {{
    var query = this.value.toLowerCase();
    nodes.update(nodes.get().map(function(node) {{
      if (!query) {{
        return {{
          id: node.id,
          size: 20,  // Varsayılan boyuta geri döndürün
          hidden: false  // Tüm düğümleri gösterin
        }};
      }} else if (node.label.toLowerCase().includes(query)) {{
        return {{
          id: node.id,
          size: 30  // Bulunan düğümün boyutunu artırın
        }};
      }} else {{
        return {{
          id: node.id,
          hidden: true  // Arama yapılıyorsa diğer düğümleri gizleyin
        }};
      }}
    }}));
  }});
</script>
</body>
</html>
'''

# HTML dosyasını oluşturma ve içeriği yazma
with open('Player_Agi.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

print("HTML dosyası oluşturuldu: Player_Agi.html")