import streamlit as st

# Set up a form to accept all input variables
st.title("Personal Fitness Parameters")

with st.form("fitness_form"):
    # Accepting integer inputs
    weight = st.number_input("Weight (kg)", min_value=1, value=78, step=1, format="%i")
    height = st.number_input("Height (cm)", min_value=1, value=168, step=1, format="%i")
    age = st.number_input("Age (years)", min_value=1, value=23, step=1, format="%i")

    # Accepting float input for years of training
    n_years_training = st.number_input("Years of Training", min_value=0.0, value=5.0, step=0.1)

    # Accepting dropdown inputs for list-based variables
    gender = st.selectbox("Gender", ["Male", "Female"], index=0)
    activity = st.selectbox("Activity Level", ["Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active"], index=0)
    goal = st.selectbox("Goal", ["Cut", "Bulk", "Maintenance"], index=0)
    type_of_weight_change = st.selectbox("Type of Weight Change", ["Slow", "Moderate", "Quick"], index=0)

    # Boolean preference inputs
    preference_high_fats = st.selectbox("Preference for High Fats", ["False", "True"], index=0)
    preference_high_protein = st.selectbox("Preference for High Protein", ["False", "True"], index=0)
    pre_workout = st.selectbox("Use Pre-Workout Supplement", ["False", "True"], index=0)
    post_workout = st.selectbox("Use Post-Workout Supplement", ["False", "True"], index=0)

    # Submit button
    submitted = st.form_submit_button("Submit")

# Output the inputs after submission
if submitted:
    st.write("Here are your inputs:")
    st.write(f"Weight: {weight} kg")
    st.write(f"Height: {height} cm")
    st.write(f"Age: {age} years")
    st.write(f"Years of Training: {n_years_training} years")
    st.write(f"Gender: {gender}")
    st.write(f"Activity Level: {activity}")
    st.write(f"Goal: {goal}")
    st.write(f"Type of Weight Change: {type_of_weight_change}")
    st.write(f"Preference for High Fats: {preference_high_fats}")
    st.write(f"Preference for High Protein: {preference_high_protein}")
    st.write(f"Use Pre-Workout Supplement: {pre_workout}")
    st.write(f"Use Post-Workout Supplement: {post_workout}")
