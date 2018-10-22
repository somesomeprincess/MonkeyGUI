import tkinter as tk
import subprocess, os, threading, yaml, shutil
from tkinter import ttk
from time import *

class MonkeyGUI:
    def __init__(self):

        self.root = tk.Tk()
        self.root.title('MonkeyGUI v_0.1')
        if (os.path.getsize('param.yml')):
            self.get_param()
        else:
            shutil.copy('param_default.yml', 'param.yml')
            self.get_param()
        self.check_logfile_exist('monkeylog')
        self.log_dir = os.path.abspath('monkeylog')+'\\'

    def check_logfile_exist(self,dir):
        if(not os.path.exists('/'.join([os.getcwd(),dir]))):
            os.mkdir(dir)
    def get_param(self):
        with open('param.yml', 'r') as f:
            if (f):
                self.param = yaml.load(f)

    def create_GUI(self):
        rowid, rowruntime, rowseed, rowanr, rowpkg, rowthrottle, rowscript, rowself, rowblack, rowcrash, rowexcep, rowrun, rowlog = list(
            range(2, 15))
        PADDING = 6
        col_lable, col_text = 0, 1
        self.frame = tk.Frame(self.root, borderwidth=2)
        self.frame.pack()

        self.title = tk.Label(self.frame, text="Monkey GUI", font=('微软雅黑', 16))
        self.title.grid(row=1, columnspan=3)

        # 测试设备
        lb_device = tk.Label(self.frame, text='测试设备：')
        lb_device.grid(row=rowid, column=col_lable, padx=PADDING, pady=PADDING)
        self.tx_shebeihao = tk.Entry(self.frame)
        self.tx_shebeihao.grid(row=rowid, column=col_text, padx=PADDING, pady=PADDING)
        lb_device_tip = tk.Label(self.frame, text='[空,-d,-e,设备id]')
        lb_device_tip.grid(row=rowid, column=2, padx=PADDING, pady=PADDING)
        # self.btn_getshebeihao = tk.Button(self.frame, text="获取设备号", command=self.btn_click)
        # self.btn_getshebeihao.grid(row=rowid,column=col_lable,padx=PADDING,pady=PADDING)
        # 运行次数
        runtimes = tk.Label(self.frame, text='*事件次数[必填]：')
        runtimes.grid(row=rowruntime, column=col_lable, padx=PADDING, pady=PADDING)
        self.tx_runtimes = tk.Entry(self.frame)
        self.tx_runtimes.grid(row=rowruntime, column=col_text, padx=PADDING, pady=PADDING)
        # seed
        lb_seed = tk.Label(self.frame, text='seed值:')
        lb_seed.grid(row=rowseed, column=col_lable, padx=PADDING, pady=PADDING)
        self.tx_seed = tk.Entry(self.frame)
        self.tx_seed.grid(row=rowseed, column=col_text, padx=PADDING, pady=PADDING)
        # crash继续
        self.intvar_crash = tk.IntVar(self.frame)

        cb_crash = tk.Checkbutton(self.frame, variable=self.intvar_crash, text='Crash后继续')
        cb_crash.grid(row=rowcrash, column=col_lable, padx=PADDING, pady=PADDING)

        # anr继续
        self.intvar_anr = tk.IntVar(self.frame)

        cb_anr = tk.Checkbutton(self.frame, variable=self.intvar_anr, text='ANR后继续')
        cb_anr.grid(row=rowcrash, column=col_text, padx=PADDING, pady=PADDING)
        #
        self.intvar_secur = tk.IntVar(self.frame)

        cb_anr = tk.Checkbutton(self.frame, variable=self.intvar_secur, text='SecurityException后继续')
        cb_anr.grid(row=rowcrash, column=2, padx=PADDING, pady=PADDING)
        # 包名
        lb_pkg_tip = tk.Label(self.frame, text='[ , 分隔 ]')
        lb_pkg_tip.grid(row=rowpkg, column=2, padx=PADDING, pady=PADDING)
        self.tx_pkg = tk.Entry(self.frame)
        self.tx_pkg.grid(row=rowpkg, column=col_text, padx=PADDING, pady=PADDING)
        lb_pkg = tk.Label(self.frame, text='包名:')
        lb_pkg.grid(row=rowpkg, column=col_lable, padx=PADDING, pady=PADDING)
        # 延时
        lb_throttle = tk.Label(self.frame, text='延时（ms）:')
        lb_throttle.grid(row=rowthrottle, column=col_lable, padx=PADDING, pady=PADDING)
        self.tx_throttle = tk.Entry(self.frame)
        self.tx_throttle.grid(row=rowthrottle, column=col_text, padx=PADDING, pady=PADDING)
        lb_throttle = tk.Label(self.frame, text='[<0 : 随机延时; Default: 500]')
        lb_throttle.grid(row=rowthrottle, column=2, padx=PADDING, pady=PADDING)
        # 黑白名单
        self.blackwrite = tk.StringVar(self.frame)
        # self.blackwrite.grid(row=rowblack, padx=PADDING, pady=PADDING)
        # blacklist = tk.Radiobutton(self.frame, text='黑名单', variable=self.blackwrite, value=1)
        # blacklist.select()
        # blacklist.grid(row=rowblack, column=0)
        # writelist = tk.Radiobutton(self.frame, text='白名单', variable=self.blackwrite, value=2)
        # writelist.grid(row=rowblack, column=1)
        cb_comp = ttk.Combobox(self.frame, textvariable=self.blackwrite)
        cb_comp.grid(row=rowblack, column=0, padx=PADDING, pady=PADDING)
        cb_comp['values'] = ['黑名单', '白名单']
        cb_comp['state'] = 'readonly'
        cb_comp.set('黑名单')

        self.tx_blackwrite = tk.Entry(self.frame)
        self.tx_blackwrite.grid(row=rowblack, column=1, padx=PADDING, pady=PADDING)
        lb_throttle = tk.Label(self.frame, text='[选填;填写push到手机的路径]')
        lb_throttle.grid(row=rowblack, column=2, padx=PADDING, pady=PADDING)
        # 同时保存logcat
        self.intvar_savelogcat = tk.IntVar(self.frame)

        cb_savelogcat = tk.Checkbutton(self.frame, variable=self.intvar_savelogcat, text='同时保存logcat')
        cb_savelogcat.grid(row=rowexcep, column=0, padx=PADDING, pady=PADDING)
        # 异常log分开
        self.intvar_seperr = tk.IntVar(self.frame)

        cb_seperr = tk.Checkbutton(self.frame, variable=self.intvar_seperr, text='异常log分开')
        cb_seperr.grid(row=rowexcep, column=1, padx=PADDING, pady=PADDING)
        cb_seperr.select()
        # 保存至电脑
        self.strvar_comp = tk.StringVar(self.frame)

        cb_comp = ttk.Combobox(self.frame, textvariable=self.strvar_comp)
        cb_comp.grid(row=rowexcep, column=2, padx=PADDING, pady=PADDING)
        cb_comp['values'] = ['保存至电脑', '保存至手机']
        cb_comp['state'] = 'readonly'
        # self.strvar_comp.set('保存至电脑')
        cb_comp.set('保存至电脑')

        # 运行
        btn_run = tk.Button(self.frame, text='RUN', command=self.click_run)
        btn_run.grid(row=rowrun, column=col_lable, padx=PADDING, pady=PADDING)
        btn_stop = tk.Button(self.frame, text='保存参数', command=self.closing_save_para)
        btn_stop.grid(row=rowrun, column=col_text, padx=PADDING, pady=PADDING)
        self.text_log = tk.Listbox(self.frame, width=70)
        self.text_log.grid(row=rowlog, columnspan=3, padx=PADDING, pady=PADDING)
        #测试按钮
        btn_test = tk.Button(self.frame, text='测试按钮', command=self.find_abnormal_keywd)
        btn_test.grid(row=rowrun, column=2, padx=PADDING, pady=PADDING)
        # 脚本
        lb_script = tk.Label(self.frame, text='monkeyScript:')
        lb_script.grid(row=rowscript, column=col_lable, padx=PADDING, pady=PADDING)
        self.tx_script = tk.Entry(self.frame)
        self.tx_script.grid(row=rowscript, column=col_text, padx=PADDING, pady=PADDING)
        # 自定义
        lb_self = tk.Label(self.frame, text='自定义:')
        lb_self.grid(row=rowself, column=col_lable, padx=PADDING, pady=PADDING)
        self.tx_self = tk.Entry(self.frame)
        self.tx_self.grid(row=rowself, column=col_text, padx=PADDING, pady=PADDING)
        lb_self = tk.Label(self.frame, text='[-c,--pct-touch,--bugreport,etc]')
        lb_self.grid(row=rowself, column=2, padx=PADDING, pady=PADDING)
        # v级别
        self.combo_var = tk.StringVar()
        combo_v = ttk.Combobox(self.frame, textvariable=self.combo_var)
        combo_v.grid(row=rowruntime, column=2, padx=PADDING, pady=PADDING)
        combo_v.set('日志级别')
        combo_v['values'] = ['-v', '-v -v', '-v -v -v', '']
        combo_v['state'] = 'readonly'
        # shebeihao.pack()
        # btn_getshebeihao.pack()
        # self.et_shebeihao.pack()
        # self.root.protocol("WM_DELETE_WINDOW", self.closing_save_para)
        # messagebox.askokcancel("退出吗")
        self.set_default_value()
        self.root.mainloop()

    def set_default_value(self):
        self.tx_runtimes.insert(0, self.param['runtimes'])
        self.tx_shebeihao.insert(0, self.param['deviceid'])
        self.tx_seed.insert(0, self.param['seed'])
        self.intvar_crash.set(self.param['crashgoon'])
        self.intvar_anr.set(self.param['anrgoon'])
        self.intvar_secur.set(self.param['securgoon'])
        self.tx_blackwrite.insert(0, self.param['bwlisfile'])
        self.tx_pkg.insert(0, self.param['pkg'])

    def closing_save_para(self):
        with open('param.yml', 'w') as f:
            yaml.dump(self.param, f)
        self.text_log.insert(1, '保存参数成功！')

    def check_param(self):
        pkg = self.tx_pkg.get()
        if (pkg):
            self.param['pkg'] = pkg
            if(',' in pkg):
                pkg = ' '.join(['-p ' + i for i in pkg.split(',')])
            else :
                pkg = ' '.join(['-p', pkg])

        times = self.tx_runtimes.get()
        if (not times):
            self.text_log.insert(tk.END, '请输入测试次数！')
            return
        self.param['runtimes'] = times
        shell = 'adb shell'
        shebeihao = str(self.tx_shebeihao.get())
        if (shebeihao):
            self.param['deviceid'] = shebeihao
            if (shebeihao == '-d'):
                shell = 'adb -d shell'
            elif (shebeihao == '-e'):
                shell = 'adb -e shell'
            else:
                shell = ' '.join(['adb','-s','shell', shebeihao])
        crash_goon = self.intvar_crash.get()
        self.param['crashgoon'] = crash_goon
        crash = ''
        if (crash_goon):
            crash = '--ignore-crashes'
        anr_goon = self.intvar_anr.get()
        self.param['anrgoon'] = anr_goon
        anr = ''
        if (anr_goon):
            anr = '--ignore-timeouts'
        secur_goon = self.intvar_secur.get()
        self.param['securgoon'] = secur_goon
        secur = ''
        if (secur_goon):
            secur = '--ignore-security-exceptions'
        #延时
        throttle = self.tx_throttle.get()
        if (not throttle):
            throttle = 500
        try:
            throttle = int(throttle)
        except Exception as e:
            self.text_log.insert(tk.END, e)
            return
        self.param['throttle'] = throttle
        if(throttle >0):
            throttle = '--throttle ' + str(throttle)
        else:
            throttle = '--randomize-throttle'
        seed = self.tx_seed.get()
        if (seed):
            self.param['seed'] = seed
            seed = '-s ' + seed
        # 自定义
        selflize = self.tx_self.get()
        self.param['self'] = selflize
        # log V
        logv = self.combo_var.get()

        if ('日志级别' == logv):
            logv = '-v'
        self.param['logv'] = logv
        #monkeyscript
        script=self.tx_script.get()
        if(script):
            self.param['monkeyscript'] = script
            script = '-f '+script
            pkg = ''
        # 黑白名单
        file = self.tx_blackwrite.get()
        if (file):
            self.param['bwlisfile'] = file
            var = '--pkg-whitelist-file'
            if (self.blackwrite.get() == '黑名单'):
                var = '--pkg-blacklist-file'
            file = ' '.join([var, file])
            #self.text_log.insert(1, file)
            pkg = ''
        # 保存位置
        # 异常流
        savewhat = self.strvar_comp.get()
        if (savewhat == '保存至电脑'):
            savepath = self.log_dir
        else:
            savepath = '/sdcard/'

        sepererr = self.intvar_seperr.get()
        logname = 'amonkey.txt'
        errlog = 'amonkey_err.txt'
        if (sepererr):
            newsavepath = '1>%s 2>%s' % (savepath + logname, savepath + errlog)
        else:
            newsavepath = '>' + savepath + logname
        # if (savewhat == '保存至手机'):
        #     newsavepath = newsavepath + ' &'

        self.text_log.insert(tk.END, '开始运行monkey..')
        cmd = ' '.join([shell,'monkey', logv, seed, pkg, file, script, throttle, secur, crash, anr, selflize,
                        times, newsavepath])
        #去除空格
        saveflag = (savewhat == '保存至手机')
        if(saveflag):
            cmd = cmd + '"'
            cmd_lst = cmd.split(' ')
            for i in range(len(cmd_lst) - 1, -1, -1):
                if (cmd_lst[i] == 'monkey'):
                    cmd_lst[i] = '"monkey'
                elif (not cmd_lst[i]):
                    cmd_lst.pop(i)
        else:
            cmd_lst = cmd.split(' ')
            for i in range(len(cmd_lst) - 1, -1, -1):
                if (not cmd_lst[i]):
                    cmd_lst.pop(i)
        cmd = ' '.join(cmd_lst)
        return cmd

    def click_run(self):
        self.root.update_idletasks()
        if(not self.check_has_devices()):
            self.text_log.insert(tk.END, 'NO Devices!!  Please Connect 1 device.')
            return
        savelogcat = self.intvar_savelogcat.get()
        cmd = self.check_param()
        if (cmd):
            self.text_log.insert(tk.END, cmd)
            T2=threading.Thread(target=self.execute_monkey,args=(cmd,savelogcat,self.monkeycallback))
            T2.setDaemon(True)
            T2.start()
            self.root.update_idletasks()

    def reconnect(self):
        cmd = 'adb reconnect'
        T2 = threading.Thread(target=self.run_cmd, args=(cmd,))
        T2.start()
        T2.join()

    def run_cmd(self, cmd):
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stderr.read()

    def check_has_devices(self):
        NO_DEVICE_COUNT_LINE = 2
        cmd = 'adb devices'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        lines = proc.stdout.readlines()
        if (len(lines) <= NO_DEVICE_COUNT_LINE):
            return False
        else:
            return True

    def click_stop(self):
        self.text_log.delete(0, 10000)

    def btn_click(self):
        self.et_shebeihao.insert(tk.END, 'ok')
        output = subprocess.Popen('adb shell monkey')
        self.et_shebeihao.insert(tk.END, output.stdout.readlines())

    def monkeycallback(self):
        self.text_log.insert(tk.END, '结束monkey..')
        if(self.intvar_savelogcat.get()):
            self.p.terminate()

    def execute_monkey(self, command, savelogcat, monkeycallback):
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

        if (savelogcat):
            curtime = strftime('%F%H%M%S', localtime(time()))
            txt = ''.join([self.log_dir,'log', curtime, '.txt'])

            logcatcmd = 'adb logcat'
            logtxt = open(txt, 'w+')
            self.p = subprocess.Popen(logcatcmd, stdout=logtxt, stderr=subprocess.PIPE)
        result.stdout.readline()
        monkeycallback()

    def find_abnormal_keywd(self):
        abnormal_key =['NullPointerException','ArrayIndexOutBoundsException','beginning of crash','ANR','GC']
        search_file = self.search_log_file()

        if(search_file):
            file = self.log_dir + search_file
        else:
            self.text_log.insert(tk.END, self.log_dir+' have NO file to analyse!!')
            return
        self.text_log.insert(tk.END, '正在分析logcat...请稍等。')
        with open(file,encoding='utf-8') as f:
            s=set()
            for line in f.readlines():
                for key in abnormal_key:
                    if(key in line):
                        s.add(key)
        self.text_log.insert(tk.END, '分析完毕')
        if(len(s)>0):
            self.text_log.insert(tk.END, s)
        else:
            self.text_log.insert(tk.END, '初步判断无异常')

    def search_log_file(self):
        filelst=os.listdir(self.log_dir)
        for file in filelst:
            if(file.startswith('log')):
                return file

if __name__ == '__main__':
    MonkeyGUI().create_GUI()
