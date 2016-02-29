#
# Conditional build:
%bcond_with	lua		# LUA support
%bcond_without	zlib		# zlib support
%bcond_without	pcre		# pcre support
%bcond_without	ssl		# SSL support

Summary:	haproxy - high-performance TCP/HTTP load balancer
Summary(pl.UTF-8):	haproxy - wysoko wydajny load balancer TCP/HTTP
Name:		haproxy
Version:	1.6.3
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://www.haproxy.org/download/1.6/src/%{name}-%{version}.tar.gz
# Source0-md5:	3362d1e268c78155c2474cb73e7f03f9
Source1:	%{name}.init
Source2:	%{name}.cfg
URL:		http://www.haproxy.org/
%{?with_ssl:BuildRequires:	openssl-devel}
%{?with_pcre:BuildRequires:	pcre-devel}
BuildRequires:	rpmbuild(macros) >= 1.268
%{?with_zlib:BuildRequires:	zlib-devel}
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts
Requires:	uname(release) >= 2.6
Suggests:	vim-syntax-haproxy
Provides:	group(haproxy)
Provides:	user(haproxy)
Conflicts:	rpm < 4.4.2-45
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_vimdatadir	%{_datadir}/vim/vimfiles

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

%package -n vim-syntax-haproxy
Summary:	Vim syntax: haproxy configuration files syntax
Summary(pl.UTF-8):	Opis składni dla Vima: podświetlanie składni dla plików konfiguracyjnych haproxy
Group:		Applications/Editors/Vim
Requires:	vim-rt >= 4:6.3.058-3
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n vim-syntax-haproxy
This plugin provides syntax highlighting for haproxy configuration
files.

%description -n vim-syntax-haproxy -l pl.UTF-8
Ta wtyczka dostarcza podświetlanie składni dla plików konfiguracyjnych
haproxy.

%prep
%setup -q

mv examples/haproxy.vim .
mv examples/errorfiles .

%build
regparm_opts=
%ifarch %{ix86} %{x8664}
regparm_opts="USE_REGPARM=1"
%endif

%{__make} $regparm_opts \
	TARGET="linux2628" \
	CPU="generic" \
	USE_LINUX_TPROXY=1 \
	%{?with_lua:USE_LUA=1} \
	%{?with_ssl:USE_OPENSSL=1} \
	%{?with_pcre:USE_PCRE=1} \
	%{?with_zlib:USE_ZLIB=1} \
	CC="%{__cc}" \
	ADDINC="%{rpmcflags}" \
	ADDLIB="%{rpmldflags}"

%{__make} -C contrib/halog halog \
	CC="%{__cc}" \
	OPTIMIZE="%{optflags}"

%{__make} -C contrib/iprange iprange \
	CC="%{__cc}" \
	OPTIMIZE="%{optflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/%{name},%{_datadir}/%{name},/etc/rc.d/init.d} \
	$RPM_BUILD_ROOT%{_vimdatadir}/syntax

install -p haproxy $RPM_BUILD_ROOT%{_sbindir}
install -p contrib/halog/halog $RPM_BUILD_ROOT%{_sbindir}/halog
install -p contrib/iprange/iprange $RPM_BUILD_ROOT%{_sbindir}/iprange
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/haproxy.cfg
cp -p haproxy.vim $RPM_BUILD_ROOT%{_vimdatadir}/syntax
cp -a errorfiles $RPM_BUILD_ROOT%{_datadir}/%{name}

# Some small cleanups:
rm -f doc/gpl.txt examples/haproxy.vim

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 185 %{name}
%useradd -u 185 -d /usr/share/empty -g %{name} -c "haproxy user" %{name}

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG README README ROADMAP examples/* doc/* tests
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/haproxy.cfg
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/haproxy
%attr(755,root,root) %{_sbindir}/halog
%attr(755,root,root) %{_sbindir}/iprange
%{_datadir}/%{name}

%files -n vim-syntax-haproxy
%defattr(644,root,root,755)
%{_vimdatadir}/syntax/haproxy.vim
