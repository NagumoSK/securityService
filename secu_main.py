import subprocess
import time
import pyautogui
import pytesseract
import tkinter as tk
from cmdGUI_config import config_password_expiration_date, config_password_policy, config_ssh_remote_ip, \
    config_exec_time, config_user_group
from cmdGUI_config import get_kernel
from cmdGUI_config import config_login_fail_policy
from paramiko_check import check_ssh_remote_login, check_ssh_remote_ip, check_exec_time, check_user_group, \
    check_logrotate

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 替换为你自己的服务器信息
HOST = "172.16.199.127"
USER = "nagumo"
PASSWORD = "114514"
SUDO_PWD = "114514"

if __name__ == "__main__":

    # HOST = input("強化するホストのIPを入力してください。")
    # PORT = input("SSH接続ポートを入力してください。")
    # USER = input("ユーザー名を入力してください")
    # PASSWORD = input("パスワードを入力してください")
    # SUDO_PWD = input("SUDOパスワードを入力してください。")

    # 1. 打开 CMD 窗口，切换输入法并且全屏
    subprocess.Popen("start cmd", shell=True)
    time.sleep(2)
    pyautogui.hotkey('alt', 'enter')
    time.sleep(1)

    # 输入 SSH 命令（注意：这种方式不能输入密码，可以改用paramiko）
    pyautogui.typewrite(f'ssh {USER}@{HOST}\n', interval=0.05)
    time.sleep(1)

    # 输入密码（如果提示了）
    pyautogui.typewrite(PASSWORD + '\n', interval=0.05)
    time.sleep(1)

    # 进入sudo
    pyautogui.typewrite(f'sudo -i\n', interval=0.05)
    time.sleep(1)
    pyautogui.typewrite(PASSWORD + '\n', interval=0.05)
    time.sleep(1)

    ###########################
    # 实际运行需要注意，修改SSH要放在最后进行。
    # get_kernel()
    # config_password_policy(HOST, USER, PASSWORD) # 密码策略
    # config_password_expiration_date(HOST, USER, PASSWORD) # 密码过期期限
    # config_login_fail_policy(HOST, USER, PASSWORD) # 登录失败策略
    # check_exec_time(HOST, USER, PASSWORD)  # SSH IP 策略
    # check_exec_time(HOST, USER, PASSWORD)
    # check_user_group(HOST, USER, PASSWORD)
    # config_exec_time(HOST, USER, PASSWORD)
    # config_user_group(HOST, USER, PASSWORD)
    check_logrotate(HOST, USER, PASSWORD)
    time.sleep(1)
    ###########################

    # 关闭窗口，
    # pyautogui.typewrite('exit\n', interval=0.05)
    # pyautogui.typewrite('exit\n', interval=0.05)
    # pyautogui.typewrite('exit\n', interval=0.05)
