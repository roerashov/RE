import re


class Contact:
    def __init__(self):
        self.lastname = ''
        self.firstname = ''
        self.surname = ''
        self.organization = ''
        self.pozition = ''
        self.phone = ''
        self.email = ''

def create_contact(rows):
    pattern = r"^(8|\+7)*( |-)*(\()*(\d{3})*(\))*( |-)*(\d{3})( |-)*(\d{2})( |-)*(\d{2})*( |\()*([доб.])*( )*(\d{4})*(\))*"
    list_contact = list()
    fullname = ''
    for i in range(1,len(rows)):
        list_contact.append(Contact())
        row = rows[i]
        for element in range(0,3):
            fullname += row[element] + ' '
        text = fullname.split()
        for y in range(len(text)):
            if y == 0:
                list_contact[i-1].lastname = text[y]
            if y == 1:
                list_contact[i-1].firstname = text[y]
            if y == 2:
                list_contact[i-1].surname = text[y]
        for z in range(3,len(row)):
            if z == 3:
                list_contact[i-1].organization = row[z]
            if z == 4:
                list_contact[i-1].pozition = row[z]
            if z == 5:
                match = re.match(pattern,row[z])
                if match:
                    if match.group(15):
                        if match.group(1) != '8':
                            list_contact[i-1].phone = (f'{match.group(1)}({match.group(4)})'
                            f'{match.group(7)}-{match.group(9)}'
                            f'-{match.group(11)} доб.{match.group(15)}')
                        else:
                            list_contact[i-1].phone = f'+7({match.group(4)}){match.group(7)}'
                        f'-{match.group(9)}-{match.group(11)} доб.{match.group(15)}'
                    else:
                        if match.group(1) != '8':
                            list_contact[i-1].phone = f"{match.group(1)}({match.group(4)}){match.group(7)}-{match.group(9)}-{match.group(11)}"
                        else:
                            list_contact[i-1].phone = f'+7({match.group(4)}){match.group(7)}-{match.group(9)}-{match.group(11)}'
                
            if z == 6:
                list_contact[i-1].email = row[z]
        fullname = ''
        del_list = []
    for i in range(0,len(list_contact)):
        for y in range(0,len(list_contact)):
            if (((list_contact[i].lastname == list_contact[y].lastname)
                and (list_contact[i].firstname == list_contact[y].firstname))
                and (i != y) and (i not in del_list)):
                del_list.append(y)
                if list_contact[y].organization:
                    list_contact[i].organization = list_contact[y].organization
                    
                if list_contact[y].pozition:
                    list_contact[i].pozition = list_contact[y].pozition
                    
                if list_contact[y].phone:
                    list_contact[i].phone = list_contact[y].phone
                    
                if list_contact[y].email:
                    list_contact[i].email = list_contact[y].email
                    
    result =[]
    result_row = []
    new_list = []
    for i in range(0,len(list_contact)):
        if i not in del_list:
            new_list.append(list_contact[i])
            result_row.extend([list_contact[i].lastname, list_contact[i].firstname,list_contact[i].surname,list_contact[i].organization
                               ,list_contact[i].pozition,list_contact[i].phone,list_contact[i].email])
            result.append(result_row)
            result_row = []
    result.insert(0,rows[0])
    return result


import csv
with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
data = create_contact(contacts_list)

with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(data)