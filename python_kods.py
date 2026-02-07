import pandas as pd
import networkx as nx
from pyvis.network import Network
from itertools import combinations

df = pd.DataFrame({
    'tabula':['a','a','a','a',
              'b','b',
              'c','c','c','c','c','c',
             'd','d','d','d'],
    'kolona':['kopeja','a2','a3','kopeja2',
              'b1','kopeja',
              'c1','c2','c3','c4','c5','kopeja2',
             'kopeja','d2','d3','kopeja2']})

# izveido karti: kolona -> tabulu saraksts
col_map = df.groupby('kolona')['tabula'].apply(list)

grafiks = nx.Graph()
grafiks.add_nodes_from(df['tabula'], bipartite='table')
grafiks.add_nodes_from(df['kolona'], bipartite='column')

for _, tab_col in df.iterrows():
    grafiks.add_edge(tab_col['tabula'], tab_col['kolona'])

# sataisām sarasktu ar visiem RGB kodiem pēc kārtas, lai ir smuka varavīksne
krasu_tabula, r,g,b=[], 255,0,0
while g<255:
    krasu_tabula.append([r,g,b])
    r,g,b=r,g+1,b
while r>0:
    krasu_tabula.append([r,g,b])
    r,g,b=r-1,g,b
while b<255:
    krasu_tabula.append([r,g,b])
    r,g,b=r,g,b+1
while g>0:
    krasu_tabula.append([r,g,b])
    r,g,b=r,g-1,b
while r<255:
    krasu_tabula.append([r,g,b])
    r,g,b=r+1,g,b
while b>0:
    krasu_tabula.append([r,g,b])
    r,g,b=r,g,b-1
krasu_tabula.append([r,g,b])

# sadalām visu krāsu gammu vienadās daļās atkarībā no tabulu skaita un iegūstam RGB kodus, kas ir maksimāli tāliu viens no otra
stils={}
for tab_nr in range(0, len(set(df['tabula']))):
    tab_nosaukums = list(set(df['tabula']))[tab_nr]
    stils.update({tab_nosaukums.lower():{'size': 15, 'color': f'''rgb({str(krasu_tabula[tab_nr * int(len(krasu_tabula)/len(set(df['tabula'])))])[1:-1]})''', 'label': f'tabula - {tab_nosaukums.upper()}'}})
# variants kā nopietnāk noformatēt nodes. parastā krāsa un pēc iezīmēšnas krāsa --> {'background': '#F77B00', 'border': '#000000', 'highlight': {'background': '#FFB066', 'border': '#000000'}}

for node in grafiks.nodes():
    if node in stils:
        for k, v in stils[node].items():
            grafiks.nodes[node][k] = v
    
# vizualizācija
net = Network(height="800px", width="100%")
net.from_nx(grafiks)
net.write_html("network_tables.html")


from IPython.display import IFrame
IFrame("network_tables.html", width="100%", height=800)
