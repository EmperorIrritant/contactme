from bs4 import BeautifulSoup
from sys import argv

html_filename = "contactme.no_keys.html"
updatedhtml_filename = "contactme.html"
configfile = argv[-1]

cognito_id_text = "IdentityPoolId:"
pubkey_text = "let publickeypem ="
queue_url_text = "QueueUrl:"

with open(configfile, 'r') as config:
    config_val = config.read().split("\n")
    config_val.remove('')
    cognito_id, pubkey, queue_url = config_val

cognito_id_text_replace = f"{cognito_id_text} '{cognito_id}'" + "}); //"
pubkey_text_replace = f"{pubkey_text} `{pubkey}`; //"
queue_url_text_replace = f"{queue_url_text} '{queue_url}', //"

with open(html_filename, 'r') as html:
    soup = BeautifulSoup(html, "lxml")

script = soup.findAll('script', attrs={'id': 'config'})[0]
script_text = str(script.contents[0])
script.contents[0].replaceWith(script_text.replace(cognito_id_text, cognito_id_text_replace).replace(pubkey_text, pubkey_text_replace).replace(queue_url_text, queue_url_text_replace))

with open(updatedhtml_filename, 'w') as html_file:
    html_file.write(soup.prettify())