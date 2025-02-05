from aiogram.fsm.state import State, StatesGroup

class UserProfile(StatesGroup):
    weight = State()
    height = State()
    age = State()
    minutes_active = State()
    city = State()

class FoodInfo(StatesGroup):
    amount = State()