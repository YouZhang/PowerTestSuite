from xml.etree import ElementTree
import wmi
import urllib2
import base64
import threading
import os
import time
import sys

def newline():
    print('')

def println( s ):
    newline()
    print(s)

def except_exit( except_info ):
    newline()
    print(except_info)
    raw_input('Press <Enter> key to exit...')
    exit()

def isfile( path ):
    return os.path.isfile(path)

def isdir( path ):
    return os.path.isdir(path)

def mkdir( path ):
    os.mkdir(path)

def join_path( path1, path2 ):
    rt = os.path.join( path1, path2 )
    return rt

def run( cmd_str ):
    os.system( cmd_str )

def get_http_file_size( url, user=None, pwd=None ):
    try:
        request = urllib2.Request(url)
        if user != None:
            base64string = base64.encodestring('%s:%s' % (user, pwd)).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)
        result = urllib2.urlopen(request)
        length = int( result.headers.dict['content-length'] )
    except:
        except_exit('Fail to get http file size.')
    return length

def split_file_size( file_size, block_num ):
    ranges = []
    block_size = file_size / block_num
    for i in xrange(block_num-1):
        ranges.append( (i*block_size, i*block_size+block_size-1) )
    ranges.append( (block_size*(block_num-1), file_size-1) )
    return ranges

def is_alive( ts ):
    for t in ts:
        if t.isAlive():
            return True
    return False

class HttpDownloadThread( threading.Thread ):
    def __init__(self, name, url, filename, range=0, user=None, pwd=None):
        threading.Thread.__init__(self, name=name)
        self.url = url
        self.filename = filename
        self.range = range
        self.user  = user
        self.pwd   = pwd
        self.total_length = range[1] - range[0] + 1
        try:
          self.downloaded = os.path.getsize(self.filename)
        except OSError:
          self.downloaded = 0
        self.percent = self.downloaded / float(self.total_length) * 100
        self.header_range = (self.range[0]+self.downloaded, self.range[1])
        self.buffer_size = 8192

    def run(self):
        try:
            self.downloaded = os.path.getsize(self.filename)
        except OSError:
            self.downloaded = 0
        self.percent = self.downloaded / float(self.total_length) * 100
        self.buffer_size = 8192
        self.header_range = (self.range[0]+self.downloaded, self.range[1])
        request = urllib2.Request(self.url)
        if self.user != None:
            base64string = base64.encodestring('%s:%s' % (self.user, self.pwd)).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header('Range', 'bytes=%d-%d' % self.header_range)
        opener = urllib2.build_opener()
        result = opener.open(request)
        start_time = time.time()
        while self.downloaded < self.total_length:
            remain_size = self.total_length - self.downloaded
            if (remain_size < self.buffer_size):
                data = result.read(remain_size)
            else:
                data = result.read(self.buffer_size)
            self.downloaded += len(data)
            f = open(self.filename, 'ab')
            f.write(data)
            f.close()
            self.time = int(time.time() - start_time)
            self.percent = self.downloaded / float(self.total_length) * 100

def multi_thread_http_file_download( url, dst_file_name=None, user=None, pwd=None, thread_num=15 ):
    length = get_http_file_size(url, user, pwd)
    mb = length/1024/1024.0
    block_num = thread_num
    if dst_file_name:
        filename = dst_file_name
    else:
        dst_file_name = url.split('/')[-1]
    ranges = split_file_size(length, block_num)
    names = ["%s_%d" %(dst_file_name,i) for i in xrange(block_num)]

    ts = []
    for i in xrange(block_num):
        t = HttpDownloadThread(i, url, names[i], ranges[i], user, pwd)
        t.setDaemon(True)
        t.start()
        ts.append(t)

    live = is_alive(ts)
    start_size = sum([t.downloaded for t in ts])
    start_time = time.time()
    exec_time = 0
    time.sleep(1)

    i = 1
    d_pre    = 0.00
    d_record = 0.00
    while live:
        exec_time = time.time() - start_time
        d = sum([t.downloaded for t in ts]) / float(length) * 100
        downloaded_this_time = sum([t.downloaded for t in ts])-start_size
        rate = downloaded_this_time / float(exec_time) / 1024
        if d_pre == d:
            rate = 0.0
            i += 1
        else:
            i = 1

        d_pre = d

        if i%50 == 0:
            if d_record == d:
                return 1
            d_record = d

        progress_string = u'\rFilesize: %.2fM Downloaded: %.2f%% Avg rate: %.1fKB/s' %(mb, d, rate)
        sys.stdout.write(progress_string)
        sys.stdout.flush()
        live = is_alive(ts)
        time.sleep(0.2)


    newline()
    print('Generating final driver binary...')
    f = open(dst_file_name, 'wb')
    for n in names:
        f.write(open(n,'rb').read())
        os.remove(n)
    f.close()
    print('Finish')
    return 0

REALM = 'QuickBuild'
URL   = 'https://ubit-gfx.intel.com/'

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
    try:
        data = get_download_data(download_url, user, pwd)
        f = open(dst_file, "wb")
        f.write(data)
        f.close()
    except:
        print "cannot download the driver!"
        return -1
    # hr = multi_thread_http_file_download(download_url, dst_file, user , pwd )
    return 0

def unzip_7z( src_file, dst_file ):
    newline()
    println('<-- Unzip -->')
    print('Please wait when unzipping 7z driver binary...')
    run('"tool\\7z.exe" x %s -o%s' % (src_file, dst_file))
    print('Finish')

def launch( ci_label, build_type, arch, user=None, pwd=None ):
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

    return 0

def getSysVersion():
    sysInfo = {}
    c = wmi.WMI ()
    for system in c.Win32_OperatingSystem():
        sysInfo["OS"] = system.Caption.encode("UTF8")
        sysInfo["buildNum"] = system.BuildNumber
        sysInfo["arch"] = system.OSArchitecture.encode("UTF8")
    return sysInfo

def getUserInfo(keyFile):
    userInfo = open(keyFile,'r').readlines()
    userName = base64.decodestring(userInfo[0])
    password = base64.decodestring(userInfo[1])
    return userName,password


if __name__ == '__main__':    
    ci_label = sys.argv[1]
    build_type = sys.argv[2]
    arch = getSysVersion()["arch"]
    # title
    print('***********************')
    print('*** Driver Download ***')
    print('***********************')
    user,pwd = getUserInfo('key')
    # run
    println('<-- Download Driver -->')
    print('Please wait when downloading driver to drv...')
    hr = launch(ci_label, build_type, arch, user, pwd)
    if( hr == 0):
        print "Download finished!"
    else:
        print "Download Failed!"