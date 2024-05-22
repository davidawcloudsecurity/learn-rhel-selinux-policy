# learn-rhel-selinux-policy
How to create policy for amazon-ssm-agent

## Filter for unconfined services
```ruby
ps -eZ | grep unconfined_service_t
```
For each unconfined process identified, determine its executable `path` and investigate its SELinux policy requirements.
```ruby
ps -p 785 -o comm,args
```
If cannot find the path
```ruby
ls -l /proc/785/exe
readlink -f /proc/785/exe
lsof -p 785 | grep txt
```
Best to check everything associate with the service/application/process

Check Current SELinux Context of the Executable

Use the ls -Z command to check the SELinux context of the executable.
```ruby
ls -Z /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent
```
List all file context rules:
```ruby
semanage fcontext -l
semanage fcontext -l | grep /path/to/file
semanage fcontext -l | grep -i splunk
```
1. Create policy
```ruby
sepolicy generate --init <path_to_my_app_binary>
```
Proceed to execute the sh file

Check if the policy is created and registered in semanage
```ruby
semanage fcontext -l | grep -i amazon
```
Check if audit denies any services
```ruby
ausearch -m AVC,USER_AVC -ts recent
```
Definition of AVC & USER_AVC
```ruby
type=AVC msg=audit(1716348575.824:10653): avc:  denied  { map } for  pid=11245 comm="ausearch" path="/var/log/audit/audit.log.25" dev="xvdu" ino=138 scontext=system_u:system_r:amazon_ssm_agent_t:s0 tcontext=system_u:object_r:auditd_log_t:s0 tclass=file permissive=1
type=USER_AVC msg=audit(1716348575.824:10654): user_avc:  denied  { execute } for  pid=11245 comm="example_app" path="/path/to/resource" scontext=unconfined_u:unconfined_r:unconfined_t:s0 tcontext=system_u:object_r:user_home_t:s0 tclass=file permissive=0
```
Apply semanage and restorcon to the label created from #1
```
semanage fcontext -a -t amazon_ssm_agent_exec_t '/usr/bin/amazon-ssm-agent'
or
semanage fcontext -a -t amazon_ssm_agent_exec_t '/usr/bin/amazon-ssm-agent(/.*)?'
restorecon -v /usr/bin/amazon-ssm-agent
```
## What is selinux
https://www.digitalocean.com/community/tutorials/an-introduction-to-selinux-on-centos-7-part-1-basic-concepts

https://github.com/aws/amazon-ssm-agent-selinux/blob/main/amazon_ssm_agent.sh

https://www.whitewinterwolf.com/posts/2017/09/08/selinux-cheatsheet/

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/selinux_users_and_administrators_guide/sect-security-enhanced_linux-working_with_selinux-selinux_contexts_labeling_files

https://subscription.packtpub.com/book/cloud-and-networking/9781783989669/1/ch01lvl1sec10/building-a-simple-selinux-module

https://access.redhat.com/articles/6999267

```ruby
yum install rpm-build policycoreutils-devel selinux-policy -y
```
```ruby
yum install policycoreutils-devel policycoreutils policycoreutils-python selinux-policy selinux-policy-targeted libselinux-utils setroubleshoot-server setools setools-console mcstrans
```

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/using_selinux/writing-a-custom-selinux-policy_using-selinux

## Troubleshooting
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/selinux_users_and_administrators_guide/sect-security-enhanced_linux-troubleshooting-top_three_causes_of_problems

```ruby
ausearch -m avc -ts recent
```

https://chatgpt.com/share/f12a8beb-5d21-4178-be67-32b791fa9b4c
