import time
import re
import paramiko

# SUDO_PASSWORD = "114514\n"
ALLOW_IP = '172.16.199.0/24'


# paramiko检查密码策略（检查）
def check_pwd_policy(ip, usr, pwd, sudo_pwd) -> int:
    print("Starting to check the system password policy...")
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
            print("Password policy had configured...")
            time.sleep(1)
            return 0
        else:
            print("Password policy is not configured, starting to add policy.")
            # add_policy_cmd = f"echo {SUDO_PASSWORD} | sudo -S sh -c 'echo {required_policy} >> /etc/pam.d/common-password'"
            add_policy_cmd = (
                f"echo '{sudo_pwd}' | sudo -S sh -c "
                f"\"echo '{required_policy}' >> /etc/pam.d/common-password\""
            )
            stdin, stdout, stderr = c.exec_command(add_policy_cmd)
            error = stderr.read().decode()
            stdin, stdout, stderr = c.exec_command('cat /etc/pam.d/common-password')
            output = stdout.read().decode()
            if required_policy in output:
                print("The password policy has been successfully added.")
                return 1
            else:
                print(f"Failed to add the password policy!!!", error)
                return 2

    except Exception as e:
        print("⚠️Paramiko SSH connection error: ", e)
        return 2
    finally:
        c.close()


# paramiko检查密码过期期限（直接覆盖）
def check_pwd_expiration_date(ip, usr, pwd, sudo_pwd):
    print("Starting to check the system password exec time....")
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
            shell.send(sudo_pwd)
            time.sleep(2)
        shell.close()
    except Exception as e:
        print("⚠️Paramiko SSH connection error: ", e)
    finally:
        time.sleep(1)
        c.close()


# paramiko检查系统登录失败处理功能（检查）
def check_login_fail_policy(ip, usr, pwd, sudo_pwd) -> int:
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
                f"echo '{sudo_pwd}' | sudo -S sh -c "
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
        print("⚠️Paramiko SSH connection error: ", e)
        return 2
    finally:
        c.close()


# 强制修改SSH策略，重启需要手动进行
def check_ssh_remote_login(ip, usr, pwd, sudo_pwd):
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
            shell.send(sudo_pwd)
            time.sleep(2)
            output = shell.recv(1024).decode()
            f_out += output
        shell.close()
        print(f_out)
    except Exception as e:
        print("⚠️Paramiko SSH connection error: ", e)
    finally:
        time.sleep(1)
        c.close()


# 强制添加SSH登录ip
def check_ssh_remote_ip(ip, usr, pwd, sudo_pwd) -> int:
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
                f"echo '{sudo_pwd}' | sudo -S sh -c "
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
        print("⚠️Paramiko SSH connection error: ", e)
    finally:
        time.sleep(1)
        c.close()


# 最简单粗暴的方法，没有考虑用户组，需要进行UID判断
def check_exec_time(ip, usr, pwd, sudo_pwd):
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
        stdin, stdout, stderr = c.exec_command(f"echo '{sudo_pwd}' | sudo -S bash -c \"{set_umask_tmout}\"")
        time.sleep(1)
        print(stdout.read().decode())
        if stderr:
            print(stderr.read().decode())
    except Exception as e:
        print("⚠️Paramiko SSH connection error: ", e)
    finally:
        time.sleep(1)
        c.close()


# 配置三权分立，目前没有考虑是否已经配置（主观行为，不好介入）
def check_user_group(ip, usr, pwd, sudo_pwd):
    print("开始配置三权分立...")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    time.sleep(1)
    try:
        c.connect(hostname=ip, username=usr, password=pwd, port=22)
        time.sleep(1)
        set_umask_tmout = """
            ( grep -qE '^.*:x:1001:' /etc/passwd || echo 'auditor:x:1001:1001::/home/auditor:/bin/bash' | sudo tee -a /etc/passwd > /dev/null ) && \
            ( grep -qE '^.*:x:1002:' /etc/passwd || echo 'security:x:1002:1002::/home/security:/bin/bash' | sudo tee -a /etc/passwd > /dev/null )
            """
        stdin, stdout, stderr = c.exec_command(f"echo '{sudo_pwd}' | sudo -S bash -c \"{set_umask_tmout}\"")
        time.sleep(1)
        print(stdout.read().decode())
        if stderr:
            print(stderr.read().decode())
    except Exception as e:
        print("⚠️Paramiko SSH connection error: ", e)
    finally:
        time.sleep(1)
        c.close()


def check_logrotate(ip, usr, pwd, sudo_pwd):
    print("开始配置日志保存期限...")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    time.sleep(1)
    try:
        c.connect(hostname=ip, username=usr, password=pwd, port=22)
        time.sleep(1)

        cmds = [
            "sed -i 's/^\\s*rotate\\s\\+[0-9]\\+/rotate 6/' /etc/logrotate.conf",
            "sed -i 's/^\\s*#\\s*keep\\s\\+[0-9]\\+\\s\\+weeks/# keep 6 weeks/' /etc/logrotate.conf"
        ]
        stdin, stdout, stderr = c.exec_command(f"echo '{sudo_pwd}' | sudo -S {cmds[0]}")
        time.sleep(1)
        print(stdout.read().decode())
        stdin, stdout, stderr = c.exec_command(f"echo '{sudo_pwd}' | sudo -S {cmds[1]}")
        time.sleep(1)
        print(stdout.read().decode())
        if stderr:
            print(stderr.read().decode())
    except Exception as e:
        print("⚠️Paramiko SSH connection error: ", e)
    finally:
        time.sleep(1)
        c.close()


def check_system_port(ip, usr, pwd, sudo_pwd):
    print("Starting to check the system port....")
    ports_to_kill = [21, 23, 80]
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    time.sleep(1)
    try:
        c.connect(hostname=ip, username=usr, password=pwd, port=22)
        time.sleep(1)
        cmd = f"echo {sudo_pwd} | sudo -S netstat -tunlp"
        stdin, stdout, stderr = c.exec_command(cmd)
        time.sleep(1)

        netstat_output = stdout.read().decode()

        # 解释正则：^表示从每一行最开头开始匹配。(tcp|tcp6)匹配Proto。\s+匹配一个或多个空格。\d+匹配第二列Recv-Q数字。[\[\]:.\d]+:(\d+)捕获Local Address:port。
        # .*捕获Foreign Address。LISTEN捕获State中的固定文本。(\d+)捕获PID。re.MULTILINE让^和$分别匹配每一行的开头和结尾，而不是整个字符串的一次开头结尾。
        pattern = re.compile(r'^(tcp|tcp6|udp|udp6)\s+\d+\s+\d+\s+[\[\]:.\d]+:(\d+)\s+.*LISTEN\s+(\d+)/', re.MULTILINE)

        # 保存PID
        pids_to_kill = set()

        print(netstat_output)

        for match in pattern.finditer(netstat_output):
            protocol, port, pid = match.groups()
            port = int(port)
            if port in ports_to_kill:
                print(f"检测到{protocol}协议，端口 {port}，对应PID {pid}")
                pids_to_kill.add(pid)

        for pid in pids_to_kill:
            kill_cmd = f"echo {sudo_pwd} | sudo -S kill {pid}"
            stdin, stdout, stderr = c.exec_command(kill_cmd)
            time.sleep(1)
            if stderr:
                print("kill port error:", stderr.read().decode())

        stdin, stdout, stderr = c.exec_command(cmd)
        print(stdout.read().decode())

    except Exception as e:
        print("⚠️Paramiko SSH connection error: ", e)
    finally:
        time.sleep(1)
        c.close()
