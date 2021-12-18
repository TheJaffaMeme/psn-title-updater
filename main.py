import urllib.request
import xml.etree.ElementTree as ET
import ssl
import sys


def titlecheck(titleid : str):
    try:
        resp = urllib.request.urlopen(f'https://a0.ww.np.dl.playstation.net/tpl/np/{titleid}/{titleid}-ver.xml', context=ssl._create_unverified_context())
        xml = ET.fromstring(resp.read().decode('utf-8'))
        return xml[0][0].attrib
    except urllib.error.HTTPError:
        return False

def report(blocknr, blocksize, size):
    current = blocknr*blocksize
    print("\r{0:.2f}%".format(100.0*current/size))

def titledownload(url: str, size: int):
    filename = url.split('/')[-1]
    try:
        urllib.request.urlretrieve(url, filename, report)
        return filename
    except (urllib.error.HTTPError, RuntimeError, TypeError, NameError):
        return False


titleid = str(sys.argv[1])

titleinfo = titlecheck(titleid=titleid)
if titleinfo == False:
    print("ERROR! Check Title ID and try again.")
    quit()

print(f"Downloading {titleinfo['url'].split('/')[-1]}\nVersion: {titleinfo['version']}\nSize: {titleinfo['size']}")
yn = str(input("Continue Download? (Y/N): ")).lower().strip()
if yn[0] == 'n':
    quit()
download = titledownload(url=titleinfo['url'], size=titleinfo['size'])
if download == False:
    print("ERROR! Unable to download title update.")
    quit()

print(f"DONE! Downloaded to {download}")
