import time
import random
import math
import sys

gold = 20
wood = 10
stone = 10
food = 10
population = 5
happiness = 50
max_weight = 0
turns = 1
chance_weight = []

perm_ban = []

gold_bonus = 1
stone_bonus = 1
wood_bonus = 1
food_bonus = 1

current_buildings = [['mines', 0], ['farm', 0], ['logging', 1], ['housing', 1]]
building_info = [
    ['mines', [
        5, #gold
        0, #stone
        10, #wood
        10, #food
    ],
    "global gold,wood,stone, food, population, happiness; stone += math.floor(random.randint(3, 10) * stone_bonus); gold += math.floor(1 * gold_bonus)",
    ["stone", "gold"]
    ],
    ['farm', [
        5, #gold
        10, #stone
        10, #wood
        0, #food
    ],
    "global gold,wood,stone, food, population, happiness; food += math.floor(random.randint(3, 10) * food_bonus)",
    ["food"]
    ],
    ['logging', [
        5, #gold
        10, #stone
        0, #wood
        10, #food
    ],
    "global gold,wood,stone, food, population, happiness; wood += math.floor(random.randint(2, 7) * wood_bonus)",
    ["wood"]
    ],
    ['housing', [
        5, #gold
        10, #stone
        10, #wood
        10, #food
    ],
    "home_func()",
    ["population"]
    ],
]
rows = 3
columns = 3

blocked_list = []

market_db = [
    [["stone", "stone"], [1, 2], [3, 1]], #[buy amount, buy price],[sell amount, sell price]
    [["wood", "wood"], [1, 2], [3, 1]],
    [["food", "food"], [1, 2], [3, 1]],
    [["wellfare (happiness)", "happiness"], [10, 40], [None, None]],
    [["villager (population)", 'population'], [1, 25], [1, 2]],
]

events = [
    ['random_settlers', [
        5,
        ["Random settlers are wanting to join you! What do you say, lets let them in!"],
        [
            ["Let them in!",
                [
                    "print('New people are joining your settlement!')",
                    "population += 5; print('+5 Population')"
                ]
            ],
            ["Deny their entry!",
                [
                    "print('Its your word! Not everyone can get in right?')",
                ]
            ],
            ["Make them pay a fee!",
                [
                    "print('Our settlement grows in wealth! They are not happy about this though...')",
                    "population += 5; print('+5 Population')",
                    "gold += 20; print('+20 Gold')",
                    "happiness -= 10; print('-10 Happiness')"
                ]             
            ]
        ],
        True
    ]],
    ['bountiful_harvest', [
        5,
        ["You found a bountiful harvest!"],
        [
            ["Accept!",
                [
                    "print('Hooray!!')",
                    "food += 20; print('+20 Food')"
                ]
            ],
            ["Discard!",
                [
                    "print('Not sure why you did that, but sure I suppose.')",
                ]
            ]
        ],
        True
    ]],
    ['dragon_attack', [
        1,
        ["A dragon attacks your settlement! He asks for gold or he will eat your people!"],
        [
            ["Pay gold (200)",
                [
                    "print('The dragon licked up the shiny coins and flew away.')",
                    "gold -= 200; print('-200 Gold')"
                ]
            ],
            ["Decline",
                [
                    "print('In a fit of rage, the dragon gobbled up half of your people!')",
                    "print('-' + str(math.floor(population * 0.5)) + ' Population'); population = math.floor(population * 0.5)"
                ]
            ],
            ["Attempt to fight",
                [
                    "special_events('dragon_fight')"
                ]
            ]
        ],
        False
    ]],
    ['conquest', [
        1,
        ["Stand ready for my arrival, worm! You were given orders, you were given time, you were given more leeway than most."],
        [
            ["Bow to the Viltrum Empire",
                [
                    "print('Good.'); global perm_ban; perm_ban.append('conquest')",
                ]
            ],
            ["Fight Back",
                [
                    "print('To be honest, I want you to resist.')",
                    "print('Conquest obliterates your settlement')",
                    "print('-' + str(population - 1) + ' Population'); population = 1"
                ]
            ]
        ],
        False
    ]],
    ['market_boom', [
        1,
        ["An explosion occured inside of the market"],
        [
            ["Spend resources to rebuild.",
                [
                    "print('Rebuilding efforts are on their way!')",
                    "print('-2 Population'); population -= 2",
                    "print('-10 Wood'); wood -= 10",
                    "print('-10 Stone'); stone -= 2",
                    "print('+10 Gold'); gold += 10",
                    "print('+10 Happiness'); happiness += 10"
                ]
            ],
            ["Leave it be.",
                [
                    "print('The people will not be happy about this.')",
                    "print('-2 Population'); population -= 2",
                    "print('-10 Happiness'); happiness -= 10"

                ]
            ]
        ],
        False
    ]],
    ['false_prophet', [
        2,
        ["A man is rambling about his 'great' ecnomic policies."],
        [
            ["Listen to him",
                [
                    "print('Bad idea...')",
                    "print('-10 Wood'); wood -= 10",
                    "print('-10 Stone'); stone -= 10",
                    "print('-10 Gold'); gold -= 10",
                    "print('-10 Happiness'); happiness -= 10"
                ]
            ],
            ["Throw him in jail",
                [
                    "print('No one listens to his crazy ideas. The days go on.'); global perm_ban; perm_ban.append('false_prophet')"
                ]
            ],
            ["Do the opposite",
                [
                    "print('That worked..?')",
                    "print('+10 Wood'); wood += 10",
                    "print('+10 Stone'); stone += 10",
                    "print('+10 Gold'); gold += 10",
                    "print('+5 Happiness'); happiness += 5"
                ]
            ]
        ],
        False
    ]],
    ['trade_group', [
        3,
        ["A trade caravan travels by your empire. They bring upon trading opportunities!"],
        [
            ["Trade 20 gold for 25 food",
                [
                    "special_events('trade_caravan', 1)"
                ]
            ],
            ["Trade 20 gold for 20 stone",
                [
                    "special_events('trade_caravan', 2)"
                ]
            ],
            ["Trade 20 gold for 30 wood",
                [
                    "special_events('trade_caravan', 3)"
                ]
            ],
            ["Decline",
                [
                    "print('The group leaves. Maybe next time.')"
                ]
            ]
        ],
        False
    ]],
]

