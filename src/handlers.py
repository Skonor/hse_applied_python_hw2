from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import UserProfile

router = Router()


# Handler of /help
@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply(
        "Доступные команды:\n"
        "/set_profile - Установка профиля \n"
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
        await state.update_data(aminutes_active=minutes_active)
        await state.set_state(UserProfile.city)
        await message.answer("In which city are you based?")
    except:
        await message.answer("This should be a whole number in minutes. Please try again:")

@router.message(UserProfile.city)
async def process_city(message: Message, state: FSMContext):
    city = message.text
    await state.update_data(city=city)
    data = await state.get_data()
    await message.answer("Profile has been set up! Your stats: \n"
                         f"Weight: {data.get("weight")} kg\n"
                         f"Height: {data.get("height")} cm\n"
                         f"Age: {data.get("age")}\n"
                         f"Minutes active per day: {data.get("minutes_active")}\n"
                         f"City: {data.get("city")}")
    await state.clear()