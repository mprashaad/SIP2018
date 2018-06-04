"""Initialisations"""
token = "614243243:AAH0x8jTgg2zP6YACQB1J9NxeWLq041mTHE"

user_types = ["Participant", "Facilitator"]

part_funcs = ["Check Uru", "Unlock Uru Caches", "Forge Catalogue", "Side Heroes", "Items"]

facil_funcs = ["Check Uru", "Add Uru", "Forge Catalogue", "Forge Item", "Side Heroes",\
               "Unlock Side Hero", "Items"]

main_heroes = ["Iron Man", "Thor", "Dr Strange", "Rocket"]

main_hero_powers = {"Iron Man": "Deep Copy: Select one station in the Amazing Race before\
 attempting it. If you successfully complete the station, you get triple the number of keys.",
                    
                    "Thor": "Thunderstorm: 30 extra water bombs for Wet Games.",
                    
                    "Dr Strange": "Paralysing Mist: All mutant lifeforms freeze for 30 seconds when \
activated during Night Games.",
                    
                    "Rocket": "Whack It and It Works: One code/puzzle is solved for you in the \
Escape Room."
    }

side_heroes = ["Groot", "Black Panther", "Winter Soldier", "Scarlet Witch", "Falcon", "Vision",
                 "Heimdall"]

side_hero_powers = {"Groot": "Organic Picking: Three caches opened without a key)",
                    
                    "Black Panther": "Upgrade tools with vibranium (e.g. limited edition tool \
unobtainable via any other means)",
                    
                    "Winter Soldier": "Break a code",
                    
                    "Scarlet Witch": "Manipulate probability of successful tool creation\
(e.g. guaranteed creation)",

                    "Falcon": "Transport a message of certain number of words to another room",

                    "Vision": "Create new reaction pathway that requires less Uru for making the \
tool (e.g. 50% discount)",

                    "Heimdall": "Transport one scientist to another room for limited period of time"
    }

hero_codes = {"circleoflight":"Iron Man", "lightning&thunder":"Thor", \
              "smoke&mirrors":"Dr Strange", "YOLO":"Rocket"}

stations =["Icebreaker 1", "Icebreaker 2", "Icebreaker 3", "Icebreaker 4", \
           "Icebreaker 5", "Icebreaker 6"]

num_codes = [i for i in range(1,7)]

facil_codes = dict([(num_codes[i],stations[i]) for i in range(len(stations))])

registry = []

hero_groups = {"Iron Man":[], "Thor":[], "Dr Strange": [], "Rocket": []}

facil_list = []

uru = {"Iron Man":0, "Thor":0, "Dr Strange": 0, "Rocket": 0}

unlocked_side_heroes = {"Iron Man":[], "Thor":[], "Dr Strange": [], "Rocket": []}

box = ["LyhfL3TC", "bfMSMgJF", "JhYVTFWj", "fDqJaFun", "YA97juKd", "MDLQUzVa",
"gKMLMdwu", "cjcCBcuX", "jHm56dYT", "8BRmnKgM", "PqNqzQ6f", "5DJcEhw9",
"hpSfsNkS", "p5qbjrj9", "9f9etA4J", "bLbwSBNQ", "Zbn78GHg", "VkW4kd56", "PHAzQ4Tq",
"WfdFRcXS"]

boxes = dict([(i, 20) for i in box])

keys = ["HJ56mH9k", "pKRgw8dX", "H5XvtBUb", "yTrEdvRW", "RNGBdxmP", "CfvG9rvh", 
"J9KDdAsY", "DTF5LgyN", "RC7k82W7", "j8F62mPX", "hU3VKxSe", "RxzuLuX7", 
"gUpmGHHs", "T64p3QsD", "n3qprHvN", "AbeKzFdk", "NA3quBQe", "GBdTZAye", 
"JjvfGdDu", "6DZ9M7L2"]

forge_items = {
    "A":[1,30],
    "B": [2,50]
    }