def special_events(event_type, a):
    global gold,wood,stone, food, population, happiness, perm_ban

    if event_type == "dragon_fight":
        chance = math.floor(99 - ((population * 0.16) ** 1.5)) + 1
        if (chance < 2):
            chance = 2
        if random.randint(1, chance) == 1:
            print("Your army has successfully slain the dragon!")
            print('-' + str(math.floor(population * 0.2)) + " Population"); population = math.floor(population * 0.8)
            food += 300; print('+300 Food')
            gold += 200; print('+200 Gold')
            perm_ban.append("dragon_attack")
        else:
            print('The dragon was too powerful for your forces...')
            print('-' + str(math.floor(population * 0.8)) + " Population"); population = math.floor(population * 0.2)
            gold -= 200; print('-200 Gold')

    if event_type == "trade_caravan":
        value = None
        amount = 0
        if check_cost(20,0,0,0):
            if a == 1:
                amount = 25
                value = "food"
            if a == 2:
                amount = 20
                value = "stone"
            if a == 3:
                amount = 30
                value = "wood"
            exec("global " + value + ";" + value + "+= " + str(amount))
            gold -= 20
            print("+" + str(amount) + " " + value.capitalize())
            print("-20 Gold")
        else:
            print("They laugh at how poor you are.")


def populate_weight():
    global chance_weight
    global max_weight
    current_arithmetic = 0

    for value in events:
        max_weight += value[1][0]
    
    for value in events:
        event_name = value[0]
        weight = value[1][0]
        low = current_arithmetic + 1
        high = current_arithmetic
        for i in range(weight):
            high += 1
        
        current_arithmetic = high
        chance_weight.append([event_name, [low, high]])

def get_event(num):
    for value in chance_weight:
        event_name = value[0]
        low = value[1][0]
        high = value[1][1]
        if (low <= num and high >= num):
            return event_name

def can_int(v):
    try:
        int(v)
        return True
    except ValueError:
        return False

def get_user_input(max):
    valid = False

    while not valid:
        bad_input = False
        inputed = (input())

        if can_int(inputed):
            inputed = int(inputed)
            if (inputed <=0 or inputed > max):
                bad_input = True
        else:
            bad_input = True

        if bad_input:
            print("Invalid input, try again with a number ranging from 1 to " + str(max))
        else:
            valid = True
            return inputed

def run_event(event):
    global gold,wood,stone, food, population, happiness

    print()
    data = event[1]
    print(data[1])
    for i, option in enumerate(data[2]):
        option_text = option[0]
        print(i + 1, option_text)
    inputed_num = get_user_input(len(data[2]))
    print()
    for i, option in enumerate(data[2]):
        if inputed_num == i + 1:
            option_text = option[0]
            options_code = option[1]
            for code_snippet in options_code:
                code_snippet = "global gold,wood,stone, food,population, happiness;" + code_snippet
                exec(code_snippet)
