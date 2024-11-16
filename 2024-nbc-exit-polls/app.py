import pandas as pd
import plotly.graph_objects as pgo

df = pd.read_csv('nbc-exit-polls.csv')
df['harris'] = df['percent'] * df['harris']
df['trump'] = df['percent'] * df['trump']
df = df.drop('percent', axis=1)
df = df.melt(id_vars=['race', 'gender'], var_name='candidate', value_name='total')
df.fillna('m&f2', inplace=True)
df['vote'] = df['race'] + ' ' + df['gender'] + ': ' + df['candidate']

harris = df[df['candidate'] == 'harris']
harris['color rgb'] = '99, 110, 250'
for i, index in enumerate(harris.index):
    harris.loc[index, 'alpha'] = 0.95 * (1 - i/len(harris.index))


trump = df[df['candidate'] == 'trump']
trump['color rgb'] = '239, 85, 59'
for i, index in enumerate(trump.index):
    trump.loc[index, 'alpha'] = 1 - (i/len(trump.index))
trump = trump.iloc[::-1]  # reversed

df = pd.concat([harris, trump])
df['color'] = 'rgba(' + df['color rgb'] + ', ' + df['alpha'].astype(str) + ')'
print(df)


fig = pgo.Figure(
    data=[pgo.Pie(
        labels=df['vote'],
        values=df['total'],
        marker={
            'colors': df['color'],
        },
        textinfo='label+percent',
        rotation=-df.loc[0, 'total'] * 360,
        sort=False,
    )]
)
fig.update_layout(
    title=dict(
        text="2024 NBC Exit Polls: Contribution by Sex and Race (excluding third party)",
        font=dict(
            size=24,
        ),
    ),
)
fig.write_html('index.html', auto_open=True)
