Name:           amazon_ssm_agent_selinux
Version:        1.0
Release:        1%{?dist}
Summary:        SELinux policy for Amazon SSM Agent

Group:          System Environment/Base
License:        GPL
URL:            https://example.com/amazon_ssm_agent
Source0:        amazon_ssm_agent.te
Source1:        amazon_ssm_agent.fc

BuildArch:      noarch
BuildRequires:  selinux-policy-devel
Requires:       selinux-policy

%description
This package contains SELinux policy for Amazon SSM Agent.

%prep
%setup -q

%build
make -f /usr/share/selinux/devel/Makefile

%install
mkdir -p %{buildroot}/usr/share/selinux/packages
install -m 644 amazon_ssm_agent.pp %{buildroot}/usr/share/selinux/packages

%files
/usr/share/selinux/packages/amazon_ssm_agent.pp

%post
/sbin/semodule -i /usr/share/selinux/packages/amazon_ssm_agent.pp

%preun
/sbin/semodule -r amazon_ssm_agent

%changelog
* Tue May 14 2024 Your Name <you@example.com> - 1.0-1
- Initial package
