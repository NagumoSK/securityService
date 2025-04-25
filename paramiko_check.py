import time

import paramiko

SUDO_PASSWORD = "114514\n"
SSH_PORT = 2222
ALLOW_IP = '172.16.199.0/24'


# paramiko检查密码策略（检查）
def check_pwd_policy(ip, usr, pwd) -> int:
    print("开始检查系统密码策略...")
    required_policy = "password requisite pam_cracklib.so dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1 minlen=8 enforce_for_root"
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    time.sleep(1)
    try:
        c.connect(hostname=ip, username=usr, password=pwd, port=22)
        time.sleep(1)
        stdin, stdout, stderr = c.exec_command('cat /etc/pam.d/common-password')
        time.sleep(1)
        output = stdout.read().decode()
        if required_policy in output:
            print("密码策略已配置")
            time.sleep(1)
            return 0
        else:
            print("密码策略未配置，开始添加策略")
            # add_policy_cmd = f"echo {SUDO_PASSWORD} | sudo -S sh -c 'echo {required_policy} >> /etc/pam.d/common-password'"
            add_policy_cmd = (
                f"echo '{SUDO_PASSWORD}' | sudo -S sh -c "
                f"\"echo '{required_policy}' >> /etc/pam.d/common-password\""
            )
            stdin, stdout, stderr = c.exec_command(add_policy_cmd)
            error = stderr.read().decode()
            stdin, stdout, stderr = c.exec_command('cat /etc/pam.d/common-password')
            output = stdout.read().decode()
            if required_policy in output:
                print(f"添加密码策略完毕：")
                return 1
            else:
                print(f"添加密码策略失败！", error)
                return 2

    except Exception as e:
        print("Paramiko SSH链接错误：", e)
        return 2
    finally:
        c.close()


# paramiko检查密码过期期限（直接覆盖）
def check_pwd_expiration_date(ip, usr, pwd):
    print("开始执行密码过期期限配置...")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    time.sleep(1)
    try:
        c.connect(hostname=ip, username=usr, password=pwd, port=22)
        time.sleep(1)

        cmds = [
            'sudo sed -i \'s/^PASS_MAX_DAYS\\s\\+[0-9]\\+/PASS_MAX_DAYS   180/\' /etc/login.defs\n',
            'sudo sed -i \'s/^PASS_MIN_DAYS\\s\\+[0-9]\\+/PASS_MIN_DAYS   30/\' /etc/login.defs\n',
            'sudo sed -i \'s/^PASS_WARN_AGE\\s\\+[0-9]\\+/PASS_WARN_AGE   14/\' /etc/login.defs\n'
        ]
        shell = c.invoke_shell()
        for i, cmd in enumerate(cmds, start=1):
            print(f"开始修改Command{i}：", cmd)
            time.sleep(1)
            shell.send(cmd)
            time.sleep(1)
            shell.send(SUDO_PASSWORD)
            time.sleep(2)
        shell.close()
    except Exception as e:
        print("Paramiko SSH链接错误：", e)
    finally:
        time.sleep(1)
        c.close()


# paramiko检查系统登录失败处理功能（检查）
def check_login_fail_policy(ip, usr, pwd) -> int:
    print("开始检查系统登录失败处理功能...")
    required_policy = "auth required pam_tally.so deny=10 unlock_time=300 even_deny_root root_unlock_time=300"

    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    time.sleep(1)
    try:
        c.connect(hostname=ip, username=usr, password=pwd, port=22)
        time.sleep(1)
        stdin, stdout, stderr = c.exec_command('cat /etc/pam.d/login')
        time.sleep(1)
        output = stdout.read().decode()
        if required_policy in output:
            print("系统登录失败策略已配置")
            time.sleep(1)
            return 0
        else:

            print("系统登录失败策略未配置，开始添加策略")
            add_policy_cmd = (
                f"echo '{SUDO_PASSWORD}' | sudo -S sh -c "
                f"\"echo '{required_policy}' >> /etc/pam.d/login\""
            )
            stdin, stdout, stderr = c.exec_command(add_policy_cmd)
            error = stderr.read().decode()

            stdin, stdout, stderr = c.exec_command('cat /etc/pam.d/login')
            output = stdout.read().decode()
            if required_policy in output:
                print(f"添加系统登录失败策略策略完毕：")
                return 1
            else:
                print(f"添加系统登录失败策略策略失败！", error)
                return 2

    except Exception as e:
        print("Paramiko SSH链接错误：", e)
        return 2
    finally:
        c.close()


