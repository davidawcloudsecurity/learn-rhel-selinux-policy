# learn-rhel-selinux-policy
How to create policy for amazon-ssm-agent

## Requirements
```ruby
yum install rpm-build policycoreutils-devel selinux-policy -y
rm -rf /etc/yum.repos.d/*
```
Ctrl r to reveal previous type commands
```ruby
(reverse-i-search)`lsof': lsof -p 1854 | grep txt
```
! to search and paste previous run commands
```ruby
history | grep
528  semanage fcontext -l | grep cloudwatch
!528
```

## Filter for unconfined services
```ruby
ps -eZ | grep unconfined_service_t
```
For each unconfined process identified, determine its executable `path` and investigate its SELinux policy requirements.
```ruby
ps -eZ | grep unconfined_service_t
system_u:system_r:unconfined_service_t:s0 775 ?  00:00:00 amazon-cloudwat
```
If cannot find the path
```ruby
ps -p 775 -o comm,args
ls -l /proc/775/exe
readlink -f /proc/775/exe
lsof -p 775 | grep txt
```
```ruby
amazon-cl 775 cwagent  txt       REG              202,4 113890632  8160 /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent
```
Best to check everything associate with the service/application/process
```ruby
find / -name amazon-cloudwatch-agent
```
Use the ls -Z command to check the SELinux context of the executable.
```ruby
ls -Z /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent
system_u:object_r:bin_t:s0 /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent
```
Create policy
```ruby
sepolicy generate --init /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent
nm: /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent: no symbols
Created the following files:
/root/amazon_cloudwatch_agent.te # Type Enforcement file
/root/amazon_cloudwatch_agent.if # Interface file
/root/amazon_cloudwatch_agent.fc # File Contexts file
/root/amazon_cloudwatch_agent_selinux.spec # Spec file
/root/amazon_cloudwatch_agent.sh # Setup Script
```
Proceed to execute the sh file
```ruby
./amazon_cloudwatch_agent.sh
Building and Loading Policy
+ make -f /usr/share/selinux/devel/Makefile amazon_cloudwatch_agent.pp
Compiling targeted amazon_cloudwatch_agent module
Creating targeted amazon_cloudwatch_agent.pp policy package
rm tmp/amazon_cloudwatch_agent.mod.fc tmp/amazon_cloudwatch_agent.mod
+ /usr/sbin/semodule -i amazon_cloudwatch_agent.pp
+ sepolicy manpage -p . -d amazon_cloudwatch_agent_t
./amazon_cloudwatch_agent_selinux.8
+ /sbin/restorecon -F -R -v /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent
++ pwd
+ pwd=/root
+ rpmbuild --define '_sourcedir /root' --define '_specdir /root' --define '_builddir /root' --define '_srcrpmdir /root' --define '_rpmdir /root' --define '_buildrootdir /root/.build' -ba amazon_cloudwatch_agent_selinux.spec
setting SOURCE_DATE_EPOCH=1716336000
Executing(%install): /bin/sh -e /var/tmp/rpm-tmp.jcIDjp
+ umask 022
+ cd /root
+ '[' /root/.build/amazon_cloudwatch_agent_selinux-1.0-1.el9.x86_64 '!=' / ']'
+ rm -rf /root/.build/amazon_cloudwatch_agent_selinux-1.0-1.el9.x86_64
++ dirname /root/.build/amazon_cloudwatch_agent_selinux-1.0-1.el9.x86_64
+ mkdir -p /root/.build
+ mkdir /root/.build/amazon_cloudwatch_agent_selinux-1.0-1.el9.x86_64
+ install -d /root/.build/amazon_cloudwatch_agent_selinux-1.0-1.el9.x86_64/usr/share/selinux/packages
+ install -m 644 /root/amazon_cloudwatch_agent.pp /root/.build/amazon_cloudwatch_agent_selinux-1.0-1.el9.x86_64/usr/share/selinux/packages
+ install -d /root/.build/amazon_cloudwatch_agent_selinux-1.0-1.el9.x86_64/usr/share/selinux/devel/include/contrib
+ install -m 644 /root/amazon_cloudwatch_agent.if /root/.build/amazon_cloudwatch_agent_selinux-1.0-1.el9.x86_64/usr/share/selinux/devel/include/contrib/
+ install -d /root/.build/amazon_cloudwatch_agent_selinux-1.0-1.el9.x86_64/usr/share/man/man8/
+ install -m 644 /root/amazon_cloudwatch_agent_selinux.8 /root/.build/amazon_cloudwatch_agent_selinux-1.0-1.el9.x86_64/usr/share/man/man8/amazon_cloudwatch_agent_selinux.8
+ install -d /root/.build/amazon_cloudwatch_agent_selinux-1.0-1.el9.x86_64/etc/selinux/targeted/contexts/users/
+ /usr/lib/rpm/check-buildroot
+ /usr/lib/rpm/redhat/brp-ldconfig
+ /usr/lib/rpm/brp-compress
+ /usr/lib/rpm/brp-strip /usr/bin/strip
+ /usr/lib/rpm/brp-strip-comment-note /usr/bin/strip /usr/bin/objdump
+ /usr/lib/rpm/redhat/brp-strip-lto /usr/bin/strip
+ /usr/lib/rpm/brp-strip-static-archive /usr/bin/strip
+ /usr/lib/rpm/redhat/brp-python-bytecompile '' 1 0
+ /usr/lib/rpm/brp-python-hardlink
+ /usr/lib/rpm/redhat/brp-mangle-shebangs
Processing files: amazon_cloudwatch_agent_selinux-1.0-1.el9.noarch
Provides: amazon_cloudwatch_agent_selinux = 1.0-1.el9
Requires(interp): /bin/sh /bin/sh
Requires(rpmlib): rpmlib(CompressedFileNames) <= 3.0.4-1 rpmlib(FileDigests) <= 4.6.0-1 rpmlib(PayloadFilesHavePrefix) <= 4.0-1
Requires(post): /bin/sh policycoreutils-python-utils selinux-policy-base >= 38.1.35-2
Requires(postun): /bin/sh policycoreutils-python-utils
Checking for unpackaged file(s): /usr/lib/rpm/check-files /root/.build/amazon_cloudwatch_agent_selinux-1.0-1.el9.x86_64
Wrote: /root/amazon_cloudwatch_agent_selinux-1.0-1.el9.src.rpm
Wrote: /root/noarch/amazon_cloudwatch_agent_selinux-1.0-1.el9.noarch.rpm
Executing(%clean): /bin/sh -e /var/tmp/rpm-tmp.KTvDE5
+ umask 022
+ cd /root
+ /usr/bin/rm -rf /root/.build/amazon_cloudwatch_agent_selinux-1.0-1.el9.x86_64
+ RPM_EC=0
++ jobs -p
+ exit 0
```
## 1. List all file context rules:
```ruby
semanage fcontext -l | grep /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent
semanage fcontext -l | grep -i amazon_cloudwatch_agent
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent regular file       system_u:object_r:amazon_cloudwatch_agent_exec_t:s0
```
Relabel the directory to the policy
```ruby
semanage fcontext -a -t amazon_cloudwatch_agent_exec_t '/opt/aws/amazon-cloudwatch-agent(/.*)?'
restorecon -Rv /opt/aws/amazon-cloudwatch-agent
```
Relabel binary file to the policy
```ruby
semanage fcontext -a -t amazon_cloudwatch_agent_exec_t /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent
File context for /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent already defined, modifying instead
restorecon -Rv /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent
```
Restart service/process/application
```ruby
systemctl status | grep cloudwatch
           │ ├─amazon-cloudwatch-agent.service
           │ │ └─4035 /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent -config /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.toml -envconfig /opt/aws/amazon-cloudwatch-agent/etc/env-config.json -otelconfig /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.yaml -pidfile /opt/aws/amazon-cloudwatch-agent/var/amazon-cloudwatch-agent.pid
               │ └─4055 grep --color=auto cloudwatch
