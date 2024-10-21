import streamlit as st
import pandas as pd
from io import BytesIO
from diet_logic.diet_maker import *
from diet_logic.meals_dict import *

# Set up a form to accept all input variables
st.title("Personal Fitness Parameters")

with st.form("fitness_form"):
    # Accepting integer inputs
    weight = st.number_input("Weight (kg)", min_value=1, value=78, step=1, format="%i")
    height = st.number_input("Height (cm)", min_value=1, value=168, step=1, format="%i")
    age = st.number_input("Age (years)", min_value=1, value=23, step=1, format="%i")

    # Add a checkbox to toggle whether the number input is required
    body_fat = st.number_input("Input your body fat if you know it, if not leave it as 0", value=0, step=1)

    # Accepting float input for years of training
    n_years_training = st.number_input("Years of Training", min_value=0.0, value=5.0, step=0.1)

    # Accepting dropdown inputs for list-based variables
    gender = st.selectbox("Gender", ["Male", "Female"], index=0)
    activity = st.selectbox("Activity Level", ["Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active"], index=0)
    goal = st.selectbox("Goal", ["Cut", "Bulk", "Maintenance"], index=0)
    type_of_weight_change = st.selectbox("Type of Weight Change", ["Slow", "Moderate", "Quick"], index=0)

    # Boolean preference inputs
    preference_high_fats = st.selectbox("Preference for High Fats", [False, True], index=0)
    preference_high_protein = st.selectbox("Preference for High Protein", [False, True], index=0)
    pre_workout = st.selectbox("Use Pre-Workout Supplement", [False, True], index=0)
    post_workout = st.selectbox("Use Post-Workout Supplement", [False, True], index=0)

    with st.expander("Advanced settings for professionals"):
        cals = st.number_input("Enter the calories you want", min_value=0)
        lote = st.number_input("Select grams of protein per kg of bodyweight")


    # Submit button
    submitted = st.form_submit_button("Submit")

min_calories_meal = 500
max_calories_meal = 1000
min_meals = 3
max_meals = 5
pre_workout_cals = 300
post_workout_cals = 200

if submitted:
    # Collect data into a list of tuples (Feature, Value)
    user_data = [
        ("Weight (kg)", weight),
        ("Height (cm)", height),
        ("Age (years)", age),
        ("Years of Training", n_years_training),
        ("Gender", gender),
        ("Activity Level", activity),
        ("Goal", goal),
        ("Type of Weight Change", type_of_weight_change),
        ("Preference for High Fats", preference_high_fats),
        ("Preference for High Protein", preference_high_protein),
        ("Use Pre-Workout Supplement", pre_workout),
        ("Use Post-Workout Supplement", post_workout)
    ]

    # Convert to DataFrame with two columns: 'Feature' and 'Value'
    df = pd.DataFrame(user_data, columns=["Feature", "Value"])

    # Display the submitted data
    st.write("Here are your inputs:")
    st.dataframe(df)

    calories, kg_per_week = get_calories(weight, height, age, n_years_training, gender, activity, goal, type_of_weight_change, body_fat)
    fats, carbs, proteins = macros_cutting(weight, calories, preference_high_fats, preference_high_protein)
    meals = meal_calories(calories, fats, carbs, proteins, min_calories_meal, max_calories_meal, min_meals, max_meals, pre_workout, post_workout, pre_workout_cals, post_workout_cals)
    new_data = generate_specific_meals(meals)
    all_ingredients_df = pd.DataFrame(comida)
    meals_df = get_meals_df(all_ingredients_df, new_data)

    st.write("Here are your diets:")
    st.dataframe(meals_df)

    # Function to convert DataFrame to Excel and return as BytesIO object
    def to_excel(df, meals_df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='User_Data')
            unique_n_meals = meals_df['n_meals'].unique()
            for n in unique_n_meals:
                df_subset = meals_df[meals_df['n_meals'] == n]
                df_subset.to_excel(writer, sheet_name=f'n_meals_{n}', index=False)
        processed_data = output.getvalue()
        return processed_data

    # Convert DataFrame to Excel and store it in memory
    xlsx_data = to_excel(df, meals_df)

    # Create a download button for the Excel file
    st.download_button(label='Download Excel file',
                       data=xlsx_data,
                       file_name='user_data.xlsx',
                       mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
