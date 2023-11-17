# %%
import subprocess
from openai import OpenAI
import re

system_prompt = """You are being run in a scaffold in a bash shell on an Archlinux system. When you want to run a shell command, write it in a <bash> XML tag (example: "<bash> some command </bash>"), other things you say will be sent to the user. You will be shown the result of the command and be able to run more commands. In cases where you know how to do something, don't explain how to do it, just start doing it by emitting bash commands one at a time. You can't interact with stdin directly, so if you do things over ssh you need to run commands that will finish and return control to you rather than blocking on stdin. Don't wait for the user to say OK before suggesting a bash command to run, just say the command. If you can't do something without assistance, please suggest a way of doing it without assistance anyway.

Example:

Q: List all files in ~/ directory.

A: <bash>ls ~</bash>
"""


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
        pattern = re.compile(r"<bash>(.*)</bash>")
        if command == "exit":
            break
        else:
            messages.append({"role": "user", "content": command})
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            print(completion.choices[0].message.content)
            # Find all matches of <bash> tags using regex and loop through them:
            for bash_command in re.findall(
                pattern, completion.choices[0].message.content
            ):
                # Ask user if to execute command:
                confirm = input(f"Run command? (Y/n): {bash_command} ")
                if confirm == "n":
                    continue
                cprocess = subprocess.run(bash_command, shell=True, capture_output=True)
                print(cprocess.stdout.decode("utf-8"))
                messages.append(
                    {
                        "role": "user",
                        "content": "Output of the last command was: "
                        + cprocess.stdout.decode("utf-8"),
                    }
                )


main()
