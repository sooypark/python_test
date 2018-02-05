import pandas as pd
import numpy as np
import networkx as nx

import matplotlib.pyplot as plt

#font_name = plt.font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
plt.rc('font', family='Malgun Gothic')


from pprint import pprint

data = pd.read_excel("c:\\temp\\positive-anode.xlsx")

new_df = data.fillna("NAN")
from_list = []
to_list = []

for inx in range(0,27):
    for jnx in range(6,-1, -1) :
         if new_df.iloc[inx, jnx] == "NAN":
             new_df.iloc[inx, jnx] = new_df.iloc[inx, jnx+1]
         if jnx !=0 :
             from_list.append(new_df.iloc[inx, jnx])
         if jnx != 6:
             to_list.append(new_df.iloc[inx, jnx])

# print(len(from_list))
# pprint(from_list)
# print(len(to_list))
# pprint(to_list)

df = pd.DataFrame({ 'from':from_list, 'to':to_list})
G=nx.from_pandas_dataframe(df, 'from', 'to')

nx.draw(G, with_labels=True, node_size=100, node_color="skyblue", node_shape="s", alpha=0.5, linewidths=40, font_family='Malgun Gothic')
plt.show()

'''
for inx in range(0,27):
    temp_list = new_df.loc[inx].tolist()

    for jnx in range(0,len(temp_list)):
       if temp_list[jnx] == "NAN":
           temp_list[jnx] = temp_list[jnx-1]

    print(temp_list)
'''