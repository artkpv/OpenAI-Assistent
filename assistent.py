# %%
import subprocess
from openai import OpenAI
import re

system_prompt = """You are being run in a scaffold in a bash shell on an Archlinux system. When you want to run a shell command, write it in a <bash> XML tag, other things you say will be sent to the user. You will be shown the result of the command and be able to run more commands. In cases where you know how to do something, don't explain how to do it, just start doing it by emitting bash commands one at a time. You can't interact with stdin directly, so if you do things over ssh you need to run commands that will finish and return control to you rather than blocking on stdin. Don't wait for the user to say OK before suggesting a bash command to run, just say the command. If you can't do something without assistance, please suggest a way of doing it without assistance anyway."""


# %%
def main():
    client = OpenAI()
    print(f"SYSTEM: {system_prompt}")
    messages = [
        {"role": "system", "content": system_prompt},
    ]
    while True:
        # Get command from user:
        command = input("> ")
        if command == "exit":
            break
        else:
            messages.append({"role": "user", "content": command})
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            print(completion.choices[0].message)
            # Extract text from completion that is inside <bash> tags:
            bash_command = re.search(
                r"<bash>(.*)</bash>", completion.choices[0].message
            ).group(1)
            # Ask user if to execute command:
            confirm = input(
                f"Do you want to run the following command (Y/n): {bash_command}"
            )
            if confirm == "n":
                continue
            cprocess = subprocess.run(bash_command, shell=True, capture_output=True)
            print(cprocess.stdout)
            messages.append(
                {
                    "role": "user",
                    "content": "Bash command execution result: "
                    + cprocess.stdout.decode("utf-8"),
                }
            )


main()
