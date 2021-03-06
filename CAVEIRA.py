from github import Github
'''https://github.com/PyGithub/PyGithub'''
from truffleHog3 import core
'''https://pypi.org/project/truffleHog3/''' 
import time,csv,os,sys,re,git,json,shutil,tempfile,datetime
from urllib import parse
#access token for prod





g = Github(ACCESS_TOKEN)






domain = input('Enter A Domain Name[e.g example.com]: ')


search_keys = input('Did you want to search for specific secrets? Y or N  ')
if search_keys.upper() != 'N':
    keywords = input('Enter some keywords[e.g secret OR password]: ')
else:
    keywords = "password OR secret OR oauth"

search_rel = input('Did you want to search relevant results?  Y OR N  ')
if search_rel.upper() != 'N':
    relevant = datetime.date.today() - datetime.timedelta(days=90)
    pushed = "pushed:{}".format(relevant.strftime('%Y-%m-%d'))
else:
    pushed = ""
    print("Searching all results")







class caveira:
    '''caveira.py is a pyhton script used to get you creds off of github faster and more
        efficently get through all the bull shit in record time'''
    def __init__(self,g,domain,keywords,search_rel):
        self.domain = domain
        self.g = g
        self.q = '"'+domain+'"' + keywords + search_rel
        self.lst = []
        self.tmppathlst = []
        self.interesting_files_links = []
        self.interesting_both = []
        self.gitpath = ""
        #self.dictionary = defaultdict(list)
        self.searchgit(g,self.q)
        return None
    
    def csv(self,lst):
        '''To export data into csv'''
        #Debug Type
        #print(lst)
        #print(self.interesting_both)

        #stupid fucking way to remove dupes lol
        templst = []
        for urls in self.interesting_both:
            key, value = urls.split(': ')
            if key not in templst:
                templst.append(key)

            if value not in templst:
                templst.append(value)
        
        #print(templst)

        
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = 'intel-'+self.domain+"-"+timestr+".csv"
        path = os.path.dirname(os.path.abspath(filename))
        if os.path.isdir(path+"/CSV/")==False:
            os.mkdir(path+"/CSV/")
        with open('.\CSV\\'+'intel-'+self.domain+"-"+timestr+".csv", 'w', newline="") as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(["GIT LINKS","Interesting Files"])

            count = 1
            end = 0
            for word in lst:
                #Nicer format for shit :D
                wr.writerow([word])
            if os.name == 'nt':
                print("File Created at {}{}".format(path+"\CSV\\",filename))
            else:    
                print("File Created at {}{}".format(path+"/CSV/",filename))
        return path




    def searchgit(self,g,query):
        '''searchgit(g = github_access_token,query="domain name")'''
        lst = []
        rate_limit = g.get_rate_limit()
        rate = rate_limit.search
        if rate.remaining == 0:
            print(f'You have 0/{rate.limit} API calls remaining. Reset time: {rate.reset}')
            return
        else:
            print(f'You have {rate.remaining}/{rate.limit} API calls remaining')


        repositories = g.search_code(query=query, order='desc')
        print(f'Found {repositories.totalCount} file(s)')
        for repo in repositories:
            repo_download = f'{repo.download_url}'
            self.interesting_files_links.append(repo_download)
            repo_download = str(repo_download)
            
            git_url = repo_download[33::]
            #Strips specific file path into a .git url for scanning of secrets
            strip_character = "/"
            gitpath = strip_character.join(git_url.split(strip_character)[:3])
            gitpath_link= 'https://github.com'+gitpath+'.git'
            self.lst.append(gitpath_link)
            formating = "{}: {}".format(gitpath_link,repo_download)
            self.interesting_both.append(formating)
        self.lst = list(dict.fromkeys(self.lst))
        export_q1 = input("Would you like me to export the list to a CSV? Y OR N \n")
        if export_q1.upper() != 'N':
            print()
            self.csv(self.lst)
        else:
            print("Alright then")

          
        scan_q1 = input("Would you like me to scan the repo(s) for secrets with TruffleHog? Y OR N \n")
        if scan_q1.upper() != 'N' or 'n':
            #print("passed conditional")
            print()
            self.clone_git_repos(self.lst)
        else:
            print("Why are you using this tool then...\n")
            print("Just take the fucking list I dont want it now\n")
            print()
            print(self.lst)
        return self.lst
    
    def clone_git_repos(self, lst):
        lst1 = []
        count = 0
        log = ""
        company_url = self.domain
        
        path1 = input("Please Enter a path: ")
        for git_url in lst:
            foldername = git_url[19::]
            strip_character = "/"
            foldername = strip_character.join(foldername.split(strip_character))
            foldername = foldername.replace("/", "\\")
            foldername = foldername[:-4]
            #print(foldername)
            test = foldername.split("\\")
            username = test[0]
            filename = test[1]
            #google_drive_path = "G:\\My Drive\\Gits\\{}\\".format(company_url)
            google_drive_path = path1+"\\{}\\{}".format(company_url,username)
            m1 = path1+"\\{}".format(company_url)
            #print(google_drive_path)
            #Checks if path exsists already and shows path
            #print(git_url)
            if os.path.exists(m1):
                #skip
                print()
            else:
                os.mkdir(m1)

            
            if os.path.exists(google_drive_path):
                #skip
                print()
                print("Showing Temp Directories Below \n")
                print("Temp Directory for {}:{}".format(git_url,google_drive_path))
            else:
                os.mkdir(google_drive_path)
                git.Repo.clone_from(git_url,google_drive_path)
                print("Showing Temp Directories Below \n")
                print("Temp Directory for {}:{}".format(git_url,google_drive_path))
            lst1.append(google_drive_path)


            
        for path in lst1:
            issues = []
            count+=1
            print("Starting analysis on branch {} of {}\n".format(count,len(lst1)))
            issues.append(core.search_current(path))
            issues.append(core.search_history(path))
            #print(core.search_history(path))
            #print(core.search_current(path))
            print("logging issues to report {} of {}\n".format(count,len(lst1)))
            log = core.log(issues,output=False, json_output=True)
            #print(len(issues))
            if len(issues) == 2:
                print("{} in log so we are going to delete this repo as confidence is 0".format(log))
                shutil.rmtree(path)      
            else:
                with open(path+"\\"+'proof.json', 'w') as outfile:
                    #Log File should be in the root dir of git repos
                    json.dump(issues, outfile)

search1 = caveira(g,domain,keywords,search_rel)


