import requests
import csv

# getting contact list
response = requests.get('https://catalogodeservicos.tce.go.gov.br/api/ramal')

# open the file in the write mode
f = open('csv_file.csv', 'w')

# create the csv writer
writer = csv.writer(f)

contactList = response.json()

answerList = []

for i in contactList:
    row = ['Contato', i['nome']]
    answerList.append(row)
    # write a row to the csv file
    writer.writerow(row)

for i in contactList:
    for i2 in i['ramais']:
        row = ['Contato', i2['responsavel']]
        answerList.append(row)
        # write a row to the csv file
        writer.writerow(row)

print(answerList)
print(len(answerList))


# close the file
f.close()