import datetime
import calendar
from keyboa import Keyboa
from telebot import types


def habits_keyboard():
    habits_buttons = [{"Add new habit":"new_habit"}, {"Change progress":"progress_habit"},
                              {"Edit":"edit_habit"}, {"Delete":"delete_habit"}]
    keyboard = Keyboa(habits_buttons, items_in_row=2).keyboard 
    return keyboard

def goals_keyboard():
    goals_buttons = [{'Add new goal': 'new_goal'}, {'Change progress': 'progress_goal'},
                 {'Edit': 'edit_goal'}, {'Delete': 'delete_goal'}]
    keyboard = Keyboa(goals_buttons, 2).keyboard
    return keyboard

def tasks_keyboard():
    buttons = [{'add new task': 'new_task'}, {'change progress': 'progress_task'}, 
                   {'edit': 'edit_task'}, {'delete': 'delete_task'}, {'change deadline': 'changedeadline_task'}]
    keyboard = Keyboa(buttons, 2).keyboard 
    return keyboard

def progress_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
    to_do = types.InlineKeyboardButton('to do')
    in_progress = types.InlineKeyboardButton('in progress')
    done = types.InlineKeyboardButton('done')
    keyboard.add(to_do, in_progress, done)
    return keyboard

def time_keyboard():
    buttons = [{'add time' : 'add_time'}, {'skip':'skip'}]
    keyboard = Keyboa(buttons, 2).keyboard
    return keyboard
    
 ###################################  creating keyboards  ###############################
def create_year_keyboard():
    current_year = datetime.datetime.today().year
    year_buttons = [i for i in range(current_year, current_year + 4)]
    year_keyboard = Keyboa(items=year_buttons, back_marker = '@year', items_in_row=2, copy_text_to_callback=True).keyboard
    return year_keyboard

def create_months_keyboard():
    month_buttons = []
    for i in range(1,13):
        button = {}
        button[calendar.month_name[i]] = str(i)
        month_buttons.append(button)
    month_keyboard = Keyboa(items=month_buttons, items_in_row=3, back_marker='@month').keyboard
    return month_keyboard
   
def create_days_keyboard(selected_date):
    days_of_week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    days_of_week_kb = Keyboa(items=days_of_week, items_in_row=7).keyboard
    selected_date = selected_date.split('-')
    days = calendar.monthcalendar(int(selected_date[0]), int(selected_date[1]))
    day_buttons = []
    for week in days:
        week = list(map(str, week))
        for i in range(len(week)):
            if week[i] == '0':
                week[i] = ' '
        day_buttons.append(week)
    day_keyboard = Keyboa(items=day_buttons, back_marker='@day', copy_text_to_callback=True).keyboard
    month_calendar_keyboard = Keyboa.combine(keyboards=(days_of_week_kb, day_keyboard))
    return month_calendar_keyboard

