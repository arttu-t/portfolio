from random import *
from string import *

pituus = int(input("Anna salasanan pituus, minkä haluat luoda: "))
salasana = []

merkit = ascii_letters + "0123456789" + punctuation


for i in range(0, pituus):
    salasana.append(choice(merkit))


lopullinen_salasana = "".join(salasana)
print(f"salasanasi on {lopullinen_salasana}")