# coding: utf-8
import os, sys, re
import config
from log_handler import Logger
from show_options import Show_Options


class Gen_EXE(object):
    def __init__(self):
        self.cmd = "msfvenom -f exe "
        self.work_dir = config.work_dir
        self.exe_dir = config.path_dict["exe_path"]
        self.log_dir = config.path_dict["log_path"]
        self.payload_info_dir = config.path_dict["payload_info_path"]
        self.sensitive_char = config.sensitive_char
        self.replace_str = config.replace_str
        self.re_pattern = re.compile(config.re_pattern)
        self.option_info = Show_Options()


        if not os.path.exists(self.exe_dir):
            os.mkdir(self.exe_dir)
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)
        if not os.path.exists(self.payload_info_dir):
            os.mkdir(self.payload_info_dir)

        self.encoder = [""]
        with open(config.path_dict["encoder"]) as pf:
            for line in pf.readlines():
                line = line.strip()
                if not line:
                    continue
                self.encoder.append(line)

        self.payload_x86 = []
        with open(config.path_dict["payload_x86"]) as pf:
            for line in pf.readlines():
                line = line.strip()
                if not line:
                    continue
                self.payload_x86.append(line)

        self.payload_x64 = []
        with open(config.path_dict["payload_x64"]) as pf:
            for line in pf.readlines():
                line = line.strip()
                if not line:
                    continue
                self.payload_x64.append(line)

        log_path = config.log
        with open(config.log, "w"):
            print "clear main log"
        self.logger = Logger(log_path)
        self.logger.debug("encoder count: %s" %len(self.encoder))
        self.logger.debug("x86 payload count: %s" %len(self.payload_x86))
        self.logger.debug("x64 payload count: %s" % len(self.payload_x64))


    def parse_log(self, filename):
        try:
            with open(filename) as pf:
                for line in pf.readlines():
                    res = re.search(self.re_pattern, line)
                    if res:
                        return res.group(1).strip()
            return None
        except Exception, e:
            return e.message

    def get_opt_string(self, payload):
        pl = payload.replace(self.sensitive_char, self.replace_str)
        pl_info_path = os.path.join(self.payload_info_dir, pl)
        print pl_info_path
        option_dict = self.option_info.parse_options(payload, pl_info_path)
        basic_option = option_dict["Options"]
        option_string = ""
        for opt in basic_option:
            if isinstance(opt, dict):
                key = opt.keys()[0]
                if opt[key] is None:
                    option_string = option_string + key + "=" + config.option_dict[key] + " "
        return option_string


    def generate_exe(self, payload, encoder, option_string):
        pl = payload.replace(self.sensitive_char, self.replace_str)
        if not os.path.exists(os.path.join(self.exe_dir, pl)):
            os.mkdir(os.path.join(self.exe_dir, pl))
        if not os.path.exists(os.path.join(self.log_dir, pl)):
            os.mkdir(os.path.join(self.log_dir, pl))
        exe_path = log_path = ""
        self.logger.info("generate exe for %s, encoder: %s, options: %s"%(payload, encoder, option_string))
        if not encoder:
            en = "raw"
            exe_path = os.path.join(self.exe_dir, pl, en)
            log_path = os.path.join(self.log_dir, pl, en)
            cmd = self.cmd + option_string + "-p %s -o %s 2>%s"%(payload, exe_path, log_path)
            self.logger.debug(cmd)
            os.system(cmd)
        else:
            en = encoder.replace(self.sensitive_char, self.replace_str)
            exe_path = os.path.join(self.exe_dir, pl, en)
            log_path = os.path.join(self.log_dir, pl, en)
            cmd = self.cmd + option_string + "-p %s -e %s -o %s 2>%s" % (payload, encoder, exe_path, log_path)
            self.logger.debug(cmd)
            os.system(cmd)
        if not os.path.exists(exe_path):
            self.logger.info("generate failed, error info: %s"%(self.parse_log(log_path)))


    def run(self):
        for payload in self.payload_x86:
            option_string = self.get_opt_string(payload)
            for encoder in self.encoder:
                self.generate_exe(payload, encoder, option_string)
                break

        for payload in self.payload_x64:
            option_string = self.get_opt_string(payload)
            for encoder in self.encoder:
                self.generate_exe(payload, encoder, option_string)
                break




g = Gen_EXE()
g.run()