def log_current():
    print("Gold: " + str(gold))
    print("Stone: " + str(stone))
    print("Wood: " + str(wood))
    print("Food: " + str(food))
    print("Population: " + str(population))
    print("Happiness: " + str(happiness))

def do_events():
    global blocked_list

    random_num = random.randint(1, max_weight)
    event_name = get_event(random_num)
    for event in events:
        if event[0] == event_name:
            in_list = False
            for string in blocked_list:
                if string == event[0]:
                    in_list = True
            for string in perm_ban:
                if string == event[0]:
                    in_list = True
            if in_list:
                do_events()
            else:
                run_event(event)
                if not event[1][3]:
                    blocked_list.append(event[0])           

def check_cost(gold_val, stone_val, wood_val, food_val):
    good_val = True

    if gold < gold_val:
        good_val = False
    if stone < stone_val:
        good_val = False
    if wood < wood_val:
        good_val = False
    if food < food_val:
        good_val = False

    return good_val

def home_func():
    global population, happiness
    if population > 1 and population < current_buildings[3][1] * 8:
        r = random.randint(1, math.floor(population / 4))
        population += r
    else:
        happiness -= 1

def create_new_building():
    global gold,wood,stone, food, population, happiness
    print("What would you like to make? [mines, farm, logging, homes]; Press 0 to back")
    type_input = str(input()).lower().strip()
    if type_input == "mines" or type_input == "farm" or type_input == "logging" or type_input == "homes":
        used_data = []
        for building_data in building_info:
            if building_data[0] == type_input:
                used_data = building_data
        print("Creating " + type_input)
        print("Gold Needed: " + str(used_data[1][0]) + " (" + str(gold) + ")")
        print("Stone Needed: " + str(used_data[1][1]) + " (" + str(stone) + ")")
        print("Wood Needed: " + str(used_data[1][2]) + " (" + str(wood) + ")")
        print("Food Needed: " + str(used_data[1][3]) + " (" + str(food) + ")")
        print()
        print('1 to build; 2 to return')
        if (get_user_input(2) == 1):
            if (check_cost(used_data[1][0], used_data[1][1], used_data[1][2], used_data[1][3])):
                for building in current_buildings:
                    if building[0] == type_input:
                        building[1] = building[1] + 1
                        gold -= used_data[1][0]
                        stone -= used_data[1][1]
                        wood -= used_data[1][2]
                        food -= used_data[1][3]
            else:
                print("Insufficient Resources")
        else:
            print("back")
    else:
        if type_input != "0":
            print("Invalid input.")
            create_new_building()

def manage_func():
    turn_done = False

    while not turn_done:
        print();print();print()
        print("Managing Settlement")
        print("1. View Current Buildings")
        print("2. Build New Building")
        print("3. Exit")
        inputed_value = get_user_input(4)
        
        if inputed_value == 1:
            for building_arr in current_buildings:
                name = building_arr[0]
                amount = building_arr[1]
                print(name + ": " + str(amount))
            print()
            print("Input to exit")
            input()
        elif inputed_value == 2:
            create_new_building()
        elif inputed_value == 3:
            turn_done = True

def buy_market():
    turn_done = False
    while not turn_done:
        print();print();print()
        print("Buy Goods")
        for index, value in enumerate(market_db):
            print(str(index + 1) + ". Purchase " + str(value[1][0]) + " " + value[0][0] + " for " + str(value[1][1]) + " gold")
        print(str(len(market_db) + 1) + ". Exit")

        inputed_value = get_user_input(len(market_db) + 1)
        
        if inputed_value == len(market_db) + 1:
            turn_done = True
        else:
            for value in market_db:
                if value == market_db[inputed_value - 1]:
                    print("How many times would you like to buy " + value[0][0] + "?")
                    user_input = get_user_input(999)

                    if (user_input * value[1][1]) < gold:
                        for i in range(user_input):
                            exec("global " + value[0][1] + ";" + value[0][1] + "+= " + str(value[1][0]))
                            exec("global gold; gold -= " + str(value[1][1]))
                    else:
                        print()
                        print("Not enough gold")
                        time.sleep(0.5)

