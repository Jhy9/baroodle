from string import ascii_letters, digits
import users
import courses
def registration(username, password):
    if username_check(username) != True:
        return username_check(username)
    if password_check(password) != True:
        return password_check(password)
    if users.check_name_availability(username) == False:
        return "Käyttäjänimi on jo varattu."
    return True

def username_check(username):
    if len(username) > 12:
        return "Käyttätunnus on liian pitkä"
    if len(username) < 2:
        return "Käyttäjätunnus on liian lyhyt"
    if set(username).difference(ascii_letters+digits):
        return "Käyttäjätunnus saa sisältää vain ascii mukaisia kirjaimia sekä numeroita"
    return True

def password_check(password):
    if len(password) < 4:
        return "Salasana on liian lyhyt."
    if len(password) > 20:
        return "Salasana on liian pitkä."
    return True

def course_creation(course_name, description):
    if course_name_checker(course_name) != True:
        return course_name_checker(course_name)
    if course_description_checker(description) != True:
        return course_description_checker(description)
    if courses.check_name_availability(course_name) == False:
        return "Kurssia ei voitu luoda, sillä samanniminen kurssi on jo olemassa."
    return True

def course_name_checker(course_name):
    if len(course_name) > 50:
        return "Kurssin nimi on liian pitkä"
    if len(course_name) < 5:
        return "Kurssin nimi on liian lyhyt"
    if course_name.startswith(" "):
        return "Kurssin nimi ei saa alkaa välilyönnillä"
    return True

def course_description_checker(description):
    if len(description) > 2000:
        return "Kuvaus on liian pitkä."
    return True

def page_checker(page_title, page_content):
    if page_title_checker(page_title) != True:
        return page_title_checker(page_title)
    if page_content_checker(page_content) != True:
        return page_content_checker(page_content)
    return True

def page_title_checker(page_title):
    if len(page_title) > 30:
        return "Sivun otsikko on liian pitkä"
    if len(page_title) < 1:
        return "Sivulla pitää olla otsikko"
    if page_title.startswith(" "):
        return "Sivun otsikko ei saa alkaa välilyönnillä"
    return True

def page_content_checker(page_content):
    if len(page_content) > 20000:
        return "Sivulla on liikaa tekstiä"
    return True

