from aiogram.fsm.state import State, StatesGroup

# Определяем состояния для FSM
class Form(StatesGroup):
    style = State()
    genre = State()
    era = State()
    author = State()
