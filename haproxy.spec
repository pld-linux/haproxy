Summary:	haproxy - high-performance TCP/HTTP load balancer
Summary(pl):	haproxy - wysoko wydajny load balancer TCP/HTTP
Name:		haproxy
Version:	1.2.15
Release:	0.1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://haproxy.1wt.eu/download/1.2/src/%{name}-%{version}.tar.gz
# Source0-md5:	7461a3deeda099a6ee190f99e9763fea
#Source1:	%{name}.cfg
Source2:	%{name}.init
URL:		http://haproxy.1wt.eu/
BuildRequires:	pcre-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HA-Proxy is a TCP/HTTP reverse proxy which is particularly suited for
high availability environments. Indeed, it can:
- route HTTP requests depending on statically assigned cookies;
- spread the load among several servers while assuring server
  persistence through the use of HTTP cookies;
- switch to backup servers in the event a main one fails;
- accept connections to special ports dedicated to service monitoring;
- stop accepting connections without breaking existing ones;
- add/modify/delete HTTP headers both ways;
- block requests matching a particular pattern.

It needs very little resource. Its event-driven architecture allows it
to easily handle thousands of simultaneous connections on hundreds of
instances without risking the system's stability.

%description -l pl
HA-Proxy to odwrotne proxy TCP/HTTP przeznaczone w szczególno¶ci dla
¶rodowisk o wysokiej dostêpno¶ci. W rzeczywisto¶ci mo¿e:
- przekazywaæ ¿±dania HTTP w zale¿no¶ci od statycznie przypisanych
  ciasteczek;
- rozdzielaæ obci±¿enie miêdzy ró¿ne serwery zapewniaj±c ci±g³o¶æ
  ³±czno¶ci z serwerem poprzez u¿ycie ciasteczek HTTP;
- prze³±czaæ na serwery zapasowe w przypadku, gdy g³ówny zawiedzie;
- przyjmowaæ po³±czenia na specjalne porty przeznaczone do
  monitorowania us³ug;
- zaprzestaæ przyjmowania po³±czeñ bez zrywania istniej±cych;
- dodawaæ/modyfikowaæ/usuwaæ nag³ówki HTTP w obie strony;
- blokowaæ ¿±dania pasuj±ce do okre¶lonego wzorca.

Wymaga bardzo niewiele zasobów. Jego sterowana zdarzeniami
architektura pozwala ³atwo obs³ugiwaæ tysi±ce jednoczesnych po³±czeñ
do setek instancji bez ryzykowania stabilno¶ci systemu.

%prep
%setup -q

%build
%{__make} \
	DEBUG= \
	CPU_OPTS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/%{name},/etc/rc.d/init.d}

install haproxy $RPM_BUILD_ROOT%{_sbindir}
#install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG examples/* doc/*
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}/%{name}
#%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
