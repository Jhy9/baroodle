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

def set_name_check(set_name):
    if len(set_name) > 30:
        return "Tehtäväsarjan nimi on liian pitkä"
    if len(set_name) < 1:
        return "Tehtäväsarjalla pitää olla nimi"
    if set_name.startswith(" "):
        return "Tehtäväsarjan nimi ei saa alkaa välilyönnillä"
    return True

def exercise_multi_check(assignment,answer,option1,option2,option3,max_points):
    if max_points < 0:
        return "Maksimipisteet eivät saa olla negatiivisia"
    if len(assignment) < 1:
        return "Tehtävänanto on pakollinen"
    if assignment.startswith(" "):
        return "Tehtävänanto ei saa alkaa välilyönnillä"
    if len(answer) < 1:
        return "Vastaus on pakollinen"
    if answer.startswith(" "):
        return "Vastaus ei saa alkaa välilyönnillä"
    if option1 == answer or option2 == answer or option3==answer:
        return True
    return "Jonkun vaihdoehdoista on oltava oikea vastaus"

def exercise_check(assignment, max_points):
    if max_points < 0:
        return "Maksimipisteet eivät saa olla negatiivisia"
    if len(assignment) < 1:
        return "Tehtävänanto on pakollinen"
    if assignment.startswith(" "):
        return "Tehtävänanto ei saa alkaa välilyönnillä"
    return True