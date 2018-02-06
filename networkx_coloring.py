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
#2차원 배열을 위한 matrix 배열잡기
matrix = []

for inx in range(0,27):
    t1 = ()
    source = ""
    target = ""
    #2차원 배열중 row_list를 잡기위한 배열잡기
    row_list = []

    for jnx in range(6,-1, -1) :
         t2 = ()
         if new_df.iloc[inx, jnx] == "NAN":
             new_df.iloc[inx, jnx] = new_df.iloc[inx, jnx+1]
         if jnx !=0 :
             from_list.append(new_df.iloc[inx, jnx])
             source = new_df.iloc[inx, jnx]
             if new_df.iloc[inx, jnx -1] == "NAN":
                 target = new_df.iloc[inx, jnx]
             else:
                 target = new_df.iloc[inx, jnx-1]
         if jnx != 6:
             to_list.append(new_df.iloc[inx, jnx])

         t2 = (source, target)

         #for 문의 for문을 돌면서 row_list에 값 채워넣기
         row_list.append(t2)

    #for문을 돌면서 2차원 배열에 row_list 채워넣기
    matrix.append(row_list)

pprint(matrix)
# print(len(from_list))
# pprint(from_list)
# print(len(to_list))
# pprint(to_list)

for inx in reversed(range(len(from_list))):
    if from_list[inx] == to_list[inx]:
        del(from_list[inx])
        del(to_list[inx])

df = pd.DataFrame({ 'from':from_list, 'to':to_list})
G=nx.from_pandas_dataframe(df, 'from', 'to' )


def nodesize_return():
    return_val = []
    for i,v in G.degree():
        if v <=2:
            return_val.append(v)
        else:
            return_val.append(v*10)
    return return_val
pos = nx.spring_layout(G)

#edge에 색각을 넣기위해서 nx.draw에는 pos를 쓰지 않아도 되지만 pos를 넣기
nx.draw(G, pos, with_labels=True, node_size=nodesize_return(), node_color="skyblue",  alpha=0.5, linewidths=20, font_family='Malgun Gothic', font_size='8')


#edge 색깔입히기
# pos = nx.random_layout(G)
# nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)


colors = ['AliceBlue','Blue','BlueViolet','Brown','BurlyWood','CadetBlue',
          'Chartreuse','Chocolate','Coral','Cyan','DarkCyan','DarkKhaki','DarkOliveGreen',
          'DarkOrchid','DarkRed','DarkSlateGray','DarkViolet','FireBrick','ForestGreen','Fuchsia','Gold',
          'GreenYellow','HotPink','LightCoral','LightPink','LightSalmon','LightSlateGrey']

#matrixX를 사용해서 edge에 색깔넣기
for inx in range(27):
    nx.draw_networkx_edges(G, pos,
                           edgelist=matrix[inx],
                           width=8, alpha=0.5, edge_color=colors[inx])
plt.show()

