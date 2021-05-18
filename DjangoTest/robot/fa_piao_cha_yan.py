#coding:utf-8
import win32com.client as win32
import os,pandas as pd
import time,datetime,json
from selenium import webdriver
import time,requests
import random
import os, uuid, re
from PIL import Image
from selenium.webdriver.common.keys import Keys
from hashlib import md5
import xlrd,openpyxl
from multiprocessing import Process, Lock
import win32com.client
import zipfile
import shutil
import django
django.setup()
from robot.models import fa_piao_cha_yan

num=3  #开启进程数


#超级鹰账号，密码，ID
username = 'zgdcHZ'
password  =  '123!@#qwe'
soft_id  = '901924'
pic_id = ''#识别验证码返回的id

h = ''
d = ''
r = ''
j = ''
# global fu_path
# global Results_Screenshot,verification_Code,file_name
fu_path = ''
Results_Screenshot = ''
verification_Code =''
# fu_path=os.path.split(os.path.realpath(__file__))[0]  #根路径
# Results_Screenshot = fu_path + r'\Results_Screenshot' #结果截图路径
# verification_Code = fu_path + r'\verification_Code'   #验证码保存路径
file_name = '' #输入文件的路径

def browser():
    '''
    设置浏览器
    :return:
    '''
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('-headless')  # 设为无界面
    chromeOptions.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"')
    # chromeOptions.add_argument('--user-agent=Mozilla/5.0 HAHA')  # 配置对象添加替换User-Agent的命令
    chromeOptions.add_argument('--disable-infobars')  # 去掉提示：Chrome正收到自动测试软件的控制
    chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
    chromeOptions.add_experimental_option('useAutomationExtension', False)
    chromeOptions.add_argument('--disable-extensions')
    chromeOptions.add_argument('--ignore-certificate-errors')
    # chromeOptions.add_argument('--start-maximized')  # 最大化运行（全屏窗口）,不设置，取元素会报错
    driver = webdriver.Chrome(options=chromeOptions,
                              executable_path=r'chromedriver.exe')
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                    """
    })
    driver.set_window_size(1920, 1080)
    driver.set_page_load_timeout(120)  # 设置超时时间
    driver.get('https://inv-veri.chinatax.gov.cn/')
    time.sleep(5)
    return driver






def check_exsit(process_name='chromedriver.exe'):
    """
    监控多进程查验发票是否结束
    :param process_name: 进程名
    :return:
    """
    WMI = win32com.client.GetObject('winmgmts:')
    processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % process_name)
    if len(processCodeCov) > 0:
        print('%s is exists' % process_name )
        return False
    else:
        print('%s is not exists' % process_name )
        return True  #无进程

def get_process_count(imagename='chromedriver.exe'):
    p = os.popen('tasklist /FI "IMAGENAME eq %s"' % imagename)
    return p.read().count(imagename)

#平均分割列表
def bisector_list(origin_list, n):
    if len(origin_list) % n == 0:
        cnt = len(origin_list) // n
    else:
        cnt = len(origin_list) // n + 1
    for i in range(0, n):
        yield origin_list[i * cnt:(i + 1) * cnt]


def __check_popup(path,driver):
        """检查是否出现弹框"""
        popup_message=''
        print("判断查验前异常提示框...")
        html_source = driver.page_source
        popup_lst = re.findall("id=\"popup_container\"", html_source)
        if not popup_lst:
            #print("查询无异常弹框... ...")
            msg = '正常'
            return  msg

        popup_message = driver.find_element_by_id("popup_message").text
        sure_obj = driver.find_element_by_id("popup_ok")
        # logger.error(popup_message)
        msg = popup_message

        print('有弹框信息：>>>>', msg)
        if "错误" in popup_message:
            #print('验证码错误')
            #jietu(driver, msg)
            time.sleep(1)
            #jietu(driver, msg)
            driver.execute_script("arguments[0].click();", sure_obj)
            time.sleep(1)
            #jietu(driver,'关闭验证码')
            return msg
        else:
            #print('其他弹框信息')
            jietu(path,driver, d + '-' + h, areamx=False)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", sure_obj)
            time.sleep(1)
            return msg


def __input_check(driver,input_id, jy_id, context, path):
    """检查输入的数据是否正确"""
    try:
        if not context:
            return False
        driver.find_element_by_xpath("//*[@id='{}']".format(input_id)).clear()
        time.sleep(1)
        fp_obj = driver.find_element_by_xpath("//*[@id='{}']".format(input_id))
        fp_obj.send_keys(Keys.CONTROL, "a")
        # fp_obj.send_keys("")
        time.sleep(1)#random.uniform(1,2)
        fp_obj.send_keys(context.replace(",",""))
        time.sleep(1)
        jy_obj = driver.find_element_by_xpath("//*[@id='{}']".format(jy_id))
        jy_obj.click()
        time.sleep(1)

        if "有误" in jy_obj.text:
            # logger.error("输入信息有误：{}".format(context))
            jietu(path,driver,jy_obj.text+'-'+d+'-'+h,areamx=False)
            return False
        return True
    except Exception as e:
        print('报错了')
        print(e)
        return False


def m_get_timestr():
    """获取日期时间字符串"""
    stamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
    return stamp


def jietu(path,driver,fphm='默认',areamx=False):
    time.sleep(4)
    if areamx:
        print('截取成功后的区域图片')
        left = 380
        top = 1
        right = 1548
        bottom = 760
        names = str(fphm) + ".png"
        screen_shop = os.path.join(path + r'\Results_Screenshot', names)
        # print("++++++++++++++++++", screen_shop)
        a = Image.open(screen_shop)
        im = a.crop((left, top, right, bottom))
        im.save(screen_shop)
        time.sleep(1)
    else:
        names = str(fphm )+ ".png"
        screen_shop = os.path.join(path + r'\Results_Screenshot', names)
        driver.save_screenshot(screen_shop)  # 截图保存
        time.sleep(1)
    # print(screen_shop)


def __check_loaded(driver):
    """检查网页是否加载完成"""
    for i in range(60):
        try:

            fpdm = driver.find_element_by_xpath("//*[@id='fpdm']")
            if fpdm:
                print("页面加载完毕")
                break
        except Exception as e:
            print('页面加载出现异常---->',e)
        time.sleep(0.5)
        if i == 29:
            print("加载网页超时！")
            return '加载网页超时'
    return True


def __check_captcha_show(driver, path):
    """检查验证码图片是否显示"""
    for j in range(5):
        yzm_img = driver.find_element_by_id('yzm_img')
        for k in range(5):
            driver.execute_script("$(arguments[0]).click();", yzm_img)
            time.sleep(random.uniform(2,3))
            msg = __check_popup(path,driver)
            print(msg)
            if '正常'== msg:
                break
            else:
                continue
        # break


        base64_code = yzm_img.get_attribute('src')
        if "base64" not in base64_code:
            time.sleep(1)
            driver.execute_script("$(arguments[0]).click();", yzm_img)
            time.sleep(random.uniform(2, 3))
            continue

        verify_code_img = 'code{}.png'.format(uuid.uuid4())
        # captcha_root = os.path.join(r'验证码图片', "captcha")
        # if not os.path.exists(captcha_root):
        #     os.makedirs(captcha_root)
        print(verification_Code)
        verify_code_path = os.path.join(path + r'\verification_Code', verify_code_img)
        # print("***********************", verify_code_path)
        dd = driver.get_screenshot_as_file(verify_code_path)
        # dd.save(verify_code_path)
        # time.sleep(20)
        a = Image.open(verify_code_path)
        # print("***********************",verify_code_path)

        # phantomjs无界面浏览器

        # chrome无界面浏览器
        left = 995
        top = 550 -20
        right = 1480
        bottom = 660 -20
        # elif self.browser == "chrome":
        #     # chrome有界面
        # left = 990
        # top = 650
        # right = 1625
        # bottom = 825
        im = a.crop((left, top, right, bottom))
        # im=a.crop()
        im.save(verify_code_path)  # 保存验证码图片
        #time.sleep(5)
        # logger.info("验证码的图片路径：{}".format(verify_code_path))
        time.sleep(1)

        return verify_code_path

    # logger.error("验证码无法显示: {}".format(fpdm))
    return False


class MyClient(object):
    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()



# 返回验证码识别服务出错题分
def get_money_back():
    # confi_dict = get_conf_dict()
    # username = confi_dict["username"]
    # password = confi_dict["password"]
    # software_id = confi_dict["software_id"]
    chaojiying = MyClient(username, password, soft_id)

    #chaojiying = MyClient('chinahcl', '1qaz2wsx', '899681')  # 用户中心 >> 软件ID 生成一个替换 897915
    report_error = chaojiying.ReportError(pic_id)
    print("report_error", report_error)



class Chaojiying_Client(object):
    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


def m_distinguish_verifycode(verifycode_img_path):
    """识别图片验证码,针对发票查验网站的验证码形式"""
    if not os.path.exists(verifycode_img_path):
        #print("验证码图片路径不存在：{}".format(verifycode_img_path))
        return ""
    result = []
    # chaojiying = Chaojiying_Client('cpfcxb', '12345@qwert', '901924')  # 用户中心>>软件ID 生成一个替换 96001
    chaojiying = Chaojiying_Client(username, password, soft_id)  # 用户中心>>软件ID 生成一个替换 96001
    im = open(verifycode_img_path, 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    #result = chaojiying.PostPic(im, 6004)  # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
    try:
        result = chaojiying.PostPic(im, 6004)
    except:
        print("发送验证码图片到网络识别过程中出错")
        return '默认验证码'
        # get_money_back()
        # print("发送验证码图片到网络识别过程中出错")
        # results.append("EMERGENCY")
        # return results
    #print(result)
    err_str = result.get('err_str')
    err_no = result.get('err_no')
    global pic_id
    pic_id = result.get('pic_id')
    if err_str == "OK":
        # 识别成功
        v_code = result.get('pic_str', "")
        #print("识别成功的验证码pic_id:{}".format(pic_id))
        return v_code.upper()
    elif err_no == -1005:
        print("识别接口错误:{}".format(err_str))
        return -1005
    else:
        # 识别错误，返回题分
        print("识别错误的验证码pic_id:{}".format(pic_id))
        return err_str


def __input_verification(driver, path):
    '''
    :param driver:
    :param v_code:
    :return:
    '''
    v_code='222'
    verify_code_path = __check_captcha_show(driver, path)  # 检查验证码是否出现
    v_code = m_distinguish_verifycode(verify_code_path) #开始识别
    print("识别后的验证码：{}".format(v_code))
    if v_code == -1005:
        return '识别验证码出现异常'
    elif not v_code:
        return '识别验证码出现异常'
    # 识别后的验证码图片立即清除
    os.remove(verify_code_path)
    driver.find_element_by_id("yzm").clear()
    yzm_obj = driver.find_element_by_id("yzm")
    yzm_obj.send_keys(Keys.CONTROL, "a")
    # time.sleep(5)
    yzm_obj.send_keys(v_code)#v_code
    time.sleep(1)
    #jietu(driver, '111111')
    return True


def checkfp(driver):
    #点击查验按钮
    checkfp = driver.find_element_by_id("checkfp")
    driver.execute_script("arguments[0].click();", checkfp)
    time.sleep(2)



def _find_id(driver,id):
    #通过ID获取
    try:
        value = driver.find_element_by_id(id).text
        return value
    except:
        return ' '

def _find_xpath(driver,id):
    #通过节点获取
    try:
        if id == "je_zp":
            je_str = driver.find_element_by_id("je_zp").text
            je_lst = re.findall("\d.*", je_str)
            # time.sleep(2)
            if je_lst:
                je_str = je_lst[0]
                return je_str
        elif id == "se_zp":
            je_str = driver.find_element_by_id("je_zp").text
            je_lst = re.findall("\d.*", je_str)
            # time.sleep(2)
            if je_lst:
                je_str = je_lst[0]
            # 总税额
            zse_str = driver.find_element_by_id("se_zp").text
            zse_lst = re.findall("\d.*", zse_str)
            if je_lst:
                zse_str = zse_lst[0]
                return zse_str
        elif id=="cysj":
            cysj_str = driver.find_element_by_id("cysj").text
            cysj_lst = re.findall("\d.*", cysj_str)
            if cysj_lst:
                cysj_str = cysj_lst[0]
                return cysj_str

        value = driver.find_element_by_id(id).text
        return value
    except:
        return ' '


def __areamx(driver):
    #抓取存在销货清单数据
    #返回：[['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['*配电控制设备*故障录波装置', 'AC750,500kV', '套', '1', '32743.36283185841', '32743.36', '13%', '4256.64'], ['', '', '', '', '', '￥720353.92', '', '￥93646.08'], ['', '', '', '', '', '￥720353.92', '', '￥93646.08']]
    data=[]
    try:
        for i in range(2,100):
            data_1 = []
            for j in range(2,10):
                id_str = '//*[@id="print_areamx"]/table[2]/tbody/tr['+str(i)+']/td['+str(j)+']'
                info_str = driver.find_element_by_xpath(id_str).text
                data_1.append(info_str)
            data.append(data_1)
        return data
    except Exception as e:
        print("获取销货清单数据异常", e)
        return data

def get_information(path,driver,item):
    #抓取查验成功后的信息
    data1 = [item[0], item[1], item[3]]
    try:
        js = "return document.documentElement.outerHTML"
        html = driver.execute_script(js)
        #print(str(html))
        if "增值税专用发票<" not in str(html):
            return '非增值税专用发票'
        #通过ID获取数据信息
        id = ["jym_zp","jqbh_zp","gfmc_zp","gfsbh_zp","gfdzdh_zp","gfyhzh_zp","je_zp","se_zp",'jshjxx_zp',"xfmc_zp","xfsbh_zp","xfdzdh_zp","xfyhzh_zp",'bz_zp',"cycs","cysj"]
        for i in id:
            data1.append(_find_id(driver, i))
        time.sleep(2)
        jietu(path,driver,item[0]+"-"+ item[1],areamx=True)
        data1[9]=data1[9][1:]
        data1[10] = data1[10][1:]
        data1[11] = data1[11][1:]
        data2 = []
        if "查看货物明细清单<" in str(html) or '(详见销货清单)' in str(html):
            checkfp = driver.find_element_by_id("showmx")
            driver.execute_script("arguments[0].click();", checkfp)
            time.sleep(2)
            js = "return document.documentElement.outerHTML"
            html = driver.execute_script(js)
            #print(str(html))mxclose
            print("存在销货清单")
            data_ls = __areamx(driver)
            #print(data_ls)
            # jietu(driver,item[0] +"-"+ item[1]+"销货清单")
            for i in range(len(data_ls)-2):
                data2.append(data1 + data_ls[i])
            try:
                driver.find_element_by_id("mxclose").click()
                time.sleep(1)
                driver.find_element_by_id("closebt").click()
                time.sleep(2)
                return data2
            except Exception as e:
                print('点击关闭按钮异常',e)
                return data2

        try:
            base_tr = '//*[@id="tabPage2"]/div[1]/table[2]/tbody/tr[5]/td/table/tbody/tr'
            tr_lst = driver.find_elements_by_xpath(base_tr)
            if len(tr_lst) < 4:
                return "未获取到发票详细信息"

        except Exception as e:
            print("数据抓取意外出错---->",e)
            return "未获取到发票详细信息"
        data2 = []
        for x in range(1, len(tr_lst) - 2):
            fwmc_str = driver.find_element_by_xpath(base_tr + "[{}]/td[1]/span".format(str(x + 1))).text
            # 规格型号
            ggxh_str = driver.find_element_by_xpath(base_tr + "[{}]/td[2]/span".format(str(x + 1))).text
            # 单位
            dw_str = driver.find_element_by_xpath(base_tr + "[{}]/td[3]/span".format(str(x + 1))).text
            # 数量
            num_str = str(driver.find_element_by_xpath(base_tr + "[{}]/td[4]/span".format(str(x + 1))).text)
            # 单价
            price_str = str(driver.find_element_by_xpath(base_tr + "[{}]/td[5]/span".format(str(x + 1))).text)
            # 税前金额
            sqje_str = str(driver.find_element_by_xpath(base_tr + "[{}]/td[6]/span".format(str(x + 1))).text)
            # 税率
            sl_str = str(driver.find_element_by_xpath(base_tr + "[{}]/td[7]/span".format(str(x + 1))).text)
            # 税额
            se_str = str(driver.find_element_by_xpath(base_tr + "[{}]/td[8]/span".format(str(x + 1))).text)


            data = [fwmc_str, ggxh_str, dw_str, num_str, price_str, sqje_str, sl_str,se_str]
            #print(data)
            data2.append( data1+data)
            # print(data2)
        driver.find_element_by_id("closebt").click()
        time.sleep(2)
        return data2
    except Exception as e:
        print("抓取数据阶段出现异常===",e)
        #logger.error(str(e))


def __result(path,driver,item):
    #查验结果判断
    msg = __check_popup(path,driver)
    print("+++",msg)
    if "错误" in msg:
        return '验证码错误'
    elif "正常" not in msg:
        return msg
    try:
        # logger.info("开始切换到查询结果框架")
        driver.switch_to_frame("dialog-body")
        # jietu(path,driver, d + '-' + h, areamx=False)
        # js = "return document.documentElement.outerHTML"
        # html = driver.execute_script(js)
        # print(str(html))
        cyjg_text=""
        try:
            cyjg_text = driver.find_element_by_id("cyjg").text
        except:
            pass
        # logger.info(cyjg_text)
        if "无此票" in cyjg_text:
            driver.find_element_by_id("closebt").click()
            return "无此票"
        if "不一致" in cyjg_text:
            driver.find_element_by_id("closebt").click()
            return "不一致"
        else:
            return get_information(path,driver,item)
    except Exception as e:
        print('查验后的问题：>>>>>>>>>>>',e)
        return get_information(path,driver, item)
        #logger.error("存在此发票信息：{}".format(item[2]))



def get_year():
    year = datetime.date.today().year
    # print("year", year)
    return year


def get_today():
    today = datetime.date.today()
    today = str(today).replace("-", "")
    # print("today", today)
    return today


def write_json(result,num):
    '''

    :param result: 数据
    :param num: 进程号
    :return:
    '''
    pass


def writr_excel(result,num,mutex, path):
    #在表格写入查验结果
    mutex.acquire()
    #os.system('taskkill /IM EXCEL.EXE /F')
    today = get_today()
    col = ['发票代码', '发票号码', '开票日期', '校验码', '机器编号', '名称', '纳税人识别号', '地址电话', '开户银行及账号', '税前总金额', '总税额', '价税合计', '销售方名称',
           '销售方纳税人识别号', '销售方地址电话', '销售方开户银行及账号', '备注', '查验次数', '查验时间', '服务名称', '规格型号', '单位', '数量', '单价', '税前金额', '税率',
           '税额']
    col_ = ['01,01,发票代码，发票号码，税前合计金额，开票日期，，0123，', '问题反馈', '发票代码', '发票号码', '金额', '开票日期', '进程编号', '备注']
    # excel_path = today +"-增值税发票二维码数据.xls"
    result_path = os.path.join(path,today + "-抓取的数据结果.xlsx")
    excel=os.path.join(path,str(today)+'-查验过的发票.xlsx')
    #print(len(result))
    if len(result) == 8 and len(result[0])>35:
        result[-2]=num
        if not os.path.exists(excel):
            workbook=openpyxl.Workbook()
            worksheet=workbook.create_sheet('Sheet1',0)
            worksheet.append(col_)
            worksheet.append(result)
            workbook.save(excel)
            workbook.close()
        else:
            try:
                df = pd.read_excel(excel)
                ls = str(result[0]).strip()
                print(ls)
                index =df[(df['01,01,发票代码，发票号码，税前合计金额，开票日期，，0123，'] == ls) & (df['备注'] == ' ')].index.tolist()[0]
                df = df.drop([index], axis=0)
                df.to_excel(excel,index=False) #删除那一行然后在最后重新写
                workbook = openpyxl.load_workbook(excel)
                worksheet = workbook['Sheet1']
                worksheet.append(result)
                workbook.save(excel)
                workbook.close()
            except Exception as e:
                print('682行报错了')
                print(e) #没有那一行就直接最后写
                workbook = openpyxl.load_workbook(excel)
                worksheet = workbook['Sheet1']
                worksheet.append(result)
                workbook.save(excel)
                workbook.close()
        mutex.release()
        return
        # xls = xlrd.open_workbook(excel_path)
        # xlsx = copy(xls)
        # sheet = xlsx.get_sheet(0)
        # if result == '已抓取':
        #     sheet.write(num,7,result)
        # else:
        #     sheet.write(num, 1, result)
        # xlsx.save(excel_path)

        #mutex.release()


    if not os.path.exists(result_path):
        workbook=openpyxl.Workbook()
        worksheet=workbook.create_sheet('Sheet1',0)
        worksheet.append(col)
        for i in result:
            worksheet.append(i)
    else:

        workbook = openpyxl.load_workbook(result_path)
        worksheet = workbook['Sheet1']
        for i in result:
            worksheet.append(i)
    workbook.save(result_path)
    workbook.close()
    mutex.release()




def read_excel(num):
    #os.system('taskkill /IM EXCEL.EXE /F')

    #读取表格返回四要素列表
    data = []
    yes = []
    issue = []
    new = []
    df_ls_1 = []
    today = get_today()
    excel=file_name
    # print(excel)
    # return
    # excel_result=fu_path+"\\"+today + "-增值税发票二维码数据--查验结果.xlsx"
    if os.path.isfile(excel):# and os.path.isfile(excel_result): #返回剩余未查验的数据
        df_ls = pd.read_excel(excel).fillna(" ").values.tolist()
        #result = pd.read_excel(excel_result).values.tolist()
        #print(df_ls,111)
        for i in df_ls:
            # if i[2] != ' ' and i[3] != ' 'and i[4] != ' 'and i[5] != ' ' and i[0] != ' ':
            if i[2] != ' ' and i[3] != ' 'and i[4] != ' 'and i[5] != ' ':
                df_ls_1.append(i)
    #     for i in df_ls_1:
    #         for j in result:
    #             if i not in data:
    #                 new.append(i)
    # if os.path.isfile(today + "-增值税发票二维码数据--查验结果.xlsx"):
    #     result = pd.read_excel(today + "-增值税发票二维码数据--查验结果.xlsx").values.tolist()

    # for i in range(num):
    excel = fu_path+"\\"+str(today) + '-查验过的发票.xlsx'
    if os.path.isfile(excel):
        df = pd.read_excel(excel).fillna(" ").values.tolist()
        #print(len(df))
        for j in df:
            if j[-1] != '已抓取' and '不一致' not in j[1] and '无此票' not in j[1] and '有误' not in j[1]:
                issue .append(j)
            else:
                yes.append(j)
            data.append(j[0])
    print("一共有：",len(df_ls_1))
    for i in df_ls_1:
    # for j in result:
        if i[0] not in data:
            new.append(i)
    a=new+issue
    # print(len(yes))
    # print(len(issue))
    print("实际查验：",len(a))
    # print(len(df_ls_1))
    # print(len(data))
    #print(a)
    df_ls = bisector_list(a,num)
    b=[]
    for i in df_ls:
        b.append(i)
        #print(i)
    #print(df_ls)
    # print(len(df_ls))
    # print(a)
    if len(a):
        return b
    else:
        return False
    # for i in df_ls:
    #     invoice = []
    #     #if i[-1] == ' ' and i[1] == ' ':
    #     ls = str(i[0]).split(',')
    #     invoice.append(ls[2])
    #     invoice.append(ls[3])
    #     invoice.append(ls[4])
    #     invoice.append(ls[5])
    #     data.append(invoice)
    # print(df_ls)
    # return data


def input_info(driver,item, path):
    '''
    接收发票四要素列表
    返回查询结果
    :param item:
    :return:
    '''

    browser_ok = __check_loaded(driver)
    if browser_ok != '加载网页超时': #先检查网页是否打开完成
        try:
            # print('开始输入四要素')
            # 输入发票代码
            global d
            d=item[0]
            if not __input_check(driver,"fpdm", "fpdmjy", item[0], path):
                return  "发票代码有误"

            # 输入发票号码
            global h
            h = item[1]
            if not __input_check(driver,"fphm", "fphmjy", item[1], path):
                return "发票号码有误"

            # 输入开票日期
            global r
            r = item[3]
            if not __input_check(driver,"kprq", "kprqjy", str(item[3]), path):
                return "开票日期有误"

            # 输入开具金额
            global j
            j = item[2]
            if not __input_check(driver,"kjje", "kjjejy", item[2], path):
                return "开具金额有误"

            #输入验证码
            if not __input_verification(driver, path):
                return '识别验证码出现异常'

            print('点击查验按钮')
            checkfp(driver)

            #截取图片
            jietu(path,driver, item[0] +"-"+ item[1])
            print("已截图")

            #开始返回结果
            print("开始抓取数据")
            result = __result(path,driver, item)

            #追回超级鹰扣分
            chaojiying = Chaojiying_Client(username, password, soft_id)
            chaojiying.ReportError(pic_id)

            for i in range(5):
                if "错误" in result or "失效" in result:
                    chaojiying = Chaojiying_Client(username, password, soft_id)
                    chaojiying.ReportError(pic_id)
                    __input_verification(driver, path)
                    #print('点击查验按钮')
                    checkfp(driver)
                    jietu(path,driver, item[0] + "-" + item[1])
                    print("已截图")
                    result = __result(path,driver, item)
                else:
                    return result
            return result
        except Exception as e:
            print(">>>",e)
            return "其他错误"

    elif browser_ok =='加载网页超时' :
        return '加载网页超时'



def main(df_ls,mutex,num, path):
    '''

    :param df_ls:被平均拆分后的发票四要素
    :param mutex: 互斥锁
    :param num: 第几个进程
    :return:
    '''
    driver = browser()
    #print(df_ls)
    for i in range(len(df_ls)):
        # os.system('taskkill /IM EXCEL.EXE /F')
        invoice = []
        if df_ls[i][-1] == ' ' and df_ls[i][0] != ' ':
            #print(df_ls[i])
            #print(len(df_ls[i][0]),df_ls[i][0])
            ls = str(df_ls[i][0]).split(',')
            invoice.append(ls[2])
            invoice.append(ls[3])
            invoice.append(ls[4])
            invoice.append(ls[5])
            #print(invoice)
            # for j in range(10):
            result = input_info(driver, invoice, path) #传入发票四要素，返回查验结果
            print(result)
            if isinstance(result,list):
                writr_excel(result,num,mutex, path)
                df_ls[i][-1]='已抓取'
                df_ls[i][1] = ' '
                writr_excel(df_ls[i],num,mutex, path)
            # elif '加载网页超时' == result:
            #     driver.close()
            #     time.sleep(3)
            #     driver = browser()
            #     df_ls[i][1] = result
            #     writr_excel(df_ls[i], num, mutex)
            #     # writr_excel(result, num,mutex)
            else:
                driver.close()
                time.sleep(3)
                driver = browser()
                df_ls[i][1] = result
                writr_excel(df_ls[i], num, mutex, path)
                # writr_excel(result,num,mutex)
    driver.close()


def begin(num, df_ls,path,file_name_zip,id):
    mutex = Lock()
    for i in range(num):
        # if len(df_ls[i])>0:
        p = Process(target=main, args=(df_ls[i], mutex, i, path))
        p.start()
        p.join()
    print('全部查验结束')
    print('开始压缩')
    time.sleep(2)
    make_zip(path, file_name_zip)
    print('压缩文件创建成功')
    change_info = fa_piao_cha_yan.objects.get(id=id)
    print('change_info.file----->>>>', change_info.file)
    change_info.file_state = '3'
    change_info.down_file = file_name_zip.split('upload\\')[1]
    change_info.save()
    shutil.rmtree(path)

def taskkill():
    try:
        os.system('taskkill /IM chromedriver.exe /F')
        os.system('taskkill /IM chrome.exe /F')
        os.system('taskkill /IM EXCEL.EXE /F')
    except:
        pass

def if_number_(file_name):
    list_info=[]
    today = get_today()
    data_info=pd.read_excel(file_name)
    list_data=data_info.values.tolist()
    # print(str(data_info.values.tolist()))
    for ii in list_data:
        list_str=[]
        for i in ii:
            print(i)
            if str(i) !='nannannannannannannannan':
                list_str.append(str(i))
        list_info.append(''.join(list_str))
    print(len(set(list_info)))
    # print(list_info)
    # time.sleep(20)
    # number_=(len(set(list_info)))
    # print(number_)
    # print(set(data_info.values.tolist()))
    # use_uoload_loc=data_info.shape[0]
    excel = fu_path + "\\" + str(today) + '-查验过的发票.xlsx'
    print('---->>>>>',excel)
    data_info=pd.read_excel(excel)
    create_loc=data_info.shape[0]
    print(create_loc,len(set(list_info)))
    if len(set(list_info)) != create_loc:
        return False
    return True

def if_number(file_name):
    list_info=[]
    today = get_today()
    data_info=pd.read_excel(file_name).fillna("__")
    list_data=data_info.values.tolist()
    print(list_data)
    n=0
    for ii in list_data:
        if ii[0]!= '__':
            n+=1
    print(n)
    excel = fu_path + "\\" + str(today) + '-查验过的发票.xlsx'
    data_info=pd.read_excel(excel)
    create_loc=data_info.shape[0]
    # print()
    print(create_loc,create_loc)
    if n != int(create_loc):
        return False
    return True

def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
          pathfile = os.path.join(parent, filename)
          arcname = pathfile[pre_len:].strip(os.path.sep)   #相对路径
          zipf.write(pathfile, arcname)
    zipf.close()


def __start(id,path):
    path_file=path.split('\\')
    # print(path_file)
    # return
    global fu_path,Results_Screenshot,verification_Code,file_name
    fu_path = path
    file_name = os.path.join(path,path_file[-1]+'.xlsx')
    file_name_zip = os.path.join(path + '.zip')
    Results_Screenshot = path + r'\Results_Screenshot'
    verification_Code = path + r'\verification_Code'
    if not os.path.exists(Results_Screenshot):
        os.mkdir(Results_Screenshot)
    if not os.path.exists(verification_Code):
        os.mkdir(verification_Code)
    # print(fu_path,Results_Screenshot,verification_Code)
    # return
    for i in range(2):#一共查验2轮
        taskkill() #清理进程
        df_ls = read_excel(num)
        # return

        if not df_ls:
            print("无可查验的发票")
            break   #无可查验的发票
        #print(df_ls)
        for i in df_ls:
            print(len(i))
        begin(num,df_ls,path,file_name_zip,id) #开始启动多进程
        time.sleep(10)
        # while True: #判断当前是否查验结束
        #     time.sleep(20)
        #     try:
        #         if if_number(file_name):
        #             print('结束')
        #             break
        #     except Exception as e:
        #         print("************************",e)
    # print('全部查验结束')
    # print('开始压缩')
    # time.sleep(2)
    # make_zip(path,file_name_zip)
    # print('压缩文件创建成功')
    # change_info = fa_piao_cha_yan.objects.get(id=id)
    # print('change_info.file----->>>>', change_info.file)
    # change_info.file_state = '3'
    # change_info.down_file = file_name_zip.split('upload\\')[1]
    # change_info.save()
    # shutil.rmtree(path)

def main_test():
    a=r'D:\yingda_project\ying_da\DjangoTest\upload\fa_piao_cha_yan\2021\04\09\mmm_3'
    __start(32,a)

def main_start(id,path):
    print('开始调用机器人')
    a = path
    # path=os.path.split(os.path.realpath(__file__))[0]
    __start(id,a)
    # change_info = fa_piao_cha_yan.objects.get(id=id)
    # print('change_info.file----->>>>', change_info.file)
    # change_info.file_state = '3'
    # change_info.save()
    # print('jiqirenyunxing jie shu')






#
if __name__ == '__main__':
    main_test()
    # path=r'D:\yingda_project\ying_da\DjangoTest\upload\fa_piao_cha_yan\2021\04\02\20201113-1-增值税发票二维码数据'
    # path_1=r'D:\yingda_project\ying_da\DjangoTest\upload\fa_piao_cha_yan\2021\04\02\20201113-1-增值税发票二维码数据.zip'
    # make_zip(path, path_1)
    # check_exsit()
    # file_name='D:\\yingda_project\\ying_da\\DjangoTest\\upload\\fa_piao_cha_yan\\2021\\04\\09\\mmm_3\\20210412-查验过的发票.xlsx'
    # file_name=r'D:\yingda_project\ying_da\DjangoTest\upload\fa_piao_cha_yan\2021\04\09\mmm_3\20210412-查验过的发票.xlsx'
    # if_number(file_name)


    pass
