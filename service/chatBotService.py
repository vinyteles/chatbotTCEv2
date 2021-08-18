import json

import requests

flag = 0



def concatStringAnswer(nome, responsavel, numero):
    x = "Nome: " + nome + ", Responsável: " + responsavel + ", Contato: " + numero + "\n"

    return x


def same_interval(local_interval, person_interval):
    if person_interval[0] <= local_interval[0] <= person_interval[1]:
        return 1

    if local_interval[0] <= person_interval[0] <= local_interval[1]:
        return 1

    return 0


# Achar o local e armazená-lo em um dict
def find_local_contact(user_contacts_request):

    for user_contact in user_contacts_request:
        if 'Local_Contact' in user_contact['entity']:
            return user_contact


# retira todos as pessoas que foram identificadas no mesmo intervalo de palavras que o local
def remove_ambiguos_entities(user_contacts_request):
    local_contact = find_local_contact(user_contacts_request)
    if not local_contact:
        return user_contacts_request

    result = []

    i = 0
    for user_contact in user_contacts_request:
        if 'Person_Contact' in user_contact['entity'] and not same_interval(local_contact['location'],
                                                                          user_contact['location']):
            result.append(user_contact)
        i += 1

    return result


def find_local_and_people(user_contacts_request):
    local_contact = find_local_contact(user_contacts_request)
    print(local_contact)
    user_contacts_request = remove_ambiguos_entities(user_contacts_request)

    if not local_contact:
        return find_person_in_API(user_contacts_request)
    elif not user_contacts_request:
        return find_local_in_API(local_contact)
    else:
        return find_local_and_people_in_API(local_contact, user_contacts_request)


def find_person_in_API(user_contacts_request):
    answer_string = ""
    response = requests.get('https://catalogodeservicos.tce.go.gov.br/api/ramal')
    api_contact_list = response.json()


    for user_contact in user_contacts_request:

        for api_contact in api_contact_list:
                for api_ramal in api_contact['ramais']:
                    if user_contact['value'].lower() in api_ramal['responsavel'].lower():
                        answer_string += concatStringAnswer(api_contact['nome'], api_ramal['responsavel'], api_ramal['numero'])


    return answer_string


def find_local_in_API(local_contact):
    answer_string = ""
    response = requests.get('https://catalogodeservicos.tce.go.gov.br/api/ramal')
    api_contact_list = response.json()

    for api_contact in api_contact_list:
        if local_contact['value'].lower() in api_contact['nome'].lower():
            for api_ramal in api_contact['ramais']:
                answer_string += concatStringAnswer(api_contact['nome'], api_ramal['responsavel'], api_ramal['numero'])


    return answer_string


def find_local_and_people_in_API(local_contact, user_contacts_request):
    answer_string = ""
    response = requests.get('https://catalogodeservicos.tce.go.gov.br/api/ramal')
    api_contact_list = response.json()

    for user_contact in user_contacts_request:
        answer_string += find_person_in_local(local_contact, user_contact, api_contact_list)

    return answer_string

def find_person_in_local(local_contact, user_contact, api_contact_list):
    answer_string = ""
    for api_contact in api_contact_list:
        if local_contact['value'].lower() in api_contact['nome'].lower():
            for api_ramal in api_contact['ramais']:
                if user_contact['value'].lower() in api_ramal['responsavel'].lower():
                    answer_string += concatStringAnswer(api_contact['nome'], api_ramal['responsavel'],
                                                        api_ramal['numero'])
            break

    return answer_string