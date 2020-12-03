import pandas as pd
from json import load
import matplotlib.pyplot as plt

data = load(open("rezultate.json"))

for i, v in enumerate(data):
    data[i]["varsta"] = int(v["varsta"].replace("de ani", "").strip())
    data[i]["Alegeri locale in 2 tururi"] = v["raspunsuri"][0]
    data[i]["Reducerea aparatului bugetar"] = v["raspunsuri"][1]
    data[i]["Anularea imunitatii parlamentare"] = v["raspunsuri"][2]
    data[i]["Pierderea mandatului in caz de traseism"] = v["raspunsuri"][3]
    data[i]["Educatia sexuala in scoli"] = v["raspunsuri"][4]
    del data[i]["raspunsuri"]

df = pd.DataFrame.from_dict(data)
print (df)

intrebari = ["Alegeri locale in 2 tururi", "Reducerea aparatului bugetar", "Anularea imunitatii parlamentare", "Pierderea mandatului in caz de traseism", "Educatia sexuala in scoli"]

def procentaj_raspuns(i):
    k = df[i].value_counts()
    k = k.apply(lambda x: x / k.sum() * 100)
    return k.plot.pie(legend=True, autopct='%1.1f%%', ylabel="", title=i)

for k, i in enumerate(intrebari):
    procentaj_raspuns(i)
    plt.savefig('intrb{}.png'.format(k))
    plt.clf()

plot = df["varsta"].hist(bins=5, alpha=0.5, histtype='bar', ec='black')
plot.set_xlim((18, 75))
plot.set_xlabel("Varsta")
plot.set_ylabel("Candidat")
plot.grid(False)
plt.savefig("varste.png")
