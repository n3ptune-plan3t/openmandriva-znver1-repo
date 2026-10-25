%{!?_unitdir:%global _unitdir %{_prefix}/lib/systemd/system}

Name:		lumdm
Version:	0.1.3
Release:	1
Summary:	Tiny, themeable TTY display manager for X11 and Wayland sessions
License:	MIT
URL:		https://github.com/n3ptune-plan3t/lumdm
Source0:	%{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:	pam-devel
Requires:	pam
Requires:	systemd
Recommends:	%{_bindir}/xinit
Recommends:	%{_bindir}/Xorg
Recommends:	%{_bindir}/numlockx
Provides:	bundled(stb_truetype)

%description
lumdm is a minimal, resource-efficient login manager written in C23 for old
laptops. It runs on a virtual console, authenticates through PAM, registers the
session with logind and launches any X11 or Wayland session found in
/usr/share/xsessions and /usr/share/wayland-sessions.

Features: themes (palette-programmed on the Linux VT, truecolor elsewhere),
ASCII wallpapers (festival, ocean, forest), optional system TrueType/OpenType
console fonts, remembered user and session, configurable F1-F12 actions,
optional NumLock default, and layered configuration: /etc/lumdm.conf for
system defaults and ~/.config/lumdm.conf for per-user overrides.

%prep
%autosetup -p1
sed -i 's|/usr/local/bin/lumdm|%{_bindir}/lumdm|' data/init/lumdm.service

%build
%{__cc} -std=c2x %{optflags} %{?build_ldflags} -o lumdm src/lumdm.c -lpam -lm

%install
install -Dm755 lumdm %{buildroot}%{_bindir}/lumdm
install -Dm644 data/lumdm.conf %{buildroot}%{_sysconfdir}/lumdm.conf
install -Dm644 data/pam.d/lumdm %{buildroot}%{_sysconfdir}/pam.d/lumdm
install -Dm644 data/init/lumdm.service %{buildroot}%{_unitdir}/lumdm.service
install -dm755 %{buildroot}%{_localstatedir}/lib/lumdm

%files
%license LICENSE
%doc README.md
%{_bindir}/lumdm
%config(noreplace) %{_sysconfdir}/lumdm.conf
%config(noreplace) %{_sysconfdir}/pam.d/lumdm
%{_unitdir}/lumdm.service
%dir %{_localstatedir}/lib/lumdm