```
```ruby
systemctl stop amazon-cloudwatch-agent; systemctl start amazon-cloudwatch-agent; systemctl status amazon-cloudwatch-agent
```
List policy rules for a system service
```ruby
sesearch -A -s amazon_cloudwatch_agent_t -c service
```
Check if audit denies any services
```ruby
ausearch -c amazon-cloud -ts recent | grep denied
ausearch -ts recent | grep amazon-cloudwatch-agent | grep denied
```
Definition of AVC & USER_AVC
```ruby
type=AVC msg=audit(1716348575.824:10653): avc:  denied  { map } for  pid=11245 comm="ausearch" path="/var/log/audit/audit.log.25" dev="xvdu" ino=138 scontext=system_u:system_r:amazon_ssm_agent_t:s0 tcontext=system_u:object_r:auditd_log_t:s0 tclass=file permissive=1
type=USER_AVC msg=audit(1716348575.824:10654): user_avc:  denied  { execute } for  pid=11245 comm="example_app" path="/path/to/resource" scontext=unconfined_u:unconfined_r:unconfined_t:s0 tcontext=system_u:object_r:user_home_t:s0 tclass=file permissive=0
```
Apply semanage and restorcon to the label created from #1
```ruby
semanage fcontext -a -t amazon_ssm_agent_exec_t '/usr/bin/amazon-ssm-agent'
or
semanage fcontext -a -t amazon_ssm_agent_exec_t '/usr/bin/amazon-ssm-agent(/.*)?'
restorecon -v /usr/bin/amazon-ssm-agent
```
Reboot and repeat the above process with the new pp if service/process/application gets denied in /var/log/audit/audit.log
```ruby
ausearch -ts recent | grep "amazon-ssm-agent" | grep denied | audit2allow -M amazon-ssm-agent-custom
grep amazon-ssm-agent /var/log/audit/audit* | audit2allow -M amazon-ssmagent-custom
cat /var/log/messages | grep amazon-ssm-agent
```
```ruby
yum install policycoreutils-devel policycoreutils policycoreutils-python selinux-policy selinux-policy-targeted libselinux-utils setroubleshoot-server setools setools-console mcstrans
1. policycoreutils (provides utilities for managing SELinux)
2. policycoreutils-python (provides utilities for managing SELinux)
3. selinux-policy (provides SELinux reference policy)
4. selinux-policy-targeted (provides SELinux targeted policy)
5. libselinux-utils (provides some tools for managing SELinux)
6. setroubleshoot-server (provides tools for deciphering audit log messages)
7. setools (provides tools for audit log monitoring, querying policy, and file context management)
8. setools-console (provides tools for audit log monitoring, querying policy, and file context management)
9. mcstrans (tools to translate different levels to easy-to-understand format)
```

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/using_selinux/writing-a-custom-selinux-policy_using-selinux
## Manual execution of creating, applying selinux policy
```ruby
ausearch -m avc -ts recent | grep <service/process> | audit2allow -M <service/process>_custom
semodule -i <service/process>_custom.pp
```
## Troubleshooting
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/selinux_users_and_administrators_guide/sect-security-enhanced_linux-troubleshooting-top_three_causes_of_problems

## Create a Custom SELinux Policy Module
Create a new policy file named amazon-ssm-agent.te with the following content

This policy allows processes in the amazon_ssm_agent_t domain to read and open files labeled with the var_log_t type.
```ruby
module amazon-ssm-agent 1.0;

