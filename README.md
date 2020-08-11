# Cav-Project

I was really tired of doing manual searches for secrets in files on github.
I Think we can all agree trufflehog is an amazing tool but it just doesnt search for repos for you. With that I am lazy, I don't want to manually pass info to that tool.
In the process of all my retardedness I decided I would use trufflehog3 because it had stated it could do pdf generation and html stuff and I wanted to form this tool into a shitty web app.
Not really sure what happened but it did not work so I just figured I would rewrite this soon and only use trufflehog.
Honestly with things I have seen in the last month or so this tool will become obsolete very quickly lol.
This tool netted me $3k in bounties...
uhm yeah use it or don't ¯\_(ツ)_/¯


## Installation
Python 3.7+ is required ~~because I dont want to write this again.~~ Although with some tweaks you can get it to work on any version of python you want.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirments.

*nix
```bash
pip3 install -r requirements
```

Windows 
```cmd.exe or powershell
pip3 install -r requirements
```

# Add GITHUB API TOKEN

Google how to generate a token for github
and add it to `g = Github(ACCESS_TOKEN)`

## Usage

Run `CAVEIRA.py` to activate the automation

*nix
```
python3 CAVEIRA.py
Enter A Domain Name[e.g example.com]:

```
Windows (RunAs Administrator plz)
```
python3 CAVEIRA.py
Enter A Domain Name[e.g example.com]:
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
Not sure yet what I am doing here ¯\_(ツ)_/¯

## Shout outs (ツ)
PatrickFarwick
