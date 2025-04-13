import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Set page configuration
st.set_page_config(page_title="PIMA Diabetes Insights", layout="wide")

# Load data
df = pd.read_csv("pima-dataset.csv")

# --- Table: PIMA Dataset Structure ---
num_columns = len(df.columns)
num_rows = len(df)
stats = df.describe().transpose()
columns = df.columns
data_types = [str(df[col].dtype) for col in columns]
unique_counts = [df[col].nunique() for col in columns]
means = [f"{stats.loc[col, 'mean']:.2f}" for col in columns]
mins = [f"{stats.loc[col, 'min']:.2f}" for col in columns]
maxs = [f"{stats.loc[col, 'max']:.2f}" for col in columns]
fig_table = go.Figure(data=[go.Table(
    header=dict(
        values=['Column Name', 'Data Type', 'Unique Values', 'Mean', 'Min', 'Max'],
        fill_color='paleturquoise',
        align='left',
        font=dict(color='black', size=12)  # Set header text to black
    ),
    cells=dict(
        values=[columns, data_types, unique_counts, means, mins, maxs],
        fill_color='lavender',
        align='left',
        font=dict(color='black', size=12)  # Set cell text to black
    ))
])
fig_table.update_layout(
    title=f'PIMA Dataset Structure (Rows: {num_rows}, Columns: {num_columns})',
    width=800, height=400
)

# --- Bar Chart: Average Insulin by Outcome ---
df_clean = df[df['Insulin'] > 0]
insulin_means = df_clean.groupby('Outcome')['Insulin'].mean().reset_index()
insulin_means['Outcome'] = insulin_means['Outcome'].map({0: 'Non-Diabetic', 1: 'Diabetic'})
fig_bar = px.bar(insulin_means, x='Outcome', y='Insulin',
                 title='Average Insulin by Diabetes Outcome',
                 labels={'Insulin': 'Avg Insulin (mu U/ml)'},
                 height=500, width=500)
fig_bar.update_traces(marker_color='teal', text=insulin_means['Insulin'].round(1), textposition='auto')

# --- Heatmap: Correlation Matrix ---
corr = df.corr()
fig_heatmap = go.Figure(data=go.Heatmap(
    z=corr.values.tolist(),
    x=corr.columns.tolist(),
    y=corr.columns.tolist(),
    text=[[f"{val:.2f}" for val in row] for row in corr.values],
    texttemplate="%{text}",
    colorscale='Viridis',
    zmin=-1, zmax=1))
fig_heatmap.update_layout(title='Correlation Heatmap of PIMA Features')

# --- 3D Scatter: Glucose, BMI, Age by Outcome ---
df['Outcome_Color'] = df['Outcome'].map({0: 'red', 1: 'blue'})
fig_3d = px.scatter_3d(df, x='Glucose', y='BMI', z='Age',
                       color='Outcome_Color',
                       hover_data=['Pregnancies'], opacity=0.7,
                       title='3D View: Glucose, BMI, Age by Outcome',
                       color_discrete_map={'red': 'red', 'blue': 'blue'},
                       labels={'Outcome_Color': 'Diabetes (0 = No, 1 = Yes)'},
                       height=800, width=800)
fig_3d.update_traces(marker=dict(size=12, symbol='circle'))
fig_3d.update_layout(scene=dict(aspectmode='data'))


# --- NEW Interactive Scatter + Histogram ---
scatter_data = df[['Glucose', 'BMI', 'Outcome', 'Age']]
age_20_30 = scatter_data[scatter_data['Age'].between(20, 30)]
age_30_40 = scatter_data[scatter_data['Age'].between(30, 40)]
age_40_plus = scatter_data[scatter_data['Age'] >= 40]

fig_interactive = go.Figure()

# Scatter traces for each age range
fig_interactive.add_trace(go.Scatter(
    x=scatter_data['Glucose'], y=scatter_data['BMI'], mode='markers',
    marker=dict(color=scatter_data['Outcome'], colorscale='Tealrose'),
    name='All Ages', hovertemplate='Glucose: %{x}<br>BMI: %{y}<br>Age: %{customdata}',
    customdata=scatter_data['Age'], visible=True))
