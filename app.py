import streamlit as st
import data
import visualization

# Set page configuration
st.set_page_config(page_title="Glucose Guardian Live Demo", layout="wide")

# Initialize database
data.init_db()

# Load and clean data
df = data.load_data()
df = data.clean_data(df)

# st.header("Manage Patient Records")

# # Add Record
# st.subheader("Add New Record")
# with st.form("add_patient"):
#     pregnancies = st.number_input("Pregnancies", min_value=0, max_value=17, step=1)
#     glucose = st.number_input("Glucose", min_value=0, max_value=200, step=1)
#     blood_pressure = st.number_input("BloodPressure", min_value=0, max_value=122, step=1)
#     skin_thickness = st.number_input("SkinThickness", min_value=0, max_value=99, step=1)
#     insulin = st.number_input("Insulin", min_value=0, max_value=846, step=1)
#     bmi = st.number_input("BMI", min_value=0.0, max_value=67.1, step=0.1)
#     dpf = st.number_input("DiabetesPedigreeFunction", min_value=0.0, max_value=2.42, step=0.01)
#     age = st.number_input("Age", min_value=21, max_value=81, step=1)
#     outcome = st.selectbox("Outcome", [0, 1])
#     submitted = st.form_submit_button("Add Record")
#     if submitted:
#         record = {
#             "Pregnancies": pregnancies,
#             "Glucose": glucose,
#             "BloodPressure": blood_pressure,
#             "SkinThickness": skin_thickness,
#             "Insulin": insulin,
#             "BMI": bmi,
#             "DiabetesPedigreeFunction": dpf,
#             "Age": age,
#             "Outcome": outcome
#         }
#         if data.add_record(record):
#             st.success("Record added successfully!")
#             last_record = data.get_last_record()
#             if last_record is not None:
#                 st.subheader("Last Added Record")
#                 st.dataframe(last_record, hide_index=True)
#         # Reload data to reflect changes
#         st.session_state.df = data.load_data()
#         st.session_state.df = data.clean_data(st.session_state.df)

# # Update Record
# st.subheader("Update Existing Record")
# with st.form("update_patient"):
#     record_id = st.number_input("Record ID (rowid)", min_value=1, step=1)
#     update_glucose = st.number_input("New Glucose", min_value=0, max_value=200, step=1, key="update_glucose")
#     update_bmi = st.number_input("New BMI", min_value=0.0, max_value=67.1, step=0.1, key="update_bmi")
#     submitted = st.form_submit_button("Update Record")
#     if submitted:
#         update_data = {"Glucose": update_glucose, "BMI": update_bmi}
#         if data.update_record(record_id, update_data):
#             st.success(f"Record {record_id} updated successfully!")
#         # Reload data
#         st.session_state.df = data.load_data()
#         st.session_state.df = data.clean_data(st.session_state.df)

# # Delete Record
# st.subheader("Delete Record")
# with st.form("delete_patient"):
#     delete_id = st.number_input("Record ID (rowid) to Delete", min_value=1, step=1)
#     submitted = st.form_submit_button("Delete Record")
#     if submitted:
#         if data.delete_record(delete_id):
#             st.success(f"Record {delete_id} deleted successfully!")
#         # Reload data
#         st.session_state.df = data.load_data()
#         st.session_state.df = data.clean_data(st.session_state.df)

# # Display Current Data (Optional, for verification)
# st.subheader("Current Records")
# if "df" in st.session_state and st.session_state.df is not None:
#     st.dataframe(st.session_state.df.head())
# else:
#     df = data.load_data()
#     df = data.clean_data(df)
#     st.session_state.df = df
#     st.dataframe(df.head() if df is not None else [])

# --- Streamlit Layout ---
st.title("Glucose Guardian Live Demo")

# Dataset Structure
st.header("Dataset Structure")
fig_table = visualization.create_dataset_table(df)
if fig_table:
    st.plotly_chart(fig_table, use_container_width=True)
else:
    st.error("Failed to load dataset table.")

# Average Insulin by Outcome
st.header("Average Insulin by Outcome")
fig_bar = visualization.create_insulin_bar(df)
if fig_bar:
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.error("Failed to load insulin bar chart.")

# Correlation Heatmap
st.header("Correlation Heatmap")
fig_heatmap = visualization.create_correlation_heatmap(df)
if fig_heatmap:
    st.plotly_chart(fig_heatmap, use_container_width=True)
else:
    st.error("Failed to load correlation heatmap.")

# 3D Scatter: Glucose, BMI, Age
st.header("3D Scatter: Glucose, BMI, Age")
fig_3d = visualization.create_3d_scatter(df)
if fig_3d:
    st.plotly_chart(fig_3d, use_container_width=True)
else:
    st.error("Failed to load 3D scatter plot.")

# 2D Scatter: Glucose vs BMI
st.header("2D Scatter: Glucose vs BMI")
fig_2d = visualization.create_2d_scatter(df)
if fig_2d:
    st.plotly_chart(fig_2d, use_container_width=True)
else:
    st.error("Failed to load 2D scatter plot.")


# Age-Wise Diabetes Prevalence
st.header("Age-Wise Diabetes Prevalence")
fig_trend = visualization.create_age_prevalence_line(df)
if fig_trend:
    st.plotly_chart(fig_trend, use_container_width=True)
else:
    st.error("Failed to load age prevalence line chart.")

# Diabetes Prevalence by Pregnancies
st.header("Diabetes Prevalence by Pregnancies")
fig_preg = visualization.create_pregnancies_prevalence_bar(df)
if fig_preg:
    st.plotly_chart(fig_preg, use_container_width=True)
else:
    st.error("Failed to load pregnancies prevalence bar chart.")

# Parallel Coordinates Plot
st.header("Parallel Coordinates: Glucose, BMI, Age")
fig_parallel = visualization.create_parallel_coordinates(df)
if fig_parallel:
    st.plotly_chart(fig_parallel, use_container_width=True)
else:
    st.error("Failed to load parallel coordinates plot.")

# Interactive Scatter & Age Distribution
st.header("Interactive Scatter & Age Distribution")
fig_interactive = visualization.create_interactive_scatter(df)
if fig_interactive:
    st.plotly_chart(fig_interactive, use_container_width=True)
else:
    st.error("Failed to load interactive scatter plot.")