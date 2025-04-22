flavors = ["vanilla", "chocolate", "strawberry", "banana", "mint chocolate", "superman", "bubblegum"]

print("Name your favorite icecream flavor!!! all lowercase")

def check_for_flavor(user_input):
    has_flavor = False
    for flavor in flavors:
        if user_input == flavor:
            has_flavor = True
    return has_flavor

flavor_input = str(input())

if check_for_flavor(flavor_input):
    print("I love " + flavor_input + ", it is my favorite flavor too!")
else:
    print("Never heard of it!")