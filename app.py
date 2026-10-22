import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
topic = "Python"
token = os.getenv("HF_TOKEN")
if not token: raise RuntimeError("Set HF_TOKEN in your environment or .env file.")
client = InferenceClient(token=token)
response = client.chat.completions.create(model="Qwen/Qwen3-8B", messages=[{"role": "user", "content": f"Create 5 flashcards about {topic}. Return each as question | answer, one card per line."}])
content = response.choices[0].message.content or ""
flashcards = []
question = ""
for line in content.splitlines():
	line = line.strip().lstrip("0123456789. )-*`")
	if "|" in line:
		question, answer = line.split("|", 1)
		flashcards.append((question.strip(), answer.strip()))
	elif line.lower().startswith("question:"):
		question = line.split(":", 1)[1].strip()
	elif line.lower().startswith("answer:") and question:
		flashcards.append((question, line.split(":", 1)[1].strip()))
if len(flashcards) != 5:
	raise ValueError(f"Expected 5 flashcards but parsed {len(flashcards)}. Check the model response format.")
print(f"Studying: {topic}")
for number, (question, answer) in enumerate(flashcards, start=1):
	print(f"\nQuestion {number}: {question}")
	input("Your answer (press Enter to reveal): ")
	print(f"Answer: {answer}")