# 强制修改SSH策略，重启需要手动进行
def check_ssh_remote_login(ip, usr, pwd):
    print("开始配置SSH策略...重启SSH需要手动进行！！！")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    time.sleep(1)
    try:
        c.connect(hostname=ip, username=usr, password=pwd, port=22)
        time.sleep(1)
        cmds = [
            f'sshd:{ALLOW_IP}:allow\n',
            'sudo sed -i \'s/^#\\?PermitRootLogin .*/PermitRootLogin no/\' /etc/ssh/sshd_config\n'
        ]
        shell = c.invoke_shell()
        time.sleep(1)
        f_out = ''
        for cmd in cmds:
            shell.send(cmd)
            time.sleep(2)
            shell.send(SUDO_PASSWORD)
            time.sleep(2)
            output = shell.recv(1024).decode()
            f_out += output
        shell.close()
        print(f_out)
    except Exception as e:
        print("Paramiko SSH链接错误：", e)
    finally:
        time.sleep(1)
        c.close()


# 强制添加SSH登录ip
def check_ssh_remote_ip(ip, usr, pwd) -> int:
    print("开始配置SSH登录IP...")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    time.sleep(1)
    try:
        c.connect(hostname=ip, username=usr, password=pwd, port=22)
        time.sleep(1)
        allow_ip_policy = f'sshd:{ALLOW_IP}:allow'
        deny_ip_policy = f'sshd:ALL'
        allow_ip_file = '/etc/hosts.allow'
        deny_ip_file = '/etc/hosts.deny'

        def add_policy_cmd(policy, file):
            return (
                f"echo '{SUDO_PASSWORD}' | sudo -S sh -c "
                f"\"echo '{policy}' >> {file}\""
            )

        c.exec_command(add_policy_cmd(allow_ip_policy, allow_ip_file))
        time.sleep(1)
        c.exec_command(add_policy_cmd(deny_ip_policy, deny_ip_file))
        stdin, stdout, stderr = c.exec_command('cat /etc/hosts.allow')
        time.sleep(1)
        if allow_ip_policy in stdout.read().decode():
            print("SSH ALLOW IP配置完成！")
        else:
            print("SSH ALLOW IP配置失败！！！", stderr.read().decode())
            return 2
        stdin, stdout, stderr = c.exec_command('cat /etc/hosts.deny')
        if deny_ip_policy in stdout.read().decode():
            print("SSH DENY IP配置完成！")
        else:
            print("SSH DENY IP配置失败！！！", stderr.read().decode())
            return 2
    except Exception as e:
        print("Paramiko SSH链接错误：", e)
    finally:
        time.sleep(1)
        c.close()


# 最简单粗暴的方法，没有考虑用户组，需要继续补充用户组
def check_exec_time(ip, usr, pwd):
    print("开始配置超时登录时间和umask...")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    time.sleep(1)
    try:
        c.connect(hostname=ip, username=usr, password=pwd, port=22)
        time.sleep(1)
        set_umask_tmout = """
        ( grep -qE '^\\s*umask\\s+[0-9]+' /etc/profile || echo 'umask 022' | sudo tee -a /etc/profile > /dev/null ) && \
        ( grep -qE '^\\s*TMOUT=' /etc/profile || echo 'TMOUT=300' | sudo tee -a /etc/profile > /dev/null )
        """
        stdin, stdout, stderr = c.exec_command(f"echo '{SUDO_PASSWORD}' | sudo -S bash -c \"{set_umask_tmout}\"")
        time.sleep(1)
        print(stdout.read().decode())
        if stderr:
            print(stderr.read().decode())
    except Exception as e:
        print("Paramiko SSH链接错误：", e)
    finally:
        time.sleep(1)
        c.close()
