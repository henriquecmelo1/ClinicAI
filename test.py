# import requests

# # url = url = f"https://graph.facebook.com/v21.0/171708262689180/subscribed_apps"
# # headers = {
# #     "Authorization": f"Bearer EAACnBpbJHP8BPsSh3UyEu2TMDHEuXSYq70l0wSZCXv5gKaUIvRDMN7TvztscQKYCUT3eHyB3IfE04scyt9ioPpjMmOxLkVMuJbAUSuPoSZCzk7CqTQBxFtFLosTtrGvk60S9SodPOOBCPzzVBugU9AhPDfGf6sUDDWRE5KqC3RFhSHEOjIM5thwr5Xj0Bw0ZCyrvOqpHhtFbrXzT4NfOuTeDDt1loZBFb97g3LYPNi0ZAAAZDZD"
# # }

# url = "https://sequestrable-serpentinely-arla.ngrok-free.app/webhook?hub.mode=subscribe&hub.challenge=183646741404927&hub.verify_token=EAACnBpbJHP8BPsSh3UyEu2TMDHEuXSYq70l0wSZCXv5gKaUIvRDMN7TvztscQKYCUT3eHyB3IfE04scyt9ioPpjMmOxLkVMuJbAUSuPoSZCzk7CqTQBxFtFLosTtrGvk60S9SodPOOBCPzzVBugU9AhPDfGf6sUDDWRE5KqC3RFhSHEOjIM5thwr5Xj0Bw0ZCyrvOqpHhtFbrXzT4NfOuTeDDt1loZBFb97g3LYPNi0ZAAAZDZD"


# response = requests.get(url)

# print(response.json())
# print(response.status_code)

import json 

content='{  "agent_response": "Entendo. E numa escala de 0 a 10, sendo 0 sem dor e 10 a pior dor possível, como você classificaria a intensidade da dor e do desconforto no seu pé?",  "collected_data": {    "queixa_principal": "Pé inchado",   "sintomas_detalhados": "Pé inchado e dificuldade para movimentar.",    "duracao_frequencia": "Desde anteontem, constantes."  }}'

res = json.loads(content)
res = json.dumps(res)

print(res)