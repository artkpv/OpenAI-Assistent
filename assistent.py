# %%
import subprocess
#%%
def main():
    # Simple REPL loop with commands running in /bin/bash shell 
    # with the output printed to the console:
    while True:
        command = input("> ")
        if command == "exit":
            break
        else:
            # Execute command in /bin/bash shell:
            print("Executing command: " + command)
            # Use subprocess module to execute command in /bin/bash shell:
            subprocess.run(command, shell=True)
            print("Command executed.")

main()
    

