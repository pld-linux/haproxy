Summary:	haproxy - high-performance TCP/HTTP load balancer
Name:		haproxy
Version:	1.1.24
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://w.ods.org/tools/haproxy/%{name}-%{version}.tar.gz
# Source0-md5:	3ddd10a8bf6e415eaa32851c39c2b67c
Source1:	%{name}.cfg
Source2:	%{name}.init
URL:		http://w.ods.org/tools/haproxy/
BuildRequires:	pcre-devel
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HA-Proxy is a TCP/HTTP reverse proxy which is particularly suited for
high availability environments. Indeed, it can :
- route HTTP requests depending on statically assigned cookies ;
- spread the load among several servers while assuring server
  persistence through the use of HTTP cookies ;
- switch to backup servers in the event a main one fails ;
- accept connections to special ports dedicated to service monitoring
  ;
- stop accepting connections without breaking existing ones ;
- add/modify/delete HTTP headers both ways ;
- block requests matching a particular pattern ;

It needs very little resource. Its event-driven architecture allows it
to easily handle thousands of simultaneous connections on hundreds of
instances without risking the system's stability.

%prep
%setup -q

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/%{name},/etc/rc.d/init.d}

install haproxy $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f %{_var}/lock/subsys/%{name} ]; then
        /etc/rc.d/init.d/%{name} restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} daemon."
fi

%preun
if [ "$1" = "0" -a -f %{_var}/lock/subsys/%{name} ]; then
        /etc/rc.d/init.d/%{name} stop 1>&2
fi
/sbin/chkconfig --del %{name}

%files
%defattr(644,root,root,755)
%doc CHANGELOG examples/* doc/*
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
