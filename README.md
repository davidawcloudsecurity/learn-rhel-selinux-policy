# learn-rhel-selinux-policy
How to create policy for amazon-ssm-agent

## Filter for unconfined services
```ruby
ps -eZ | grep unconfined_service_t
```
For each unconfined process identified, determine its executable and investigate its SELinux policy requirements.
```ruby
ps -p 785 -o comm,args
```
Check Current SELinux Context of the Executable
Use the ls -Z command to check the SELinux context of the executable.
```ruby
ls -Z /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent
```
## What is selinux
https://www.digitalocean.com/community/tutorials/an-introduction-to-selinux-on-centos-7-part-1-basic-concepts

https://github.com/aws/amazon-ssm-agent-selinux/blob/main/amazon_ssm_agent.sh

https://www.whitewinterwolf.com/posts/2017/09/08/selinux-cheatsheet/

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/selinux_users_and_administrators_guide/sect-security-enhanced_linux-working_with_selinux-selinux_contexts_labeling_files

https://subscription.packtpub.com/book/cloud-and-networking/9781783989669/1/ch01lvl1sec10/building-a-simple-selinux-module

https://access.redhat.com/articles/6999267

```ruby
yum install rpm-build
```
```ruby
yum install policycoreutils-devel policycoreutils policycoreutils-python selinux-policy selinux-policy-targeted libselinux-utils setroubleshoot-server setools setools-console mcstrans
```

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/using_selinux/writing-a-custom-selinux-policy_using-selinux

## Troubleshooting
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/selinux_users_and_administrators_guide/sect-security-enhanced_linux-troubleshooting-top_three_causes_of_problems
