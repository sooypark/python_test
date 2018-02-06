import pandas as pd
import numpy as np
import networkx as nx

import matplotlib.pyplot as plt

#font_name = plt.font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
plt.rc('font', family='Malgun Gothic')


from pprint import pprint

data = pd.read_excel("c:\\temp\\positive-anode.xlsx")

#결측치를NAN으로변경
new_df = data.fillna("NAN")
from_list = []
to_list = []

#From to list create
for inx in range(0,27):
    for jnx in range(6,-1, -1) :
         if new_df.iloc[inx, jnx] == "NAN":
             new_df.iloc[inx, jnx] = new_df.iloc[inx, jnx+1]
         if jnx !=0 :
             from_list.append(new_df.iloc[inx, jnx])
         if jnx != 6:
             to_list.append(new_df.iloc[inx, jnx])

#fromTO리스트의길이가같은지검증
print(len(from_list))
# pprint(from_list)
print(len(to_list))
# pprint(to_list)

#자기자신을fromTo로가지는경우삭제
#reverse로삭제해야outofrange에러가안남
for inx in reversed(range(len(from_list))):
    if from_list[inx] == to_list[inx]:
        del(from_list[inx])
        del(to_list[inx])

df = pd.DataFrame({ 'from':from_list, 'to':to_list})
G=nx.from_pandas_dataframe(df, 'from', 'to' )

#degree에따라size를드라게하기위함
def nodesize_return():
    return_val = []
    for i,v in G.degree():
        if v <=2:
            return_val.append(v)
        else:
            return_val.append(v*10)
    return return_val

nx.draw(G, with_labels=True, node_size=nodesize_return(), node_color="skyblue",  alpha=0.5, linewidths=20, font_family='Malgun Gothic', font_size='8')
#nx.spring_layout(G,k=0.15,iterations=20)
plt.show()

