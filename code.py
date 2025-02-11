import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
#создание датафреймов
df_valid = pd.read_excel('/home/lis/Mishnev/tim_task/валид.xlsx', usecols = 'A,C', skiprows = 1)
df_valid = df_valid.drop(0).reset_index(drop = True)
df_valid['Class '] = df_valid['Class '].str.strip() 
df_valid = df_valid.sort_values(by = 'Class ')

df_test_sum = pd.read_excel('/home/lis/Mishnev/tim_task/сумма.xlsx', usecols = 'A,B,C', skiprows = 1, names = ['Class ', 'Images_test', 'Images_sum'])
df_test_sum = df_test_sum.sort_values(by = 'Class ')

df_sum = pd.DataFrame()
df_merged = pd.merge(df_valid, df_test_sum[['Class ', 'Images_test']], on = 'Class ', how = 'outer', suffixes = ('_df_valid', '_df_test_sum'))
df_merged.fillna(0, inplace=True)
df_sum['Class '] = df_merged['Class ']
df_sum['Кол-во дефектов'] = df_merged['Instances'] + df_merged['Images_test']
df_sum = df_sum.sort_values(by = 'Class ')

# создание графиков
fig = make_subplots(rows=4, cols=2, subplot_titles=("Валидационные данные","Валид+Сумм", "Тестовые данные","Тест+Сумм", "Суммарные данные", "Валид+Общие","Общие данные", "Тест+Общие"))

#создание одиночных графиков
fig.add_trace(go.Bar(x=df_valid['Class '], y=df_valid['Instances'], name='Валидационные данные'), row=1, col=1)
fig.add_trace(go.Bar(x=df_test_sum['Class '], y=df_test_sum['Images_test'], name='Тестовые данные'), row=2, col=1)
fig.add_trace(go.Bar(x=df_sum['Class '], y=df_sum['Кол-во дефектов'], name='Суммарные данные'), row=3, col=1)
fig.add_trace(go.Bar(x=df_test_sum['Class '], y=df_test_sum['Images_sum'], name='Общие данные'), row=4, col=1)

#создание парных графиков
fig.add_trace(go.Bar(x=df_valid['Class '], y=df_valid['Instances'], opacity = 0.4, name='Валидационные данные',marker_color='red'), row=1, col=2)
fig.add_trace(go.Bar(x=df_sum['Class '], y=df_sum['Кол-во дефектов'], opacity = 0.4, name='Суммарные данные'), row=1, col=2)

fig.add_trace(go.Bar(x=df_test_sum['Class '], y=df_test_sum['Images_test'],opacity = 0.4,  name='Тестовые данные'), row=2, col=2)
fig.add_trace(go.Bar(x=df_sum['Class '], y=df_sum['Кол-во дефектов'],opacity = 0.4,  name='Суммарные данные'), row=2, col=2)

fig.add_trace(go.Bar(x=df_valid['Class '], y=df_valid['Instances'], opacity = 0.4, name='Валидационные данные'), row=3, col=2)
fig.add_trace(go.Bar(x=df_test_sum['Class '], y=df_test_sum['Images_sum'], opacity = 0.4, name='Общие данные'), row=3, col=2)

fig.add_trace(go.Bar(x=df_test_sum['Class '], y=df_test_sum['Images_test'],opacity = 0.4,  name='Тестовые данные'), row=4, col=2)
fig.add_trace(go.Bar(x=df_test_sum['Class '], y=df_test_sum['Images_sum'], opacity = 0.4, name='Общие данные'), row=4, col=2)

fig.update_layout(height=2500, width=1200, barmode = 'overlay',legend_orientation="h", 
                  margin=dict(l=0, r=0, t=20, b=0))
fig.show()