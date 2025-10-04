from aiogram.fsm.state import State, StatesGroup


class ParserStates(StatesGroup):
    """Состояния FSM для парсера"""
    waiting_for_link = State()
