Summary:	haproxy - high-performance TCP/HTTP load balancer
Summary(pl.UTF-8):	haproxy - wysoko wydajny load balancer TCP/HTTP
Name:		haproxy
Version:	1.2.17
Release:	0.1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://haproxy.1wt.eu/download/1.2/src/%{name}-%{version}.tar.gz
# Source0-md5:	45a66691aa3b22996862e3e5bac4289c
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

%description -l pl.UTF-8
HA-Proxy to odwrotne proxy TCP/HTTP przeznaczone w szczególności dla
środowisk o wysokiej dostępności. W rzeczywistości może:
- przekazywać żądania HTTP w zależności od statycznie przypisanych
  ciasteczek;
- rozdzielać obciążenie między różne serwery zapewniając ciągłość
  łączności z serwerem poprzez użycie ciasteczek HTTP;
- przełączać na serwery zapasowe w przypadku, gdy główny zawiedzie;
- przyjmować połączenia na specjalne porty przeznaczone do
  monitorowania usług;
- zaprzestać przyjmowania połączeń bez zrywania istniejących;
- dodawać/modyfikować/usuwać nagłówki HTTP w obie strony;
- blokować żądania pasujące do określonego wzorca.

Wymaga bardzo niewiele zasobów. Jego sterowana zdarzeniami
architektura pozwala łatwo obsługiwać tysiące jednoczesnych połączeń
do setek instancji bez ryzykowania stabilności systemu.

%prep
%setup -q

%build
%{__make} \
	DEBUG= \
	CC="%{__cc}" \
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
