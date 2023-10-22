from aiogram.dispatcher.filters.state import State, StatesGroup


class CourseDescription(StatesGroup):
    description = State()


class Phone(StatesGroup):
    phone = State()