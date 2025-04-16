import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import config

def create_dataset_table(df):
    if df is None or df.empty:
        return None
    try:
        num_columns = len(df.columns)
        num_rows = len(df)
        stats = df.describe().transpose()
        columns = df.columns.tolist()
        data_types = [str(df[col].dtype) for col in columns]
        unique_counts = [df[col].nunique() for col in columns]
        means = [f"{stats.loc[col, 'mean']:.2f}" if col in stats.index else "N/A" for col in columns]
        mins = [f"{stats.loc[col, 'min']:.2f}" if col in stats.index else "N/A" for col in columns]
        maxs = [f"{stats.loc[col, 'max']:.2f}" if col in stats.index else "N/A" for col in columns]

        fig = go.Figure(data=[go.Table(
            header=dict(
                values=['Column Name', 'Data Type', 'Unique Values', 'Mean', 'Min', 'Max'],
                fill_color='paleturquoise',
                align='left',
                font=dict(color='black', size=12)
            ),
            cells=dict(
                values=[columns, data_types, unique_counts, means, mins, maxs],
                fill_color='lavender',
                align='left',
                font=dict(color='black', size=12)
            )
        )])
        fig.update_layout(
            title=f'PIMA Dataset Structure (Rows: {num_rows}, Columns: {num_columns})',
            width=config.TABLE_WIDTH,
            height=config.TABLE_HEIGHT
        )
        return fig
    except Exception as e:
        print(f"Error creating table: {e}")
        return None

def create_insulin_bar(df):
    if df is None or df.empty:
        return None
    df_clean = df[df['Insulin'] > 0]
    insulin_means = df_clean.groupby('Outcome')['Insulin'].mean().reset_index()
    insulin_means['Outcome'] = insulin_means['Outcome'].map({0: 'Non-Diabetic', 1: 'Diabetic'})
    fig = px.bar(insulin_means, x='Outcome', y='Insulin',
                 title='Average Insulin by Diabetes Outcome',
                 labels={'Insulin': 'Avg Insulin (mu U/ml)'},
                 height=config.BAR_HEIGHT, width=config.BAR_WIDTH)
    fig.update_traces(marker_color='teal', text=insulin_means['Insulin'].round(1), textposition='auto')
    return fig

def create_correlation_heatmap(df):
    if df is None or df.empty:
        return None
    corr = df.corr()
    fig = go.Figure(data=go.Heatmap(
        z=corr.values.tolist(),
        x=corr.columns.tolist(),
        y=corr.columns.tolist(),
        text=[[f"{val:.2f}" for val in row] for row in corr.values],
        texttemplate="%{text}",
        colorscale='Viridis',
        zmin=-1, zmax=1))
    fig.update_layout(title='Correlation Heatmap of PIMA Features')
    return fig

def create_3d_scatter(df):
    """Create 3D scatter plot of Glucose, BMI, Age by Outcome."""
    if df is None or df.empty:
        return None
    df['Outcome_Color'] = df['Outcome'].map({0: 'red', 1: 'blue'})
    fig = px.scatter_3d(df, x='Glucose', y='BMI', z='Age',
                        color='Outcome_Color',
                        hover_data=['Pregnancies'], opacity=0.7,
                        title='3D View: Glucose, BMI, Age by Outcome',
                        color_discrete_map={'red': 'red', 'blue': 'blue'},
                        labels={'Outcome_Color': 'Diabetes (0 = No, 1 = Yes)'},
                        height=config.SCATTER_3D_HEIGHT, width=config.SCATTER_3D_WIDTH)
    fig.update_traces(marker=dict(size=12, symbol='circle'))
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig

def create_2d_scatter(df):
    if df is None or df.empty:
        return None
    df_filtered = df.dropna(subset=['Glucose', 'BMI', 'Age', 'Outcome'])
    df_filtered['Outcome_Color'] = df_filtered['Outcome'].map({0: 'red', 1: 'blue'})
    fig = px.scatter(df_filtered, x='Glucose', y='BMI',
                     color='Outcome_Color',
                     text='Outcome',
                     hover_data=['Pregnancies', 'Age'],
                     title='Glucose vs BMI by Outcome')
    return fig


def create_age_prevalence_line(df):
    """Create line chart of diabetes prevalence by age."""
    if df is None or df.empty:
        return None
    age_trends = df.groupby('Age')['Outcome'].mean().reset_index()
    age_trends.columns = ['Age', 'Diabetes Prevalence']
    age_trends['Diabetes Prevalence'] *= 100

    fig = px.line(age_trends, x='Age', y='Diabetes Prevalence',
                  title='Age-Wise Diabetes Prevalence (%)',
                  labels={'Diabetes Prevalence': 'Prevalence (%)'},
                  markers=True)
    fig.update_traces(line=dict(color='purple'), marker=dict(size=8))
    fig.update_layout(yaxis_range=[0, 100])
    return fig

