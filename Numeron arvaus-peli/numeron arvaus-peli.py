import random

oikea_numero = random.randint(1, 99)
elamat = 5

while elamat > 0:
    print(f"{elamat} elamaa jaljella")
    arvattu_numero = int(input("Arvaa numero valilta 1-99 "))

    if arvattu_numero > 99 or arvattu_numero < 1:
        print("Antamasi numero ei ole valilta 1-99")

    elif arvattu_numero < oikea_numero:
        print("Oikea numero on suurempi")
        elamat -= 1

    elif arvattu_numero > oikea_numero:
        print("Oikea numero on pienempi")
        elamat -= 1

    elif arvattu_numero == oikea_numero:
        break

if elamat == 0:
    print(f"Havisit pelin, oikea numero oli {oikea_numero}")

elif elamat > 0:
    print(f"Arvasit oikein, oikea numero oli {oikea_numero}")