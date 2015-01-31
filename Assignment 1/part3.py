from pygithub3.services.repos import Repo

'''
cmd = "git shortlog -s -n"

os.chdir("C:\Users\DhruvOhri\Documents\COMP 6411\pygithub3-0.3")
os.system("git clone https://github.com/poise/python.git")
os.chdir("/home/d/d_ohri/Desktop/python")
output = commands.getoutput(cmd) 
print(output)
raw_input("press enter to continue")

'''

#r = github3.repository('poise', 'python') 
r = Repo()
r1 = r.list_contributors('poise','python')
for page in r1:
    for resource in page:
        print resource


