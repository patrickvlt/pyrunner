import os

os.system('git add .')
os.system('git commit -m "Update"')
os.system('git tag -f v2.0')
os.system('git push')
os.system('git push -f --tags')