"""
Searches on a specific site in Chicago, if new viable projects have been added.
Viable projects are Office with 25ksf and Industrial with 90ksf
Sends Mail if new projects have been found or not.
"""

import requests
import smtplib

from bs4 import BeautifulSoup


def get_projects(buildingType, soup):
    results = soup.find_all(lambda tag: buildingType in tag.string if tag.string else False)
    return map(lambda element: element.string, results)


def projects_checked_already(filename):
    with open(filename) as file:
        nrStr = file.readlines()
        return int(nrStr[0])


def get_viable_projects(projects, limit):
    """
    Example: 3,396-square-foot medical office
    It will only get those projects where the "office" or "industrial" string is found.
    Then it will break up so that it get's the square foot number, which is a string
    and it will be transformed in an int.
    If it's viable it will be appended to the corresponding list.
    """
    viables = []
    for bldg in projects:
        """
        Transforms the string in int, to verify square feet,
        then adds it to the list if it's viable
        """
        x = bldg.split(', ')
        y = x[0].split('-square')
        z = y[0].split(',')
        x = ""
        for el in z:
            x += el

        sqFeet = 0
        try:
            sqFeet = int(x)
        except ValueError as errorStringToInt:
            pass

        if sqFeet > limit:
            viables.append(bldg)
    return viables


def get_mail_message(viables, nrBldgs, filename):
    """
    It compares the length of the list with the length of the list from the previous run,
    which is always saved in the file. If there are more then an e-mail will be sent
    with the new projects that appeared.
    """
    message = ""
    if len(viables) == nrBldgs:
        message += "0 \n"
    else:
        nrNewProjects = len(viables) - nrBldgs

        for i in range(nrNewProjects):
            message += viables[i] + "\n"

        file = open(filename, "w")
        file.write(str(len(viables)))
    return message


def send_mail(message):
    """
    Sending a mail if new projects have been found or not.
    Enter two e-mails, one from which the mail will be sent,
    and another to receive it.
    """
    emailSend = input("Enter email to send the projects: ")
    passEmail = input("Enter password: ")
    emailReceive = input("To whom: ")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(emailSend, passEmail)
    server.sendmail(emailSend, emailReceive, message)
    server.quit()


def main():
    r = requests.get("http://interactive.chicagobusiness.com/closer/constructionpipeline/private/full/")
    soup = BeautifulSoup(r.content)

    offices = get_projects("office", soup)
    industrials = get_projects("industrial", soup)

    nrOffice = projects_checked_already("nr_of_office.txt")
    nrIndustrial = projects_checked_already("nr_of_industrial.txt")

    viableOffices = get_viable_projects(offices, 24999)
    viableIndustrials = get_viable_projects(industrials, 89999)

    mailMessageOffice = "\nOffice:\n"
    mailMessageOffice += get_mail_message(viableOffices, nrOffice, "nr_of_office.txt")

    mailMessageInd = "\nIndustrial:\n"
    mailMessageInd += get_mail_message(viableIndustrials, nrIndustrial, "nr_of_industrial.txt")

    mailMessage = mailMessageOffice + mailMessageInd
    send_mail(mailMessage)

main()