def sell_market():
    turn_done = False
    while not turn_done:
        print();print();print()
        print("Buy Goods")
        cleaned = []
        for value in market_db:
            if (value[2][0] != None):
                cleaned.append(value)
        for index, value in enumerate(cleaned):
            print(str(index + 1) + ". Sell " + str(value[2][0]) + " " + value[0][0] + " for " + str(value[2][1]) + " gold")
        print(str(len(cleaned) + 1) + ". Exit")

        inputed_value = get_user_input(len(cleaned) + 1)
        
        if inputed_value == len(cleaned) + 1:
            turn_done = True
        else:
            for value in cleaned:
                if value == cleaned[inputed_value - 1]:
                    print("How many times do you want to sell " + value[0][0] + "?")
                    user_input = get_user_input(999)
                    
                    if eval(value[0][1] + ">= user_input * " + str(value[2][0])):
                        print(); print()
                        print("Sold " + str(user_input * value[2][0]) + " " + value[0][1] + " for " + str(value[2][1] * user_input) + " gold" )
                        exec("global " + value[0][1] + "; " + value[0][1] + "-= " + str(user_input * value[2][0]))
                        exec("global gold; gold +=" + str(value[2][1] * user_input))
                        time.sleep(0.4)
                        log_current()
                    else:
                        print()
                        print("Not enough " + value[0][1])
                        time.sleep(0.5)

def market_func():
    turn_done = False
    while not turn_done:
        print();print();print()
        print("The Market")
        print("1. Buy Goods")
        print("2. Sell Goods")
        print("3. Buy Advancements")
        print("4. Exit")
        inputed_value = get_user_input(4)
        
        if inputed_value == 1:
            buy_market()
        elif inputed_value == 2:
            sell_market()
        elif inputed_value == 3:
            print("buy upgrades")
        elif inputed_value == 4:
            turn_done = True

def storage_func():
    log_current()
    print()
    print("Input to exit")
    input()
    
def end_turn_func():
    global gold,wood,stone, food, population, happiness

    working_citizens = population
    print("Meals are eaten!")
    r = random.randint(math.floor(population / 2), population)
    print("-" + str(r) + " Food")
    time.sleep(1)
    food -= r
    if gold < 0:
        print("Your kingdom is in a recession! People are leaving!")
        print("-5 Happiness"); happiness -= 5
        print("-" + str(math.floor(population * 0.1) + 1) + " Population"); population -= math.floor(population * 0.1) + 1
        time.sleep(1)

    if happiness < 0:
        print("Your citizens are depressed! People are leaving!")
        print("-" + str(math.floor(population * 0.1) + 1) + " Population"); population -= math.floor(population * 0.1) + 1
        time.sleep(1)

    if food < 0:
        print("Your citizens are starving! People are leaving!")
        print("-" + str(math.floor(population * 0.1) + 1) + " Population"); population -= math.floor(population * 0.1) + 1
        time.sleep(1)
    old_gold = gold
    old_wood = wood
    old_food = food
    old_stone = stone
    old_population = population

    for buildings in current_buildings:
        if buildings[1] > 0:
            num_times = buildings[1]
            if (num_times > working_citizens):
                print("Not enough workers for " + buildings[0])
            else:
                for b_func in building_info:
                    if buildings[0] == b_func[0]:
                        for _ in range(num_times):
                            working_citizens -= 1
                            exec(b_func[2])
                        print("The " + buildings[0] + " corp are hard at work!")
                        for value in b_func[3]:
                            v1, v2 = eval(value), eval("old_" + value)
                            print("+" + str((v1-v2)) + " " + value.capitalize())
                        time.sleep(1.5)
    
    if random.randint(1, 3):
        print("A random event had occured in the night!")
        time.sleep(1)
        do_events()

def game_func():
    global turns, blocked_list
    print("Day " + str(turns))
    time.sleep(1)
    if turns < 11:
        blocked_list = []
        turns += 1
        for i in range(3):
            turn_done = False

            while not turn_done:
                if population < 1:
                    print("Your kingdom has collapsed! Population is too low!")
                    sys.exit()
                print();print();print()

                print("What would you like to do?")
                print("1. Manage Settlement")
                print("2. Visit the Market")
                print("3. View Storage")
                print("4. Pass Time")
                inputed_value = get_user_input(4)
                
                if inputed_value == 1:
                    manage_func()
                elif inputed_value == 2:
                    market_func()
                elif inputed_value == 3:
                    storage_func()
                elif inputed_value == 4:
                    turn_done = True
            print("Time passes by...")
            time.sleep(1)
            do_events()
            time.sleep(1)
            print()
            print("Time passes by...")
            time.sleep(1)
        print("The day is calm.")
        time.sleep(1)
        end_turn_func()
        print()
        time.sleep(0.5)
        log_current()
        time.sleep(2)
        game_func()

populate_weight()
game_func()
