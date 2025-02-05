from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import UserProfile
from utils import calculate_calories_norm, calculate_water_norm

from utils import CALORIES_PER_MINUTE

from api_srvices import get_temperature

router = Router()

# Handler of /help
@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply(
        "Available Commands:\n"
        "/set_profile - Set up your profile info \n"
        "/check_pregress - Check current progress'n"
    )

# Handler of /set_profile
@router.message(Command("set_profile"))
async def start_setting_profile(message: Message, state: FSMContext):
    await message.reply("Please enter your weight (in kgs):")
    await state.set_state(UserProfile.weight)

@router.message(UserProfile.weight)
async def process_weight(message: Message, state: FSMContext):
    weight = message.text
    try:
        weight = int(weight)
        await state.update_data(weight=weight)
        await state.set_state(UserProfile.height)
        await message.answer("Enter your height (cm):")
    except:
        await message.answer("Weight should be a whole number. Please try again:")
    
@router.message(UserProfile.height)
async def process_height(message: Message, state: FSMContext):
    height = message.text
    try:
        height = int(height)
        await state.update_data(height=height)
        await state.set_state(UserProfile.age)
        await message.answer("Enter your age:")
    except:
        await message.answer("Height should be a whole number. Please try again:")

@router.message(UserProfile.age)
async def process_age(message: Message, state: FSMContext):
    age = message.text
    try:
        age = int(age)
        await state.update_data(age=age)
        await state.set_state(UserProfile.minutes_active)
        await message.answer("How many minutes of activity do you get per day?")
    except:
        await message.answer("Age should be a whole number. Please try again:")

@router.message(UserProfile.minutes_active)
async def process_minutes_active(message: Message, state: FSMContext):
    minutes_active = message.text
    try:
        minutes_active = int(minutes_active)
        await state.update_data(minutes_active=minutes_active)
        await state.set_state(UserProfile.city)
        await message.answer("In which city are you based?")
    except:
        await message.answer("This should be a whole number in minutes. Please try again:")

@router.message(UserProfile.city)
async def process_city(message: Message, state: FSMContext):
    users = router.users
    city = message.text
    await state.update_data(city=city)

    city_temp = await get_temperature(city)
    is_hot = 0
    if city_temp >= 25:
        is_hot = 1

    data = await state.get_data()

    weight = data.get("weight")
    height = data.get("height")
    age = data.get("age")
    minutes_active = data.get("minutes_active")

    water_goal = calculate_water_norm(weight, minutes_active, is_hot)
    calorie_goal = calculate_calories_norm(weight, height, age)

    await message.answer("Profile has been set up! Your stats: \n"
                         f"Weight: {weight} kg\n"
                         f"Height: {height} cm\n"
                         f"Age: {age}\n"
                         f"Minutes active per day: {minutes_active}\n"
                         f"City: {city}\n"
                         f"Current city temp: {city_temp} °С\n"
                         f"Water goal: {water_goal} ml\n"
                         f"Calories goal: {calorie_goal} calories \n")
    
    user_id = message.from_user.id

    users[user_id] = {
        "weight": weight,
        "height": height,
        "age": age,
        "activity": minutes_active,
        "city": city,
        "water_goal": water_goal,
        "calorie_goal": calorie_goal,
        "logged_water": 0,
        "logged_calories": 0,
        "burned_calories": 0
    }

    await state.clear()

@router.message(Command("check_progress"))
async def cmd_check_progress(message: Message):
    user_id = message.from_user.id
    users = router.users
    if user_id not in users:
        await message.reply("Your profile has not been set yet.")
    else:

        user_data = users[user_id]

        await message.reply("Progress:\n"
                      "Water:\n"
                      f"- Consumed: {user_data['logged_water']} ml from {user_data['water_goal']} ml\n"
                      f"- Left: {max(0, user_data['water_goal'] - user_data['logged_water'])} ml\n"
                      "\n\n"
                      "Calories:\n"
                      f"- Consumed: {user_data['logged_calories']} kcal\n"
                      f"- Burned: {user_data['burned_calories']} kcal\n"
                      f" - Balance: {user_data['logged_calories'] - user_data['burned_calories']} from"
                      f" {user_data['calorie_goal']} kcal.")


@router.message(Command("log_water"))
async def cmd_log_water(message: Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer("Please provide the number of water. Usage: /log_water <number of ml>")
        return
    
    user_id = message.from_user.id
    users = router.users
    if user_id not in users:
        await message.reply("Your profile has not been set yet.")
        return

    user_data = users[user_id]

    try:
        logged_water_ml = int(parts[1])
        user_data['logged_water'] += logged_water_ml
        await message.answer(f"- Logged {logged_water_ml} ml of water\n"
                             f"- Consumed: {user_data['logged_water']} ml from {user_data['water_goal']} ml")
    except ValueError:
        await message.answer("Invalid input. Please provide a valid number.")

@router.message(Command("log_workout"))
async def cmd_log_workout(message: Message):
    
    parts = message.text.split()
    if len(parts) != 3:
        await message.answer("Please provide the number of water. Usage: /log_workout <workout> <time in minutes>")
        return
    
    user_id = message.from_user.id
    users = router.users
    if user_id not in users:
        await message.reply("Your profile has not been set yet.")
        return

    user_data = users[user_id]
    
    workout, duration = parts[1], parts[2]

    if workout not in CALORIES_PER_MINUTE:
        await message.answer("This type of workout is not supported")
        return
    
    try: 
        duration = int(duration)
    except ValueError:
        await message.answer("Invalid input. Please provide a integer number for the duration, representing time spent in minutes.")
        return

    burned_calories = CALORIES_PER_MINUTE[workout] * duration
    additional_water = (duration * 10)
    await message.reply(f"Workout {workout} for {duration} minutes - {burned_calories} kcal.\n"
                  f"Additional: drink {additional_water} more ml of water.")
    
    user_data['burned_calories'] += burned_calories
    user_data['water_goal'] += additional_water

    return
    
@router.message(Command("log_food"))
async def cmd_log_workout(message: Message):
    pass
