%define commit 7c402e2331477aea08d702450acbd6504eee8193
%define _disable_ld_no_undefined 1
%define devname %{name}-devel

Name:           moksha
Version:        0.4.2
Release:        1
Summary:        Moksha desktop, a fork of Enlightenment E17 (from Bodhi Linux)
License:        BSD-2-Clause
Group:          Graphical desktop/Other
URL:            https://github.com/JeffHoogland/moksha
Source0:        https://github.com/JeffHoogland/moksha/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildSystem:    autotools
BuildOption:    --sysconfdir=%{_sysconfdir}
BuildOption:    --disable-bodhi

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  slibtool
BuildRequires:  libtool
BuildRequires:  gettext
BuildRequires:  gettext-devel
BuildRequires:  efl
BuildRequires:  pkgconfig(efl)
BuildRequires:  pkgconfig(eeze)
BuildRequires:  pkgconfig(elementary)
BuildRequires:  pkgconfig(emotion)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-shape)
BuildRequires:  pkgconfig(xcb-keysyms)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(udisks2)
BuildRequires:  pam-devel

Requires:       efl
Requires:       moksha-menu
Requires:       desktop-file-utils
Requires:       hicolor-icon-theme
Requires:       udisks2
Requires:       xkeyboard-config
Conflicts:      enlightenment

%description
Moksha is a fork of the Enlightenment 17 window manager and desktop shell,
maintained by Bodhi Linux. It is lightweight and highly configurable.

%package -n %{devname}
Summary:        Development files for Moksha modules
Group:          Development/C
Requires:       %{name} = %{EVRD}
Requires:       pkgconfig(efl)

%description -n %{devname}
Headers and pkg-config file needed to build Moksha modules.

%prep -a
# Upstream tarball is a bare git snapshot: no configure script
autoreconf -fi

%conf -p
export CFLAGS="%{optflags} -std=gnu17"
export CXXFLAGS="%{optflags}"

%build -p
# Out-of-tree build: Makefiles write .edj files into module subdirs that
# don't exist in the build dir, so mirror the source tree
(cd src && find . -type d) | while read -r d; do
  mkdir -p "_OMV_rpm_build/src/$d"
done

%install -a
# Locale files are installed under the "enlightenment" gettext domain
%find_lang enlightenment

%files -f enlightenment.lang
%license COPYING
%doc AUTHORS README.md
%dir %{_sysconfdir}/enlightenment
%config(noreplace) %{_sysconfdir}/enlightenment/sysactions.conf
%{_bindir}/enlightenment
%{_bindir}/enlightenment_*
# enlightenment_sys and enlightenment_backlight get their setuid bit
# from upstream's install-data-hook; keep it.
%{_libdir}/enlightenment
%{_datadir}/enlightenment
%{_datadir}/xsessions/enlightenment.desktop

%files -n %{devname}
%{_includedir}/enlightenment
%{_libdir}/pkgconfig/enlightenment.pc