require {
    type var_log_t;
    type amazon_ssm_agent_t;
    class file { read open };
}
```
Compile the policy module and load it into the SELinux policy store:
```ruby
checkmodule -M -m -o amazon-ssm-agent.mod amazon-ssm-agent.te
semodule_package -o amazon-ssm-agent.pp -m amazon-ssm-agent.mod
sudo semodule -i amazon-ssm-agent.pp
```
You can verify that the policy is loaded correctly by listing the SELinux policy modules
```ruby
semodule -l | grep amazon-ssm-agent
```
## Remove the Custom SELinux Policy Module:
```ruby
sudo semodule -r amazon-ssm-agent_custom
sudo rm -rf /var/lib/selinux/targeted/tmp/modules/400/amazon-ssm-agent_custom
semodule -l | grep amazon-ssm-agent_custom
```
## Allow service/application/process to access directories / files
https://community.splunk.com/t5/Security/Is-there-a-recommended-way-of-giving-the-Splunk-TA-sufficient/m-p/76196
```ruby
To set acl to a directory recursively:

setfacl -R -m u:splunk:r /var/log
getfacl -R /var/log

To set acl for individual files:

setfacl -m u:splunk:r /var/log/messages
```
```ruby
# Add CW Agent to adm group and grant access to read logs
sudo adduser foobar www-data
usermod -G root cwagent
usermod -a -G adm cwagent
setfacl -d -m g:adm:r-x /var/log
setfacl -R -d -m g:adm:r-- /var/log/*
setfacl -m g:adm:r-x /var/log
setfacl -R -m g:adm:r-- /var/log/*
```
https://www.hostingadvice.com/how-to/linux-add-user-to-group/
```ruby
ausearch -m avc -ts recent
journalctl -xe
cat /var/log/audit/audit.log | grep AVC
```

## How to use journalctl
Resource - https://www.digitalocean.com/community/tutorials/how-to-use-journalctl-to-view-and-manipulate-systemd-logs
```ruby
journalctl -f
journalctl -n 20
journalctl --no-pager
journalctl -a
journalctl -p err -b
journalctl _PID=8088
journalctl -u nginx.service
```
## How to update openssh using centos for rhel
Resource - https://medium.com/@eren.c.uysal/openssh-upgrade-process-to-9-6p1-4d71ca4cd424
```ruby
yum install gcc
yum install zlib-devel
yum install openssl-devel
ssh -V
curl -O https://cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-9.6p1.tar.gz
tar -zxvf openssh-9.6p1.tar.gz
cd openssh-9.6p1
./configure
make
sudo make install
reboot
ssh -V
```
## What is selinux
https://www.digitalocean.com/community/tutorials/an-introduction-to-selinux-on-centos-7-part-1-basic-concepts

https://github.com/aws/amazon-ssm-agent-selinux/blob/main/amazon_ssm_agent.sh

https://www.whitewinterwolf.com/posts/2017/09/08/selinux-cheatsheet/

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/selinux_users_and_administrators_guide/sect-security-enhanced_linux-working_with_selinux-selinux_contexts_labeling_files

https://subscription.packtpub.com/book/cloud-and-networking/9781783989669/1/ch01lvl1sec10/building-a-simple-selinux-module

https://access.redhat.com/articles/6999267

https://chatgpt.com/share/f12a8beb-5d21-4178-be67-32b791fa9b4c

https://www.techtarget.com/searchdatacenter/tutorial/How-to-write-an-SELinux-policy
