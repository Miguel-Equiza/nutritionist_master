

def mifflin_bmr_calculator(weight: float, height: int, age: int, gender = ["Male", "Female"]):
  """
  Weight in kg, height in cm
  """
  gender_constant = {
      "Male": 5,
      "Female": -161
  }

  constant = gender_constant[gender]

  return ((10*weight) + (6.25*height) - (5*age)) + constant

def kathmcardle_bmr_calculator(weight, body_fat: int):
  """
  Body fat in number. E.g: 21
  """
  lean_mass = weight*( 1 - (body_fat / 100))
  return (21.6*lean_mass) + 370

def bmr_calculator(weight, height: int, age, gender, body_fat = 0):
  mifflin_bmr = mifflin_bmr_calculator(weight, height, age, gender)

  if body_fat != 0:
      kathmcardle_bmr = kathmcardle_bmr_calculator(weight, body_fat)
      return (mifflin_bmr+kathmcardle_bmr)/2

  return mifflin_bmr

def calories_calculator(weight, height: int, age, gender, body_fat = 0, activity = ["Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active"]):
  bmr = bmr_calculator(weight, height, age, gender, body_fat)
  activity_multiplier = {
      "Sedentary" : 1.2,
      "Lightly active" : 1.375,
      "Moderately active" : 1.55,
      "Very active" : 1.725,
      "Extra active" : 1.9
  }
  return round(bmr * activity_multiplier[activity],0)

def cutting_kg_loose(weight, type_of_weight_change = ["Slow", "Moderate", "Quick"]):
  bw_percentage_week = {
      "Slow" : 0.005,
      "Moderate" : 0.0075,
      "Quick" : 0.01
  }
  kg_per_week = weight*bw_percentage_week[type_of_weight_change]
  return kg_per_week

def cutting(weight, maintenance_calories, type_of_weight_change = ["Slow", "Moderate", "Quick"]):
  kg_per_week = cutting_kg_loose(weight, type_of_weight_change)
  calorie_deficit_per_day = round((kg_per_week*7500)/7,0)
  print("Rate of: ", kg_per_week, "kg per week of weight loss")
  return maintenance_calories - calorie_deficit_per_day, -round(kg_per_week,2)


def bulking_kgs_gain(n_years_training: int, gender, type_of_weight_change = ["Slow", "Moderate", "Quick"]):
  n_years = int(n_years_training)

  if n_years >=4: kgs_month = [0.225, 0.45]
  elif n_years >=2: kgs_month = [0.45, 0.9]
  else: kgs_month = [0.9, 1.35]

  bulk_multiplier = {
      "Slow" : kgs_month[0],
      "Moderate" : (kgs_month[0] + kgs_month[1])/2,
      "Quick" : kgs_month[1]
  }

  kg_month = bulk_multiplier[type_of_weight_change]

  if gender == "Female": kg_month = kg_month/2
  kg_week = round(kg_month/4,2)

  return kg_week

def bulking(n_years_training: int, maintenance_calories, gender, type_of_weight_change = ["Slow", "Moderate", "Quick"]):
  kg_week = bulking_kgs_gain(n_years_training, gender, type_of_weight_change)
  calorie_surplus_per_day = round((kg_week*7500)/7,0)

  print("Rate of: ", kg_week*4, "kg per month of weight gain")

  return maintenance_calories + calorie_surplus_per_day, round(kg_week,2)



def get_calories(weight: int, height: int, age: int, n_years_training, gender , activity, goal, type_of_weight_change, body_fat = 0):
  assert gender in ["Male", "Female"], "Gender must be Male or Female"
  assert activity in ["Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active"], "Activity must be one of the following: Sedentary, Lightly active, Moderately active, Very active, Extra active"
  assert goal in ["Cut", "Bulk", "Maintenance"], "Goal has to be one of the following: Cut, Bulk, Maintenance"
  assert type_of_weight_change in ["Slow", "Moderate", "Quick"], "Type of weight change has to be one of the following: Slow, Moderate, Quick"

  maintenance_calories = calories_calculator(weight, height, age, gender, body_fat, activity)

  if goal == "Cut": return cutting(weight, maintenance_calories, type_of_weight_change)
  elif goal == "Bulk": return bulking(n_years_training, maintenance_calories, gender, type_of_weight_change)
  else: return maintenance_calories, 0



