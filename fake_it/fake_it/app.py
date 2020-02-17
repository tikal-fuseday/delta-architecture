from random import randint
from faker import Faker
from time import sleep

from fake_it.models import Voter, Poll

POSSIBLE_ACTIONS = ("insert", "update", "answer_poll")

from random import randint

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def main():
    while True:
        action = random.choice(POSSIBLE_ACTIONS)
        if action == "insert":
            insert_fake_voter()
        elif action == "update":
            update_random_voter()
        elif action == "answer_poll":
            answer_random_poll()
        # I don't know if this actually works
        sleep(random(10))

def random_race():
    return choice(('Ashkenazi', "Spharadi", "Mix", "Goy", "Smolani Boged"))

def random_gender():
    return choice(('m','f','t','n'))

def random_bibist():
    return choice(('y','n'))

def insert_fake_voter():
    Voter(
        id=str(random_with_N_digits(9)),
        name=Faker.name(),
        address=Faker.address(),
        gender=random_gender(),
        race=random_race(),
        bibist=random_bibist(),
    ).create()

def update_random_voter():
    voter = Voter.random()
    if choice((True, False)):
        voter.race = random_race()
    if choice((True, False)):
        voter.bibist = random_bibist()
    voter.save()

def answer_random_poll():
    voter = Voter.random()
    Poll(
        voter_id=voter.id,
        answer=choice(("Bibi", "Gantz", "Benet", "Emet", "Meshutefet", "Dosim"))
    ).create()