def create_pregnancies_prevalence_bar(df):
    if df is None or df.empty:
        return None
    df_clean = df.copy()
    df_clean['Pregnancies'] = df_clean['Pregnancies'].apply(lambda x: min(x, 10))
    preg_trends = df_clean.groupby('Pregnancies')['Outcome'].mean().reset_index()
    preg_trends['Outcome'] *= 100

    fig = px.bar(preg_trends, x='Pregnancies', y='Outcome',
                 title='Diabetes Prevalence by Pregnancies (%)',
                 labels={'Outcome': 'Prevalence (%)', 'Pregnancies': 'Number of Pregnancies'})
    fig.update_traces(marker_color='purple', text=preg_trends['Outcome'].round(1), textposition='auto')
    fig.update_layout(yaxis_range=[0, 100], bargap=0.2)
    return fig

def create_parallel_coordinates(df):
    if df is None or df.empty:
        return None
    fig = px.parallel_coordinates(
        df,
        dimensions=['Glucose', 'BMI', 'Age'],
        color='Outcome',
        title='Comparison of Diabetes-Positive vs. Diabetes-Negative Groups',
        labels={'Outcome': 'Diabetes (0 = No, 1 = Yes)',
                'Glucose': 'Glucose Level',
                'BMI': 'Body Mass Index',
                'Age': 'Age'},
        color_continuous_scale=px.colors.diverging.Tealrose
    )
    fig.update_layout(coloraxis_colorbar_title='Diabetes Outcome')
    return fig

def create_interactive_scatter(df):
    if df is None or df.empty:
        return None
    scatter_data = df[['Glucose', 'BMI', 'Outcome', 'Age']]
    age_20_30 = scatter_data[scatter_data['Age'].between(20, 30)]
    age_30_40 = scatter_data[scatter_data['Age'].between(30, 40)]
    age_40_plus = scatter_data[scatter_data['Age'] >= 40]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=scatter_data['Glucose'], y=scatter_data['BMI'], mode='markers',
        marker=dict(color=scatter_data['Outcome'], colorscale='Tealrose'),
        name='All Ages', hovertemplate='Glucose: %{x}<br>BMI: %{y}<br>Age: %{customdata}',
        customdata=scatter_data['Age'], visible=True))
    fig.add_trace(go.Scatter(
        x=age_20_30['Glucose'], y=age_20_30['BMI'], mode='markers',
        marker=dict(color=age_20_30['Outcome'], colorscale='Tealrose'),
        name='Age 20-30', hovertemplate='Glucose: %{x}<br>BMI: %{y}<br>Age: %{customdata}',
        customdata=age_20_30['Age'], visible=False))
    fig.add_trace(go.Scatter(
        x=age_30_40['Glucose'], y=age_30_40['BMI'], mode='markers',
        marker=dict(color=age_30_40['Outcome'], colorscale='Tealrose'),
        name='Age 30-40', hovertemplate='Glucose: %{x}<br>BMI: %{y}<br>Age: %{customdata}',
        customdata=age_30_40['Age'], visible=False))
    fig.add_trace(go.Scatter(
        x=age_40_plus['Glucose'], y=age_40_plus['BMI'], mode='markers',
        marker=dict(color=age_40_plus['Outcome'], colorscale='Tealrose'),
        name='Age 40+', hovertemplate='Glucose: %{x}<br>BMI: %{y}<br>Age: %{customdata}',
        customdata=age_40_plus['Age'], visible=False))
    fig.add_trace(go.Histogram(
        x=df[df['Outcome'] == 1]['Age'], name='Diabetic Age', opacity=0.7,
        histnorm='percent', visible=False))
    fig.add_trace(go.Histogram(
        x=df[df['Outcome'] == 0]['Age'], name='Non-Diabetic Age', opacity=0.7,
        histnorm='percent', visible=False))

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

    fig.update_layout(
        updatemenus=[dict(active=0, buttons=age_buttons, x=1.2, y=1.1)],
        title='All Ages: Glucose vs. BMI',
        height=config.INTERACTIVE_HEIGHT,
        width=config.INTERACTIVE_WIDTH,
        showlegend=True,
        barmode='overlay'
    )
    return fig