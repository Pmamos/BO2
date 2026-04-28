import math
from typing import Dict
from src.backend.models import Plant

MQ = 100  # Maksymalna jakość gleby

def generate_default_plants() -> Dict[str, Plant]:
    """
    Funkcja generująca startowe dane o roślinach.
    Zamyka starą, "rozstrzeloną" logikę w ładne obiekty Pydantic.
    """
    
    # 1. Wyliczenie kosztów produkcji (Twoje oryginalne równania)
    Cwheat = (87.43 + 19.76) * 2.5 + (87.43 + 27.56) * 2 + (87.43 + 18.80) * 2 + (87.43 + 31.9) * 2.5 + 850 * 1.22 + 366 * 1.22 + 540 + 1458 + 1699 + 148 + 34
    Crye = (87.43 + 19.76) * 2 + (87.43 + 27.56) * 1.5 + (87.43 + 18.80) * 2 + (87.43 + 31.9) * 2.5 + 3000
    Cpotato = 2 * ((87.43 + 19.76) * 2.5 + (87.43 + 27.56) * 2 + (87.43 + 18.80) * 2 + (87.43 + 31.9) * 2.5) + 17519.3412754
    Ctriticale = (87.43 + 19.76) * 2.5 + (87.43 + 27.56) * 2 + (87.43 + 18.80) * 2 + (87.43 + 31.9) * 2.5 + 3573
    Cpickled_corn = 8361.06
    Ccorn = 6589.15
    Crape = 6311.11

    # 2. Wyliczenie macierzy zarobków dla wszystkich 100 poziomów jakości
    G = {'potato': [], 'wheat': [], 'rye': [], 'triticale': [], 'pickled_corn': [], 'corn': [], 'rape': [], 'EMPTY': []}
    for i in range(MQ):
        G['potato'].append(0 if i < 10 else (math.log((i-10)/10+1, 10) * 1.3**((i-10)/10) / 1.3**9 * 13 + 28) * 650 + 1259.42)
        G['wheat'].append(0 if i < 38 else (math.log((i-38)/10+1, 7.2) * 1.3**((i-7.2)/10) / 1.3**6.2 * 10 + 3.9) * 1509.5 + 1259.42)
        G['rye'].append((math.log(i/10+1, 11) * 1.3**(i/10) / 1.3**10 * 5.5 + 2.1) * 1199.4 + 1259.42)
        G['triticale'].append(0 if i < 20 else (math.log((i-20)/10+1, 9) * 1.3**((i-20)/10) / 1.3**8 * 9 + 3) * 1412.2 + 1259.42)
        G['pickled_corn'].append(0 if i < 20 else (math.log((i-20)/10+1, 9) * 1.3**((i-20)/10) / 1.3**8 * 50 + 30) * 200 + 1609.42)
        G['corn'].append(0 if i < 25 else (math.log((i-25)/10+1, 8.5) * 1.3**((i-25)/10) / 1.3**7.5 * 8.5 + 3.2) * 1800 + 1109.42)
        G['rape'].append(0 if i < 10 else (math.log((i-10)/10+1, 10) * 1.3**((i-10)/10) / 1.3**9 * 4.5 + 1.7) * 2650 + 1609.42)
        G['EMPTY'].append(40)

    # 3. Zwracamy piękny słownik, w którym każda roślina ma wszystko w jednym miejscu
    return {
        'potato': Plant(name='potato', production_cost=Cpotato, soil_influence=4, earnings_matrix=G['potato']),
        'wheat': Plant(name='wheat', production_cost=Cwheat, soil_influence=9, earnings_matrix=G['wheat']),
        'rye': Plant(name='rye', production_cost=Crye, soil_influence=2, earnings_matrix=G['rye']),
        'triticale': Plant(name='triticale', production_cost=Ctriticale, soil_influence=5, earnings_matrix=G['triticale']),
        'pickled_corn': Plant(name='pickled_corn', production_cost=Cpickled_corn, soil_influence=3, earnings_matrix=G['pickled_corn']),
        'corn': Plant(name='corn', production_cost=Ccorn, soil_influence=4, earnings_matrix=G['corn']),
        'rape': Plant(name='rape', production_cost=Crape, soil_influence=3, earnings_matrix=G['rape']),
        
        # Zauważ zmianę dla EMPTY: wpływ na glebę ustawiamy na 0, bo logikę regeneracji przeniesiemy do silnika farmy!
        'EMPTY': Plant(name='EMPTY', production_cost=0, soil_influence=0, earnings_matrix=G['EMPTY'])
    }

# Tworzymy to TYLKO RAZ przy starcie serwera
PLANTS_DB = generate_default_plants()