def macros_cutting(weight, calories, preference_high_fats: bool, preference_high_protein: bool):
  if preference_high_protein: protein_grams = weight*2.5
  else: protein_grams = weight*2.2

  if preference_high_fats: fat_grams = (calories*0.25)/9
  else: fat_grams = (calories*0.15)/9

  carb_grams = (calories - fat_grams*9 - protein_grams*4)/4
  return int(fat_grams), int(carb_grams), int(protein_grams)


def macros_bulking(weight, calories, preference_high_fats: bool, preference_high_protein: bool):
  if preference_high_protein: protein_grams = weight*2.2
  else: protein_grams = weight*1.9

  if preference_high_fats: fat_grams = (calories*0.3)/9
  else: fat_grams = (calories*0.3)/9

  carb_grams = (calories - fat_grams*9 - protein_grams*4)/4
  return int(fat_grams), int(carb_grams), int(protein_grams)

def get_macros(goal, weight, calories, preference_high_fats: bool, preference_high_protein: bool):
  assert goal in ["Cut", "Bulk", "Maintenance"], "Goal has to be one of the following: Cut, Bulk, Maintenance"

  if goal == "Cut": return macros_cutting(weight, calories, preference_high_fats, preference_high_protein)
  else: return macros_bulking(weight, calories, preference_high_fats, preference_high_protein)



def meal_calories(calories, fats, carbs, proteins, min_calories_meal, max_calories_meal, min_meals, max_meals, pre_workout: bool, post_workout: bool, pre_workout_cals, post_workout_cals):
  if post_workout | pre_workout: max_meals -= 1

  meals = {}
  if post_workout:
    calories -= post_workout_cals
    proteins -= 40
  if pre_workout:
    calories -= pre_workout_cals
    carbs -= 60
  for i in range(min_meals, max_meals+1):
    if ((calories - min_calories_meal*i) >= 0) & ((calories - max_calories_meal*i) <= 0): meals[i] = {"calories" : int(calories/i), "fats": int(fats/i), "carbs": int(carbs/i), "proteins": int(proteins/i), "pre_workout": pre_workout, "post_workout": post_workout}
  return meals


def adjust_calories(weight, type_of_weight_change, new_weight, calories, goal, gender):
  assert gender in ["Male", "Female"], "Gender must be Male or Female"
  assert goal in ["Cut", "Bulk", "Maintenance"], "Goal has to be one of the following: Cut, Bulk, Maintenance"
  assert type_of_weight_change in ["Slow", "Moderate", "Quick"], "Type of weight change has to be one of the following: Slow, Moderate, Quick"

  reality_kg = new_weight - weight

  if goal == "Cut": kg_week_goal = cutting_kg_loose(weight, type_of_weight_change)
  elif goal == "Bulk": kg_week_goal = bulking_kgs_gain(n_years_training, gender, type_of_weight_change)
  else: kg_week_goal = 0

  kg_adjust = kg_week_goal - reality_kg
  calories_to_adjust = (7500*kg_adjust)/7 + calories
  if calories_to_adjust>200: calories_to_adjust = 200
  elif calories_to_adjust<200: calories_to_adjust = -200

  return calories

def meals_from_calories(calories, goal, weight, preference_high_fats, preference_high_protein, min_calories_meal, max_calories_meal, min_meals, max_meals, pre_workout, post_workout, pre_workout_cals, post_workout_cals):
  fats, carbs, proteins = get_macros(goal, weight, calories, preference_high_fats, preference_high_protein)
  meals = meal_calories(calories, fats, carbs, proteins, min_calories_meal, max_calories_meal, min_meals, max_meals, pre_workout, post_workout, pre_workout_cals, post_workout_cals)
  return meals
