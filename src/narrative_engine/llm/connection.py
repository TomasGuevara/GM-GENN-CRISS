import requests
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

load_dotenv()
assert os.getenv("GEMINI_API_KEY"), "ERROR: No se cargó GEMINI_API_KEY desde el .env"

class Llama:

	def __init__(
		self,
		model: str
	):
		self.model = model
		self.url = "http://127.0.0.1:11434/api/generate"

	def generate(
		self,
		prompt: str
	) -> str:
		response = requests.post(
			self.url,
			json={
				"model": self.model,
				"prompt": prompt,
				"stream": False
			}
		)
		response.raise_for_status()

		return response.json()["response"]

class Gemini:
    def __init__(self, model: str = "gemini-3.8-flash"):
        self.model = model
        # Subimos el timeout a 90 segundos (90000 ms) para evitar el error 504
        self.client = genai.Client(
            http_options=types.HttpOptions(timeout=90000)
        )
        # Lista de modelos ordenados por disponibilidad y velocidad
        self.modelos_respaldo = [
            model,
            "gemini-3.8-flash-lite",
            "gemini-3.5-flash",
        ]

    def generate(self, prompt: str, temp: float = 0.8) -> str:
        configuration = types.GenerateContentConfig(
            system_instruction="You are a creative writer with expertise in narrative.",
            temperature=temp,
            # Reducimos el tiempo de razonamiento interno para que genere la historia más rápido
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        )
        try_again: bool = True
        is_correct: bool = False 
        user_input = ""

        while try_again:

            for modelo_actual in self.modelos_respaldo:
                try:
                    response = self.client.models.generate_content(
                        model=modelo_actual,
                        contents=prompt,
                        config=configuration
                    )
                    return response.text
                
                except errors.APIError as e:
                    # Ahora también atrapamos el 504 (Deadline Exceeded) y 404
                    if e.code in (503, 504, 429, 404):
                        print(f"[NOTICE] {modelo_actual} delayed or busy (Error {e.code}). Trying next model...")
                        time.sleep(2)
                        continue
                    raise e

            print(f"Unable to connect to the Gemini server. Would you like to try again?")
            user_input = input("\n[Y/N] ")
            is_correct = False
                
            while not is_correct:
                if user_input.upper() in ("N", "Y"):
                    if user_input.upper() == "N":
                        try_again = False

                    is_correct = True

                else:
                    is_correct = False
                    print(f"The answer was incorrect, try again.")
                    user_input = input("\n[Y/N] ")



        raise RuntimeError("No response could be obtained from any Gemini model.")
