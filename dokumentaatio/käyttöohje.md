## Käyttöohje

1. Kloonaa repositorio ja siirry sen juurikansioon
2. Luo kansioon ".env" tiedosto ja muokkaa sen sisältö seuraavanlaiseksi:
   ```bash
   DATABASE_URL=<tietokannan paikallinen osoite>
   SECRET_KEY=<salainen avain>
   ```
3. Avaa komentorivi ja alusta sovellus sekä tietokanta seuraavilla komennoilla
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r ./requirements.txt
   psql < schema.sql
   ```
4. Sovelluksen voi nyt käynnistää komennolla
   ```bash
   flask run
   ```
5. (Vapaaehtoinen testaukseen) Voit lisätä tietokantaan muutaman valmiin kurssin ja käyttäjän painamalla sovelluksen pääsivulla linkkiä "Testaa toimintaa".
   Nämä käyttäjät, salasanat ja kurssit löytyvät tiedostosta [testfile.py](./testfile.py). Tee tämä ennen kuin rekisteröit omia käyttäjiä. (Tämä ominaisuus on vain väliaikainen).
