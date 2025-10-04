from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

common_router = Router()


@common_router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """Обработчик команды /start"""
    from encar_bot.states import ParserStates
    from encar_bot.utils.formatters import get_welcome_message

    await message.answer(get_welcome_message(), parse_mode="HTML")
    await state.set_state(ParserStates.waiting_for_link)


@common_router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    from encar_bot.utils.formatters import get_help_message

    await message.answer(get_help_message(), parse_mode="HTML")


@common_router.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    """Обработчик команды /cancel"""
    await state.clear()
    await message.answer(
        "❌ Операция отменена. Отправьте /start для начала работы.", parse_mode="HTML"
    )
