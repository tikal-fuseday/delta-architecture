from random import randint, choice
from faker import Faker
from time import sleep

from fake_it.models import Voter, Poll

POSSIBLE_ACTIONS = ("insert", "update", "answer_poll")

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def main():
    while True:
        action = choice(POSSIBLE_ACTIONS)
        if action == "insert":
            insert_fake_voter()
        elif action == "update":
            update_random_voter()
        elif action == "answer_poll":
            answer_random_poll()
        # I don't know if this actually works
        sleep(0.5)

def random_race():
    return choice(('Ashkenazi', "Spharadi", "Mix", "Goy", "Smolani Boged"))

def random_gender():
    return choice(('m','f','t','n'))

def random_bibist():
    return choice(('y','n'))

def insert_fake_voter():
    faker = Faker()
    Voter(
        id=str(random_with_N_digits(9)),
        name=faker.name(),
        address=faker.address(),
        gender=random_gender(),
        race=random_race(),
        bibist=random_bibist(),
    ).create()

def update_random_voter():
    voter = Voter.random()
    if voter is not None:
        if choice((True, False)):
            voter.race = random_race()
        if choice((True, False)):
            voter.bibist = random_bibist()
        voter.save()

def answer_random_poll():
    voter = Voter.random()
    if voter is not None:
        Poll(
            voter_id=voter.id,
            answer=choice(("Bibi", "Gantz", "Benet", "Emet", "Meshutefet", "Dosim"))
        ).create()
