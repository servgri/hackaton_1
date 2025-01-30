from aiogram.fsm.state import State, StatesGroup

# Определяем состояния для FSM
class Form(StatesGroup):
    phrase = State()
    author = State()


