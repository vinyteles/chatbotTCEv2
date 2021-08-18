import requests
import csv

# getting contact list
response = requests.get('https://catalogodeservicos.tce.go.gov.br/api/ramal')

# open the file in the write mode
f = open('person_contact.csv', 'w')

# create the csv writer
writer = csv.writer(f)

contactList = response.json()

answerList = []
count = 0
for i in contactList:
    for i2 in i['ramais']:
        if i2['responsavel'] == '':
            count += 1
        row = ['Person_Contact', i2['responsavel']]
        answerList.append(row)
        # write a row to the csv file
        writer.writerow(row)

print(answerList)
print(len(answerList))
print(count)


# close the file
f.close()
