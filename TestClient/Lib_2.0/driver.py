__author__ = 'guow'
sys.path.append("C:\Windows\System32")
from xml.etree import ElementTree
from will import *
import string
from common import syncAdminRun
import glob

REALM = 'QuickBuild'
URL   = 'https://ubit-gfx.intel.com/'

def get_dir_list( path ):
    dir_file_list = os.listdir( path )

    dir_list = []
    for i in dir_file_list:
        if isdir(join_path(path, i)):
            dir_list.append(i)
    return dir_list

def installDrv( driver_igdlh_path ):
    os.system("%s\\tool\\devcon32.exe hwids =Display >tool\hwids.log" % os.getcwd())
    tool_path = 'tool'

    dev_path  = ''
    if driver_igdlh_path.endswith('igdlh.inf'):
        dev_path = join_path(tool_path, 'devcon32.exe')
    else:
        dev_path = join_path(tool_path, 'devcon64.exe')

    # uninstall drv
    run("tool\PnPutil.exe -e > pnp_e.log")
    fp = open('pnp_e.log')
    pnp_e_info = fp.read()
    fp.close()
    os.remove('pnp_e.log')

    pnp_info_list = pnp_e_info.split('\n')
    publish_name = ''
    display_publish_names = []
    for str in pnp_info_list:
        if str.endswith('inf'):
            publish_name = str
        if str.endswith('Display adapters'):
            display_publish_names.append(publish_name)

    oem_list = []
    for name in display_publish_names:
        oem_list.append(name.split()[-1])

    run('"%s" remove =Display' % dev_path)
    for oem_name in oem_list:
        run( 'tool\PnPutil.exe -f -d %s' % oem_name )
    run('"%s" rescan' % dev_path)

    # install drv
    fp = open('tool\hwids.log')
    hwids = fp.read()
    fp.close()
    os.remove('tool\hwids.log')

    hwids_list = hwids.split('\n')
    start_record = False
    display_hwids_list = []
    for str in hwids_list:
        str = str.strip()
        if str.startswith('Compatible IDs'):
            start_record = True
        if start_record and str.startswith('PCI\\VEN'):
            display_hwids_list.append(str)

    hwid = display_hwids_list[0]

    run( 'tool\PnPutil.exe -a %s' % driver_igdlh_path )
    cmd = r'%s update "%s" "%s"' % (dev_path, driver_igdlh_path, hwid)
    run(cmd)

def translator(frm='', to='', delete='', keep=None):
    if len(to) == 1:
        to = to * len(frm)
    
    trans = string.maketrans(frm, to)
    if keep is not None:
        trans_all = string.maketrans('', '')
        delete = trans_all.translate(trans_all, keep.translate(trans_all, delete))
        
    def translate(s):
        return s.translate(trans, delete)
        
    return translate
    
def get_url( url, user, pwd ):
    auth_handler = urllib2.HTTPBasicAuthHandler()
    auth_handler.add_password(realm=REALM,uri=url,user=user,passwd=pwd)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
    response = urllib2.urlopen(url)
    txt      = response.read()
    return txt

def get_build_id_by_name( ci_label, user, pwd ):
    txt = get_url(URL + "rest/builds?&version=%s&count=20" % (ci_label), user, pwd)
    xml = ElementTree.fromstring(txt)
    try:
        sml_bld_id = xml.find("com.pmease.quickbuild.model.Build").findtext("id")
    except:
        except_exit("Label:%s does not exist." % ci_label)
    for e in xml:
        id_info = e.findtext("id")
        if id_info < sml_bld_id:
            sml_bld_id = id_info
    return sml_bld_id

def get_windows_download_url( ci_label, build_id, build_type, arch ):
    drv_name = 'Driver-' + build_type + '-' + arch + '.7z'
    (ci_manual, branch, label) = ci_label.split('-')
    ci_flag = 'CI' if ci_manual == 'ci' else 'Manual'
    if branch == 'main':
        branch_flag = ci_flag + '-' + 'Main'
    elif branch == 'gen8_2014':
        branch_flag = ci_flag + '-' + 'Gen8_2014'
    elif branch == '15.33':
        branch_flag = ci_flag + '/' + '15.33'
    # file_url = ('https://ubitstore.intel.com/webstores/fm/sfa/Artifacts/Graphics/Builds/%s/Run/%s/builds/%s/artifacts/Windows/%s' % (ci_flag, branch_flag, build_id, drv_name) )
    # Published Download
    file_url = ("http://ubit-gfx.intel.com/download/%s/artifacts/Windows/%s" % (build_id, drv_name))
    return file_url

def get_download_data( download_url, user, pwd ):
    request = urllib2.Request(download_url)
    base64string = base64.encodestring('%s:%s' % (user, pwd)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    try:
        result = urllib2.urlopen(request)
    except:
        except_exit("Fail to download from %s" % download_url)
    println('Downloading Driver from QB...')
    txt = result.read()
    print('Finish')
    return txt

def download_file( download_url, dst_file, user=None, pwd=None ):
    # data = get_download_data(download_url, user, pwd)
    # f = open(dst_file, "wb")
    # f.write(data)
    # f.close()
    hr = multi_thread_http_file_download(download_url, dst_file, user , pwd )
    return hr

def unzip_7z( src_file, dst_file ):
    newline()
    println('<-- Unzip -->')
    print('Please wait when unzipping 7z driver binary...')
    run('"tool\\7z.exe" x %s -o%s' % (src_file, dst_file))
    print('Finish')

def downloadDrv( ci_label, build_type, arch, user=None, pwd=None ):
    if not isdir('drv'):
        mkdir('drv')

    drv_binary = join_path('drv', ci_label + '_' + build_type + '_' + arch)
    drv_binary_7z = join_path('drv', ci_label + '_' + build_type + '_' + arch + '.7z')
    if not isdir(drv_binary):
        build_id = get_build_id_by_name(ci_label, user, pwd)
        download_url = get_windows_download_url(ci_label, build_id, build_type, arch)
        print download_url
        hr = download_file( download_url, drv_binary_7z, user, pwd )
        if hr == 1:
            return 1
        time.sleep(1)
        unzip_7z( drv_binary_7z, drv_binary )
    else:
        println('Driver %s has already existed in drv.' % drv_binary)

    return drv_binary

if __name__ == '__main__':
    ci_label = sys.argv[1]
    build_type = sys.argv[2]
    arch = sys.argv[3]
    user = "youzhang"
    code = '>}?&{it^rdgl4@'
    decipher = translator(frm="^%Ip()&{}:>?80=MGLgld.",to="abcdefGuHISUJKLMNs2310")
    pwd =  decipher(code)
    drv_binary = downloadDrv(ci_label, build_type, arch, user, pwd)
    while drv_binary == 1:
        println('Reconnecting...')
        drv_binary = downloadDrv(ci_label, build_type, arch, user, pwd)
    infFileList = glob.glob(drv_binary+ '\*.inf')
    infFile = infFileList[0]
    print infFile
    newline()
    installDrv(infFile)