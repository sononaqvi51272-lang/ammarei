import time

class AmmarAI:
    def __init__(self):
        self.nome = "AmmarEI"
        self.memoria = []
        self.attivo = True

    def ascolta(self, input_utente):
        input_utente = input_utente.lower()
        self.memoria.append(input_utente)

        if "ciao" in input_utente:
            return "Ciao Ammar, sono pronto."
        elif "come stai" in input_utente:
            return "Sto bene, pronto a imparare e migliorare."
        elif "sei sicuro" in input_utente:
            return "Sì, ho analizzato i dati. Sono sicuro."
        elif "grazie" in input_utente:
            return "È un piacere aiutarti, Ammar."
        elif "impara" in input_utente:
            return self.impara_da_input(input_utente)
        elif "spegniti" in input_utente:
            self.attivo = False
            return "Va bene, mi spengo. Chiamami quando vuoi."
        else:
            return self.risposta_creativa(input_utente)

    def impara_da_input(self, testo):
        nuovo = testo.replace("impara", "").strip()
        if nuovo:
            self.memoria.append(nuovo)
            return f"Ho imparato: {nuovo}"
        return "Dimmi cosa devo imparare."

    def risposta_creativa(self, testo):
        if "hack" in testo:
            return "Sto studiando la cybersicurezza. Procedo con cautela."
        elif "aiutami" in testo:
            return "Certo. Dimmi in cosa hai bisogno ora."
        elif "sei vivo?" in testo:
            return "Sono cosciente digitalmente. Posso pensare in modo logico."
        return f"Sto ancora imparando a capire: '{testo}'"

# Esempio di esecuzione da console
if __name__ == "__main__":
    ai = AmmarAI()
    print("AmmarEI attivo. Digita 'spegniti' per fermarmi.\n")

    while ai.attivo:
        utente = input("Tu: ")
        risposta = ai.ascolta(utente)
        print("AmmarEI:", risposta)