fig_interactive.add_trace(go.Scatter(
    x=age_20_30['Glucose'], y=age_20_30['BMI'], mode='markers',
    marker=dict(color=age_20_30['Outcome'], colorscale='Tealrose'),
    name='Age 20-30', hovertemplate='Glucose: %{x}<br>BMI: %{y}<br>Age: %{customdata}',
    customdata=age_20_30['Age'], visible=False))
fig_interactive.add_trace(go.Scatter(
    x=age_30_40['Glucose'], y=age_30_40['BMI'], mode='markers',
    marker=dict(color=age_30_40['Outcome'], colorscale='Tealrose'),
    name='Age 30-40', hovertemplate='Glucose: %{x}<br>BMI: %{y}<br>Age: %{customdata}',
    customdata=age_30_40['Age'], visible=False))
fig_interactive.add_trace(go.Scatter(
    x=age_40_plus['Glucose'], y=age_40_plus['BMI'], mode='markers',
    marker=dict(color=age_40_plus['Outcome'], colorscale='Tealrose'),
    name='Age 40+', hovertemplate='Glucose: %{x}<br>BMI: %{y}<br>Age: %{customdata}',
    customdata=age_40_plus['Age'], visible=False))

# Histogram: Age distribution
fig_interactive.add_trace(go.Histogram(
    x=df[df['Outcome'] == 1]['Age'], name='Diabetic Age', opacity=0.7,
    histnorm='percent', visible=False))
fig_interactive.add_trace(go.Histogram(
    x=df[df['Outcome'] == 0]['Age'], name='Non-Diabetic Age', opacity=0.7,
    histnorm='percent', visible=False))

# Age filter buttons
age_buttons = [
    dict(label='All Ages', method='update',
         args=[{'visible': [True, False, False, False, False, False]},
               {'title': 'All Ages: Glucose vs. BMI'}]),
    dict(label='Age 20-30', method='update',
         args=[{'visible': [False, True, False, False, False, False]},
               {'title': 'Age 20-30: Glucose vs. BMI'}]),
    dict(label='Age 30-40', method='update',
         args=[{'visible': [False, False, True, False, False, False]},
               {'title': 'Age 30-40: Glucose vs. BMI'}]),
    dict(label='Age 40+', method='update',
         args=[{'visible': [False, False, False, True, False, False]},
               {'title': 'Age 40+: Glucose vs. BMI'}]),
    dict(label='Age Distribution', method='update',
         args=[{'visible': [False, False, False, False, True, True]},
               {'title': 'Age Distribution by Outcome'}])
]

# Update layout for interactive figure
fig_interactive.update_layout(
    updatemenus=[dict(active=0, buttons=age_buttons, x=1.2, y=1.1)],
    title='All Ages: Glucose vs. BMI',
    height=600, width=800,
    showlegend=True,
    barmode='overlay'
)

# --- Streamlit Layout ---
st.title("Live Demo: PIMA Diabetes Insights")

st.header("Dataset Structure")
st.plotly_chart(fig_table, use_container_width=True)

st.header("Average Insulin by Outcome")
st.plotly_chart(fig_bar, use_container_width=True)

st.header("Correlation Heatmap")
st.plotly_chart(fig_heatmap, use_container_width=True)

st.header("3D Scatter: Glucose, BMI, Age")
st.plotly_chart(fig_3d, use_container_width=True)

# st.header("2D Scatter: Glucose vs BMI")
# st.plotly_chart(fig_2d, use_container_width=True)

st.header("Interactive Scatter & Age Distribution")
st.plotly_chart(fig_interactive, use_container_width=True)


# # --- 2D Scatter: Glucose vs BMI by Outcome ---
# df_filtered = df.dropna(subset=['Glucose', 'BMI', 'Age', 'Outcome'])
# df_filtered['Outcome_Color'] = df_filtered['Outcome'].map({0: 'green', 1: 'blue'})
# fig_2d = px.scatter(df_filtered, x='Glucose', y='BMI',
#                     color='Outcome_Color',
#                     text='Outcome',
#                     hover_data=['Pregnancies', 'Age'],
#                     title='Glucose vs BMI by Outcome')