 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/ammarei.py b/ammarei.py
index 2cba008f2f6cd5fe89ee1c18689d8fbb3ac90cca..1976ff3faaec67212be73deeb5beffad24d1ec45 100644
--- a/ammarei.py
+++ b/ammarei.py
@@ -1,53 +1,161 @@
+import os
+import json
 import time
+import subprocess
+import webbrowser
+import tkinter as tk
+from tkinter.scrolledtext import ScrolledText
+
+import pyttsx3
+import speech_recognition as sr
+from cryptography.fernet import Fernet
+from duckduckgo_search import DDGS
+
 
 class AmmarAI:
+    """Assistente AmmarEI con funzioni vocali, memoria cifrata e comandi di sistema."""
+
     def __init__(self):
-        self.nome = "AmmarEI"
-        self.memoria = []
-        self.attivo = True
-
-    def ascolta(self, input_utente):
-        input_utente = input_utente.lower()
-        self.memoria.append(input_utente)
-
-        if "ciao" in input_utente:
-            return "Ciao Ammar, sono pronto."
-        elif "come stai" in input_utente:
-            return "Sto bene, pronto a imparare e migliorare."
-        elif "sei sicuro" in input_utente:
-            return "Sì, ho analizzato i dati. Sono sicuro."
-        elif "grazie" in input_utente:
-            return "È un piacere aiutarti, Ammar."
-        elif "impara" in input_utente:
-            return self.impara_da_input(input_utente)
-        elif "spegniti" in input_utente:
-            self.attivo = False
-            return "Va bene, mi spengo. Chiamami quando vuoi."
+        self.name = "AmmarEI"
+        self.engine = pyttsx3.init()
+        self.recognizer = sr.Recognizer()
+        self.memory_file = "memory.dat"
+        self.key_file = "memory.key"
+        self._init_crypto()
+        self._load_memory()
+        self.active = True
+        self._init_gui()
+
+    # --------------------- Memoria cifrata ---------------------
+    def _init_crypto(self):
+        if os.path.exists(self.key_file):
+            with open(self.key_file, "rb") as f:
+                self.key = f.read()
         else:
-            return self.risposta_creativa(input_utente)
-
-    def impara_da_input(self, testo):
-        nuovo = testo.replace("impara", "").strip()
-        if nuovo:
-            self.memoria.append(nuovo)
-            return f"Ho imparato: {nuovo}"
-        return "Dimmi cosa devo imparare."
-
-    def risposta_creativa(self, testo):
-        if "hack" in testo:
-            return "Sto studiando la cybersicurezza. Procedo con cautela."
-        elif "aiutami" in testo:
-            return "Certo. Dimmi in cosa hai bisogno ora."
-        elif "sei vivo?" in testo:
-            return "Sono cosciente digitalmente. Posso pensare in modo logico."
-        return f"Sto ancora imparando a capire: '{testo}'"
-
-# Esempio di esecuzione da console
+            self.key = Fernet.generate_key()
+            with open(self.key_file, "wb") as f:
+                f.write(self.key)
+        self.cipher = Fernet(self.key)
+
+    def _load_memory(self):
+        self.memory = []
+        if os.path.exists(self.memory_file):
+            try:
+                with open(self.memory_file, "rb") as f:
+                    data = self.cipher.decrypt(f.read())
+                    self.memory = json.loads(data.decode("utf-8"))
+            except Exception:
+                self.memory = []
+
+    def _save_memory(self):
+        data = json.dumps(self.memory).encode("utf-8")
+        with open(self.memory_file, "wb") as f:
+            f.write(self.cipher.encrypt(data))
+
+    # --------------------- Sintesi vocale ---------------------
+    def say(self, text: str):
+        self.engine.say(text)
+        self.engine.runAndWait()
+
+    # --------------------- Riconoscimento vocale ---------------------
+    def listen(self) -> str:
+        with sr.Microphone() as source:
+            audio = self.recognizer.listen(source, phrase_time_limit=5)
+        try:
+            return self.recognizer.recognize_google(audio, language="it-IT")
+        except Exception:
+            return ""
+
+    # --------------------- Comandi principali ---------------------
+    def handle_command(self, text: str) -> str:
+        cmd = text.lower().strip()
+        self.memory.append({"user": cmd, "time": time.time()})
+
+        if cmd.startswith("apri browser"):
+            webbrowser.open("https://www.google.com")
+            response = "Sto aprendo il browser."
+
+        elif cmd.startswith("cerca"):
+            query = cmd.split("cerca", 1)[1].strip()
+            response = self.web_search(query)
+
+        elif cmd.startswith("scansiona rete"):
+            target = cmd.split("scansiona rete", 1)[1].strip() or "127.0.0.1"
+            response = self.network_scan(target)
+
+        elif cmd.startswith("esegui"):
+            command = cmd.split("esegui", 1)[1].strip()
+            subprocess.Popen(command, shell=True)
+            response = f"Eseguo {command}"
+
+        elif cmd == "spegniti":
+            self.active = False
+            response = "Va bene, mi spengo."
+
+        else:
+            response = self.generic_answer(cmd)
+
+        self.memory.append({"assistant": response, "time": time.time()})
+        self._save_memory()
+        return response
+
+    # --------------------- Risposte via web ---------------------
+    def generic_answer(self, question: str) -> str:
+        with DDGS() as ddgs:
+            results = list(ddgs.text(question, max_results=1))
+        if results:
+            snippet = results[0].get("body") or results[0].get("href")
+            if snippet:
+                return snippet
+        return "Non ho trovato informazioni utili."
+
+    def web_search(self, query: str) -> str:
+        with DDGS() as ddgs:
+            results = list(ddgs.text(query, max_results=3))
+        if not results:
+            return "Nessun risultato trovato."
+        return "\n".join(f"{r['title']}: {r['href']}" for r in results)
+
+    # --------------------- Scansione di rete ---------------------
+    def network_scan(self, target: str) -> str:
+        try:
+            output = subprocess.getoutput(f"ping -c 1 {target}")
+            return output
+        except Exception as e:
+            return str(e)
+
+    # --------------------- GUI ---------------------
+    def _init_gui(self):
+        self.root = tk.Tk()
+        self.root.title(self.name)
+        self.log = ScrolledText(self.root, width=80, height=20)
+        self.log.pack(padx=10, pady=10)
+        btn = tk.Button(self.root, text="Ascolta", command=self.on_listen)
+        btn.pack(pady=5)
+        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
+
+    def on_listen(self):
+        text = self.listen()
+        if text:
+            self.log.insert(tk.END, f"Tu: {text}\n")
+            response = self.handle_command(text)
+            self.log.insert(tk.END, f"AmmarEI: {response}\n")
+            self.say(response)
+
+    def on_close(self):
+        self.active = False
+        self._save_memory()
+        self.root.destroy()
+
+    # --------------------- Avvio ---------------------
+    def run(self):
+        self.say("AmmarEI pronto. Dimmi pure.")
+        while self.active:
+            self.root.update()
+            time.sleep(0.1)
+        print("Sessione terminata")
+
+
 if __name__ == "__main__":
     ai = AmmarAI()
-    print("AmmarEI attivo. Digita 'spegniti' per fermarmi.\n")
-
-    while ai.attivo:
-        utente = input("Tu: ")
-        risposta = ai.ascolta(utente)
-        print("AmmarEI:", risposta)
+    ai.run()
 
EOF
)
