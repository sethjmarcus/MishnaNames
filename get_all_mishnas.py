import requests
from pathlib import Path
import time

BASE = "https://www.sefaria.org/api"

TRACTATES = [
    #"Berakhot",
    #"Peah",
    #"Demai",
    #"Kilayim",
    #"Sheviit",
    #"Terumot",
    #"Maasrot",
    #"Maaser Sheni",
    #"Challah",
    #"Orlah",
    #"Bikkurim",
#
    #"Shabbat",
    #"Eruvin",
    #"Pesachim",
    #"Shekalim",
    #"Yoma",
    #"Sukkah",
    #"Beitzah",
    #"Rosh Hashanah",
    #"Taanit",
    #"Megillah",
    #"Moed Katan",
    #"Chagigah",
#
    #"Yevamot",
    #"Ketubot",
    #"Nedarim",
    #"Nazir",
    #"Sotah",
    #"Gittin",
    #"Kiddushin",
#
    #"Bava Kamma",
    #"Bava Metzia",
    #"Bava Batra",
    #"Sanhedrin",
    #"Makkot",
    #"Shevuot",
    #"Eduyot",
    #"Avodah Zarah",
    #"Avot",
    #"Horayot",
#
    #"Zevachim",
    #"Menachot",
    #"Chullin",
    #"Bekhorot",
    #"Arakhin",
    #"Temurah",
    #"Keritot",
    #"Meilah",
    #"Tamid",
    #"Middot",
    #"Kinnim",
#
    #"Kelim",
    #"Oholot",
    #"Negaim",
    #"Parah",
    #"Tahorot",
    #"Mikvaot",
    #"Niddah",
    #"Makhshirin",
    #"Zavim",
    #"Tevul Yom",
    #"Yadayim",
    "Oktzin"
]

outdir = Path("mishnayot")
outdir.mkdir(exist_ok=True)

for tractate in TRACTATES:

    title = f"Mishnah_{tractate.replace(' ', '_')}"

    # Get metadata
    idx_url = f"{BASE}/index/{title}"
    idx = requests.get(idx_url).json()
    print(idx_url)
    chapters = idx["schema"]["lengths"][0]

    print(f"{tractate}: {chapters} chapters")

    for chapter in range(1, chapters + 1):

        text_url = f"{BASE}/texts/{title}.{chapter}"

        data = requests.get(text_url).json()

        # Hebrew text
        mishnayot = data["he"]

        for m_num, text in enumerate(mishnayot, start=1):

            filename = (
                f"{tractate.replace(' ', '_')}_"
                f"{chapter}_{m_num}.txt"
            )

            path = outdir / filename

            path.write_text(text, encoding="utf-8")

            print("saved", filename)

        time.sleep(0.1)   # be polite to API