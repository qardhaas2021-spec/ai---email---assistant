import anthropic
from datetime import datetime
import os

client = anthropic.Anthropic()
  
your_name = input("What is your name? ")
your_job = input("What is your job title? ")
your_company = input("What is your company name? ")
print("\nWhat type of email?")
print("1. Meeting request")
print("2. Job application")
print("3. Follow up")
print("4. Thank you")
print("5. Apology")
print("6. Other")

choice = input("Choose a number (1-6): ")

if choice == "1":
    topic = "requesting a meeting"
elif choice == "2":
    topic = "a job application"
elif choice == "3":
    topic = "following up on a previous conversation"
elif choice == "4":
    topic = "saying thank you"
elif choice == "5":
    topic = "apologizing for something"
else:
    topic = input("Describe your email: ")
recipient = input("Who are you sending it to? ")
tone = input("What tone? (professional / friendly / formal): ")

prompt = f"Write a {tone} email to {recipient} about: {topic}. Sign off with the name: {your_name}, job title: {your_job}, company: {your_company}. Do not use any placeholders. Do not use any markdown formatting like ** or -- in the email. Write it as clean plain text."

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print("\n" + "="*50)
print("         📧 YOUR EMAIL")
print("="*50)
print(message.content[0].text)
print("="*50)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"email_{timestamp}.txt"

with open(filename, "w") as f:
    f.write(message.content[0].text)

print(f"\n✅ Email saved to {filename}")
