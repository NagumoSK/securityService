import os
import sys
import time
from datetime import datetime
import pyautogui
import paramiko_check

save_folder = r'E:\Python_screenshot'
if not os.path.exists(save_folder):
    os.makedirs(save_folder)


def get_kernel():
    # 输入命令获取内核版本
    pyautogui.typewrite('uname -r\n', interval=0.05)
    time.sleep(2)

    # 截图保存到E:\Python_screenshot
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(save_folder, f"linux_kernel_version{current_time}.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    print(f"已截图并保存至：{screenshot_path}")


# 配置密码策略
def config_password_policy(ip, usr, pwd):
    pyautogui.typewrite('clear\n', interval=0.05)
    pyautogui.typewrite('cat /etc/pam.d/common-password\n', interval=0.05)
    time.sleep(2)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(save_folder, f"密码策略{current_time}.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    print(f"已截图并保存至：{screenshot_path}")

    # 通过paramiko判断是否需要加固
    res = paramiko_check.check_pwd_policy(ip, usr, pwd)

    if res == 0:
        print(f"无需加固")
    elif res == 1:
        # 加固完成，再截图一次
        pyautogui.typewrite('clear\n', interval=0.05)
        pyautogui.typewrite('cat /etc/pam.d/common-password\n', interval=0.05)
        time.sleep(2)

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join(save_folder, f"密码策略(加固){current_time}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        print("添加密码策略成功！已经完成截图")
    elif res == 2:
        print("添加密码策略出现问题，check_pwd_policy()出现错误")


# 配置密码过期期限
def config_password_expiration_date(ip, usr, pwd):
    pyautogui.typewrite('clear\n', interval=0.05)
    pyautogui.typewrite('more /etc/login.defs\n', interval=0.05)
    pyautogui.hotkey('space')
    time.sleep(1)
    pyautogui.hotkey('space')
    time.sleep(1)
    pyautogui.hotkey('space')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(save_folder, f"密码过期期限{current_time}.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    print(f"已截图并保存至：{screenshot_path}")

    paramiko_check.check_pwd_expiration_date(ip, usr, pwd)

    pyautogui.typewrite('clear\n', interval=0.05)
    pyautogui.typewrite('more /etc/login.defs\n', interval=0.05)
    pyautogui.hotkey('space')
    time.sleep(1)
    pyautogui.hotkey('space')
    time.sleep(1)
    pyautogui.hotkey('space')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(save_folder, f"密码过期期限(加固){current_time}.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    print(f"已截图并保存至：{screenshot_path}")


# 配置系统登录失败策略
def config_login_fail_policy(ip, usr, pwd):
    pyautogui.typewrite('clear\n', interval=0.05)
    pyautogui.typewrite('cat /etc/pam.d/login\n', interval=0.05)
    time.sleep(2)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(save_folder, f"系统登录失败策略{current_time}.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    print(f"已截图并保存至：{screenshot_path}")

    # 通过paramiko判断是否需要加固
    res = paramiko_check.check_login_fail_policy(ip, usr, pwd)

    if res == 0:
        print(f"无需加固")
    elif res == 1:
        # 加固完成，再截图一次
        pyautogui.typewrite('clear\n', interval=0.05)
        pyautogui.typewrite('cat /etc/pam.d/login\n', interval=0.05)
        time.sleep(2)

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join(save_folder, f"系统登录失败策略(加固){current_time}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        print("添加系统登录失败策略成功！已经完成截图")
    elif res == 2:
        print("添加系统登录失败策略出现问题，check_login_fail_policy()出现错误")
        sys.exit(1)


def config_ssh_remote_login(ip, usr, pwd):
    pyautogui.typewrite('clear\n', interval=0.05)
    pyautogui.typewrite('more /etc/ssh/sshd_config\n', interval=0.05)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'c')
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(save_folder, f"限制root使用ssh登录{current_time}.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    print(f"已截图并保存至：{screenshot_path}")

    paramiko_check.check_ssh_remote_login(ip, usr, pwd)

    pyautogui.typewrite('clear\n', interval=0.05)
    pyautogui.typewrite('more /etc/ssh/sshd_config\n', interval=0.05)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'c')
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(save_folder, f"限制root使用ssh登录(加固){current_time}.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    print(f"已截图并保存至：{screenshot_path}")


def config_ssh_remote_ip(ip, usr, pwd):
    pyautogui.typewrite('clear\n', interval=0.05)
    pyautogui.typewrite('more /etc/hosts.allow\n', interval=0.05)
    time.sleep(1)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(save_folder, f"限制root登录ip_allow{current_time}.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    print(f"已截图并保存至：{screenshot_path}")

    pyautogui.typewrite('clear\n', interval=0.05)
    pyautogui.typewrite('more /etc/hosts.deny\n', interval=0.05)
    time.sleep(1)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(save_folder, f"限制root登录ip_deny{current_time}.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    print(f"已截图并保存至：{screenshot_path}")

    res = paramiko_check.check_ssh_remote_ip(ip, usr, pwd)

    if res != 2:
        print("SSH IP加固成功，开始截图")
        pyautogui.typewrite('clear\n', interval=0.05)
        pyautogui.typewrite('more /etc/hosts.allow\n', interval=0.05)
        time.sleep(1)
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join(save_folder, f"限制root登录ip_allow(加固){current_time}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        print(f"已截图并保存至：{screenshot_path}")

        pyautogui.typewrite('clear\n', interval=0.05)
        pyautogui.typewrite('more /etc/hosts.deny\n', interval=0.05)
        time.sleep(1)
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join(save_folder, f"限制root登录ip_allow(加固){current_time}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        print(f"已截图并保存至：{screenshot_path}")
    else:
        print("SSH IP加固失败!")
        sys.exit(1)


def config_exec_time(ip, usr, pwd):
    pyautogui.typewrite('clear\n', interval=0.05)
    pyautogui.typewrite('more /etc/profile\n', interval=0.05)
    time.sleep(1)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(save_folder, f"系统超时时间{current_time}.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    print(f"已截图并保存至：{screenshot_path}")

    check_exec_time(ip, usr, pwd)







