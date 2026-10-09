Summary:	Power saving diagnostic tool
Name:		 powertop
Version:	2.16.1
Release:	1
License:	GPL-2.0-only
Group:		System/Kernel and hardware
Url:		 https://github.com/fenrus75/powertop
Source0:	https://github.com/fenrus75/powertop/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Upstream switched to the meson build system as of 2.16
# (autotools files are still shipped but are stale/unmaintained).
BuildSystem:	meson
# Upstream installs the binary to bindir; powertop traditionally lives in sbin
BuildOption:	--bindir=%{_sbindir}

BuildRequires:	meson
BuildRequires:	gettext
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(libnl-3.0)
BuildRequires:	pkgconfig(libnl-genl-3.0)
BuildRequires:	pkgconfig(libtracefs)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(bash-completion)
BuildRequires:	pkgconfig(systemd)

%description
PowerTOP is a program that collects various pieces of information from
a system and presents an overview of how well a laptop is doing in
terms of power savings. In addition, PowerTOP will provide an
indication of which tunables and software components are the biggest
offenders in slurping up battery time. PowerTOP will update its display
frequently so that the impact of any changes can be seen directly.

%install -a
install -D -m 0644 powertop.service %{buildroot}%{_unitdir}/powertop.service
%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_sbindir}/%{name}
%{_unitdir}/%{name}.service
%{_mandir}/man8/%{name}.8*
%{_datadir}/bash-completion/completions/%{name}
