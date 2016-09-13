# coding: utf-8
import os

work_dir = os.path.dirname(os.path.abspath("."))

path_dict = {
    "log_path": os.path.join(work_dir, "log"),
    "exe_path": os.path.join(work_dir, "exe"),
    "payload_info_path": os.path.join(work_dir, "payload_info"),
    "encoder": os.path.join(work_dir, "encoders"),
    "payload_x86": os.path.join(work_dir, "payloads"),
    "payload_x64": os.path.join(work_dir, "payloads_x64")
}

log = os.path.join(work_dir, "main.log")

re_pattern = "Error:(.+)"

sensitive_char = "/"
replace_str = "__"

option_dict = {
"LHOST": "192.168.56.101",
"DNSZONE": "192.168.56.101",
"CMD": "cmd",
"DLL": "calc.exe",
"PEXEC": "calc.exe",
"AHOST": "192.168.56.101",
"KHOST": "192.168.56.101"
}

