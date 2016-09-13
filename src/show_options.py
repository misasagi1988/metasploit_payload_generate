# coding: utf-8
import os, sys, re
import config

class Show_Options(object):

    def get_options(self, payload, info_path):
        cmd = "msfvenom -p %s --payload-options >%s 2>&1" %(payload, info_path)
        os.system(cmd)

    def parse_options(self, payload, info_path):
        platform = re.compile("Platform: (.+)")
        arch = re.compile("Arch: (.+)")
        options = re.compile("^(\w+)\s+([^\s]+\s+)?yes")
        info_dict = {
            "Platform": "",
            "Arch": "",
            "Options": []
        }
        try:
            with open(info_path) as pf:
                for line in pf.readlines():
                    res = re.search(platform, line)
                    if res:
                        info_dict["Platform"] = res.group(1).strip()
                        continue
                    res = re.search(arch, line)
                    if res:
                        info_dict["Arch"] = res.group(1).strip()
                        continue
                    res = re.search(options, line)
                    if res:
                        info_dict["Options"].append({res.group(1).strip(): res.group(2).strip()}) if res.group(2) else \
                        info_dict["Options"].append({res.group(1).strip(): res.group(2)})
                        continue
            return info_dict
        except Exception, e:
            return None



if __name__ == "__main__":
    s = Show_Options()
    print s.parse_options("windows/meterpreter/bind_tcp", r"E:\SC\metasploit\mstasploit\payload_info\windows__meterpreter__bind_tcp")
    '''
    with open(config.path_dict["payload_x86"]) as pf:
        for line in pf.readlines():
            line = line.strip()
            if not line:
                continue
            print line
            info_path = os.path.join(config.path_dict["payload_info_path"],
                                     line.replace(config.sensitive_char, config.replace_str))
            print s.parse_options(line, info_path)
    with open(config.path_dict["payload_x64"]) as pf:
        for line in pf.readlines():
            line = line.strip()
            if not line:
                continue
            print line
            info_path = os.path.join(config.path_dict["payload_info_path"],
                                     line.replace(config.sensitive_char, config.replace_str))
            print s.parse_options(line, info_path)
    '''
