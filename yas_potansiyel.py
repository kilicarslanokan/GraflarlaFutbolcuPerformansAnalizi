import pandas as pd
import matplotlib.pyplot as plt

# Veri setini oku
df = pd.read_excel(r"C:\Users\okank\Desktop\önemli\DERSLER\3.2\Ağ Programlama\database.xlsx")

# Scatter plot oluştur
plt.figure(figsize=(10, 6))
plt.scatter(df['age'], df['potential'], alpha=0.5)  # x ekseni yaş, y ekseni potansiyel rating
plt.title('Yaş ve Potansiyel Rating Karşılaştırması')
plt.xlabel('Yaş')
plt.ylabel('Potansiyel Rating')
plt.grid(True)
plt.show()
