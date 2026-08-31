import requests

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