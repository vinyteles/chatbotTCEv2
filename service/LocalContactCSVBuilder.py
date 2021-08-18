import requests
import csv

# getting contact list
response = requests.get('https://catalogodeservicos.tce.go.gov.br/api/ramal')

# open the file in the write mode
f = open('local_contact.csv', 'w')

# create the csv writer
writer = csv.writer(f)

contactList = response.json()

answerList = []

for i in contactList:
    row = ['Local_Contact', i['nome']]
    answerList.append(row)
    # write a row to the csv file
    writer.writerow(row)

print(answerList)
print(len(answerList))


# close the file
f.close()