forged_items = {"Iron Man":[], "Thor":[], "Dr Strange": [], "Rocket": []}

help_info = "In case of emergencies, please contact the following personnel:\n\
Campus Security: 6874 1616\n\
Camp Directors: Si Yue (---) or Sherilyn (---)"

"""Accessors"""
def is_facil(user):
    for i in facil_list:
        if i[0] == user:
            return True
    return False

def is_part(user):
    for i in registry:
        if i == user:
            if not is_facil(user):
                return True
    return False

def is_user(user):
    for i in registry:
        if i == user:
            return True
    return False

def is_key(key):
    return key in keys

def is_box(cache):
    return cache in box

def team_uru(team):
    return uru[team]

def what_group_user(user):
    for i in main_heroes:
        for e in hero_groups[i]:
            if e == user:
                return i
            
def what_group_id(user):
    for i in main_heroes:
        for e in hero_groups[i]:
            if user == e.id:
                return i
            
def what_station(user):
    for i in facil_list:
        if user == i[0]:
            return facil_codes[i[1]]

"""BASIC SETUP"""
from telegram.ext import Updater, CommandHandler, MessageHandler, \
     Filters, CallbackQueryHandler, ConversationHandler
import telegram
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', \
                    level=logging.INFO)
logger = logging.getLogger(__name__)

"""CREATION OF TABLES"""
def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

"""FILTERS"""
from telegram.ext import BaseFilter

class GenFilter(BaseFilter):
    def __init__(self, *keys):
        self.key = [i for i in keys]
    def filter(self, message):
        for i in self.key:
            if i in message.text:
                return True
        return False

codefilter = GenFilter("code ")
addfilter = GenFilter("add ")
unlockfilter = GenFilter("unlock ")
unlocksideherofilter = GenFilter("unlock side hero ")
forgefilter = GenFilter("forge ")

"""BUTTON CONTENTS"""
def make_buttons(lis):
    menu = [telegram.InlineKeyboardButton(i, callback_data=i) for i in lis]
    return telegram.InlineKeyboardMarkup(build_menu(menu, n_cols=2))

"""CallbackQueries"""
def button(bot, update):
    query = update.callback_query
    bot.answer_callback_query(query.id)
    data = query.data
    callback_dic[data](bot,update)

def func1(bot,update):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id=query.message.message_id
    bot.edit_message_text("Selected option: {}".format(query.data),chat_id, message_id)
    bot.sendMessage(chat_id, "Please key in your team code as: code <code>")

def func2(bot,update):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id=query.message.message_id
    bot.edit_message_text("Selected option: {}".format(query.data),chat_id, message_id)
    bot.sendMessage(chat_id, "Please key in your facilitator code as: code <code>")

def func3(bot,update):
    query = update.callback_query
    chat_id = query.message.chat_id
    try:
        bot.sendMessage(chat_id, "Your team currently has {} \
Uru.".format(uru[what_group_id(chat_id)]))
    except KeyError:
        bot.sendMessage(chat_id, "You are not part of any team.")

def func4(bot,update):
    query = update.callback_query
    chat_id = query.message.chat_id
    bot.sendMessage(chat_id, "Please key in codes as: unlock <cache> <key>")

def unlock_box(bot, update):
    cache, key = update.message.text[7:].split(" ")
    user = update.message.from_user
    if is_part(user):
        if is_box(cache):
            if is_key(key):
                team, amt = what_group_user(user), boxes[cache]
                uru[team] += amt
                team_message(bot, "A cache has been unlocked and {} Uru has been \
obtained.".format(amt), team)
                box.remove(cache)
                keys.remove(key)
            else:
                update.message.reply_text("The key code is incorrect or has been used already.")                
        else:
            update.message.reply_text("The cache code is incorrect or has been used already.")
    else:
        update.message.reply_text("Only participants can unlock caches.")

