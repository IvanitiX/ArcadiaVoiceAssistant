import requests
sender = input("What is your name?\n")

bot_message = ""
while bot_message != "Adiós":
    transcripcion = []
    message = input("What's your message?\n")

    print("Sending message now...")

    r = requests.post('http://localhost:5005/webhooks/rest/webhook/', json={"sender": sender, "message": message})

    print(f"Bot says, {r.content}")
    for i in r.json():
        try:
            transcripcion.append(i['text'])
        except KeyError:
            try:
                if i['custom']['text']:
                    transcripcion.append(u'{}'.format(i['custom']['text']))
                transcripcion.append(i['custom']['audio'])
            except KeyError:
               pass
        print(f"{transcripcion}")