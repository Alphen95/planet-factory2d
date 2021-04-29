import os
commit_name = input("commit name:")
commit_command = 'git commit -a -m "{}"'.format(commit_name)
os.system("git add .")
os.system(commit_command)
os.system("git push")