def func5(bot,update): #does not work
    query = update.callback_query
    chat_id = query.message.chat_id
    bot.send_document(chat_id, document= open("sample.pdf", "rb"), timeout=20)

def func6(bot,update):
    query = update.callback_query
    chat_id = query.message.chat_id
    if unlocked_side_heroes[what_group_id(chat_id)] == []:
        bot.sendMessage(chat_id, "Your team has not unlocked any side heroes.")
    else:
        sh = unlocked_side_heroes[what_group_id(chat_id)]
        bot.sendMessage(chat_id, "{}".format("\n".join(sh)))

def func7(bot,update):
    query = update.callback_query
    chat_id = query.message.chat_id
    bot.sendMessage(chat_id, "Please key in amount as: add <team> <amount>")

def add_uru(bot, update):
    msg = update.message.text[4:].split(" ")
    amt = msg.pop()
    team = " ".join(msg)
    user = update.message.from_user
    if not (team in main_heroes):
        update.message.reply_text("Please correct the team name. Please key\
 in amount as: add <team> <amount>")
        return
    try:
        amt = int(amt)
    except:
        update.message.reply_text("Please key in an integer for the amount. Please key\
 in amount as: add <team> <amount>")
        return
    if is_facil(user):
        uru[team] += amt
        update.message.reply_text("{} Uru has successfully been added to team {}.".format(\
            amt,team))
        team_message(bot, "{} Uru has been obtained from {}."\
                     .format(amt, what_station(user)), team)
    else:
        update.message.reply_text("Only facilitators can add Uru.")

def func8(bot,update):
    query = update.callback_query
    chat_id = query.message.chat_id
    bot.sendMessage(chat_id, "Please key in details as: forge <item>&<team>&\
<cost>")

def forge(bot, update):
    item, team, cost = update.message.text[6:].split("&")
    user = update.message.from_user
    if is_facil(user):
        if not (item in forge_items):
            update.message.reply_text("The item's name is incorrect or the item is not \
available. Please key in details as: forge <item>&<team>&<cost>")
            return
        elif not (team in main_heroes):
            update.message.reply_text("Please correct the team's name. Please key in \
details as: forge <item>&<team>&<cost>")
            return
        else:
            try:
                cost = int(cost)
            except:
                update.message.reply_text("The cost cannot be recognised. \
        Please key in details as: forge <item>&<team>&<cost>")
                return
            if cost > uru[team]:
                update.message.reply_text("Team {} has insufficient Uru.".format(team))
                return
            forged_items[team] += item
            uru[team] -= cost
            update.message.reply_text("{} has been added to team {}.".format(\
                item,team))
            team_message(bot, "{} has been added to your team's items at a cost of {} Uru."\
                         .format(item, cost),team)
            forge_items[item][0] -= 1
            if forge_items[item][0] <= 0:
                         del forge_items[item]
    else:
        update.message.reply_text("Only facilitators can forge items.")

def func9(bot,update):
    query = update.callback_query
    chat_id = query.message.chat_id
    bot.sendMessage(chat_id, "Please key in details as: unlock side hero <team>&<side hero>")

def unlock_side_hero(bot, update):
    team, sh = update.message.text[17:].split("&")
    user = update.message.from_user
    if not (sh in side_heroes):
        update.message.reply_text("The side hero's name is incorrect or the side hero is not \
available. Please key in details as: unlock side hero <team>&<side hero>")
        return
    elif not (team in main_heroes):
        update.message.reply_text("Please correct the team's name. Please key in \
details as: unlock side hero <team>&<side hero>")
        return
    elif is_facil(user):
        unlocked_side_heroes[team].append(sh)
        update.message.reply_text("{} has successfully joined team {}.".format(\
            sh,team))
        team_message(bot, "{} has joined your team. {}"\
                     .format(sh, side_hero_powers[sh]),team)
        side_heroes.remove(sh)
    else:
        update.message.reply_text("Only facilitators can unlock side heroes.")

