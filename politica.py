judete = [
    "alba",
    "arad",
    "arges",
    "bacau",
    "bihor",
    "bistrita-nasaud",
    "botosani",
    "brasov",
    "braila",
    "buzau",
    "caras-severin",
    "calarasi",
    "cluj",
    "constanta",
    "covasna",
    "dambovita",
    "dolj",
    "galati",
    "giurgiu",
    "gorj",
    "harghita",
    "hunedoara",
    "ialomita",
    "iasi",
    "ilfov",
    "maramures",
    "mehedinti",
    "neamt",
    "olt",
    "prahova",
    "satu-mare",
    "sibiu",
    "suceava",
    "teleorman",
    "timisoara",
    "tulcea",
    "vaslui",
    "valcea",
    "vrancea"
]

link_judet = "https://recorder.ro/candidatii-judetului-{}/"
linkuri_judete = [link_judet.format(j) for j in judete]
linkuri = [*linkuri_judete, "https://recorder.ro/candidati-bucuresti/",
            "https://recorder.ro/candidati-diaspora/"]

locatii = [*judete, "bucuresti", "diaspora"]

from lxml import html
from pprint import pprint
import requests

lstrip = lambda l: [x.strip() for x in l]

def obtine_date_link(link, judet):
    print ("[+] {}".format(link))
    page = requests.get(link)
    tree = html.fromstring(page.content)

    nume = lstrip(tree.xpath('//h3[@class="block-parlamentar-nume mt-0"]/text()'))
    varste = lstrip(tree.xpath('//span[@class="block-parlamentar-attributes-attribute-value" and contains(text(),"de ani") and string-length(text()) < 20]/text()'))
    raspunsuri = lstrip(tree.xpath('//div[contains(@class, "block-parlamentar-answer-")]/text()'))

    print ("[i] {} {} {}".format(len(nume), len(varste), len(raspunsuri)))
    assert len(nume) != 0
    assert len(nume) == len(varste)
    assert len(nume)*5 == len(raspunsuri)

    date = []
    k = 0
    for i, n in enumerate(nume):
        date.append({
            "nume": str(n),
            "varsta": str(varste[i]),
            "raspunsuri": [str(x) for x in raspunsuri[k:k+5]],
            "judet": judet,
        })
        k+= 5

    return date

from json import dump
r = []
for i, link in enumerate(linkuri):
    r.extend(obtine_date_link(link, locatii[i]))
dump(r, open("rezultate.json", "w"))
