"""
Searches on a specific site in Chicago, if new viable projects have been added.
Viable projects are Office with 25ksf and Industrial with 90ksf
Sends Mail if new projects have been found or not.

"""


import requests
import smtplib
from bs4 import BeautifulSoup


r = requests.get("http://interactive.chicagobusiness.com/closer/constructionpipeline/private/full/")

soup = BeautifulSoup(r.content)
officeResults = soup.find_all(lambda tag: "office" in tag.string if tag.string else False)
listOffice = map(lambda element: element.string, officeResults)

indResults = soup.find_all(lambda tag: "industrial" in tag.string if tag.string else False)
listInd = map(lambda element: element.string, indResults)

viableOfficeList = []
viableIndustrialList = []


with open("nr_of_office.txt") as fileOffice:
    """
    Reads the number of viable projects from the last time the program ran, from a text file.
    It will be the only element from a list, and I will save it as int to compare it later.
    """
    nrOfficeStr = fileOffice.readlines()
    nrOffice = int(nrOfficeStr[0])


with open("nr_of_industrial.txt") as fileIndustrial:
    """
    Reads the number of viable projects from the last time the program ran, from a text file.
    It will be the only element from a list, and I will save it as int to compare it later.
    """
    nrIndStr = fileIndustrial.readlines()
    nrIndustrial = int(nrIndStr[0])

"""
Example: 3,396-square-foot medical office 
It will only get those projects where the "office" or "industrial" string is found.
Then it will break up so that it get's the square foot number, which is a string
and it will be transformed in an int.
If it's viable it will be appended to the corresponding list.
"""
for bldg in listOffice:
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

    sq_feet = 0
    try:
        sq_feet = int(x)
    except ValueError as errorStringToInt:
        pass

    if sq_feet > 24999:
        viableOfficeList.append(bldg)

"""
240,000-square-foot industrial center, $25 million 
It will only get those projects where the "office" or "industrial" string is found.
Then it will break up so that it get's the square foot number, which is a string
and it will be transformed in an int.
If it's viable it will be appended to the corresponding list.
"""
for bldg in listInd:
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

    sq_feet = 0
    try:
        sq_feet = int(x)
    except ValueError as errorStringToInt:
        pass

    if sq_feet > 89999:
        viableIndustrialList.append(bldg)


mailMessageOffice = "Office: "

"""
It compares the length of the list with the length of the list from the previous run,
which is always saved in the file. If there are more then an e-mail will be sent
with the new projects that appeared.
"""
if len(viableOfficeList) == nrOffice:
    mailMessageOffice += "0 \n"
else:
    nrNewOfficeProjects = len(viableOfficeList) - nrOffice
    
    for i in range(nrNewOfficeProjects):
        mailMessageOffice += viableOfficeList[i] + "\n"

    fileOffice = open("nr_of_office.txt", "w")
    fileOffice.write(str(len(viableOfficeList)))

mailMessageInd = ""
mailMessageInd += "Industrial: "


if len(viableIndustrialList) == nrIndustrial:
    mailMessageInd += "0 \n"
else:
    nrNewIndustrialProjects = len(viableIndustrialList) - nrIndustrial

    for i in range(nrNewIndustrialProjects):
        mailMessageInd += viableIndustrialList[i] + "\n"

    fileInd = open("nr_of_industrial.txt", "w")
    fileInd.write(str(len(viableIndustrialList)))


mailMessage = "Office: " + mailMessageOffice + mailMessageInd


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
server.sendmail(emailSend, emailReceive, mailMessage)
server.quit()