def func10(bot,update):
    query = update.callback_query
    chat_id = query.message.chat_id
    if forged_items[what_group_id(chat_id)] == []:
        bot.sendMessage(chat_id, "You have no items")
    else:
        bot.sendMessage(chat_id, "{}".format("\n".join(forged_items\
                                                       [what_group_id(chat_id)])))

callback_dic ={"Participant": func1,
               "Facilitator": func2,
               "Check Uru": func3,
               "Unlock Uru Caches": func4,
               "Forge Catalogue": func5,
               "Side Heroes": func6,
               "Add Uru": func7,
               "Forge Item": func8,
               "Unlock Side Hero": func9,
               "Items": func10
               }

"""Mass Messaging"""
def facil_message(bot, message):
    for user in facil_list:
        bot.sendMessage(user.id, message)

def part_message(bot,message):
    for user in registry:
        bot.sendMessage(user.id, message)

def team_message(bot, message, team):
    for user in hero_groups[team]:
        bot.sendMessage(user.id, message)

"""Registration"""
def codeword(bot, update):
    code = update.message.text[5:]
    user = update.message.from_user
    if user in registry:
        update.message.reply_text("You have already registered.")
        return
    try:
        code = int(code)
        if code == 0:
            logger.info("Code is 0")
            registry.append(user)
            update.message.reply_text("You have registered successfully.")
        elif code in facil_codes.keys():
            if not is_facil(user):
                facil_list.append((user,code))
                logger.info("{} was added to facilitator list".format(user))
                update.message.reply_text("Please key in your team code as: code <code>")
            else:
                update.message.reply_text("Please key in your team code as: code <code>")
    except:
        if code in hero_codes.keys():
            team = hero_codes[code]
            hero_groups[team].append(user)
            logger.info("{} was added to {}".format(user, team))
            registry.append(user)
            update.message.reply_text("You have registered successfully into \
team {}.".format(team))
            update.message.reply_text("{}".format(main_hero_powers[team]))
        else:
            update.message.reply_text("Invalid code. Please key in your code as: code <code>")

"""Commands"""
def start(bot, update):
    update.message.reply_text("Welcome to SIP 2018. Nice to meet you, \
{}!".format(update.message.from_user.first_name))
    update.message.reply_text("Are you a participant or facilitator?"\
                              ,reply_markup=make_buttons(user_types))

def options(bot,update):
    user = update.message.from_user
    if is_facil(user):
        update.message.reply_text("Please choose an option.",reply_markup=make_buttons(\
            facil_funcs))
    elif is_user(user):
        update.message.reply_text("Please choose an option.",reply_markup=make_buttons(\
            part_funcs))
    else:
         update.message.reply_text("Please register first. Use the /start command.")

def helpful_info(bot,update):
    update.message.reply_text("{}".format(help_info))

"""Main Code"""
def main():
    updater = Updater(token = "614243243:AAH0x8jTgg2zP6YACQB1J9NxeWLq041mTHE")
    dispatcher = updater.dispatcher
    print("Bot Started")

    start_handler = CommandHandler("start", start)
    options_handler = CommandHandler("options", options)
    help_handler = CommandHandler("help", helpful_info)
    buttons_handler = CallbackQueryHandler(button)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(buttons_handler)
    dispatcher.add_handler(options_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(MessageHandler(Filters.text & unlocksideherofilter, \
                                          unlock_side_hero))
    dispatcher.add_handler(MessageHandler(Filters.text & codefilter, codeword))
    dispatcher.add_handler(MessageHandler(Filters.text & unlockfilter, unlock_box))
    dispatcher.add_handler(MessageHandler(Filters.text & addfilter, add_uru))
    dispatcher.add_handler(MessageHandler(Filters.text & forgefilter, forge))
    
    updater.start_polling()
    updater.idle()

"""Run Statement"""
if __name__ == '__main__':
    main()
