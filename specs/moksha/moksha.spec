%define commit a556c48cf09f274db14e720c2648446e49d06206
%define _disable_ld_no_undefined 1
%define devname %{name}-devel

Name:           moksha
Version:        0.4.2
Release:        7
Summary:        Moksha desktop, a fork of Enlightenment E17 (from Bodhi Linux)
License:        BSD-2-Clause
Group:          Graphical desktop/Other
URL:            https://github.com/JeffHoogland/moksha
Source0:        https://github.com/JeffHoogland/moksha/archive/%{commit}/%{name}-%{commit}.tar.gz
# 1. scaling only affects native Moksha, never GTK/Qt (Xft.dpi / Xft/DPI)
Patch0:         moksha-no-gtk-qt-scale.patch
# 2. native touchpad gestures (tpgestd logic on libinput) + settings dialog
Patch1:         moksha-tpgest-native-gestures.patch
# 3. middle click on titlebar gracefully closes the window
Patch2:         moksha-middleclick-titlebar-close.patch
# 4. reservers space for shelves if needed
Patch3:         moksha-shelf-exclusive-space.patch

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
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libudev)
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

This build adds native touchpad gestures (tpgest), the Monocle tabbed/stacked
layout, graceful close on titlebar middle click, and scaling that does not
touch GTK/Qt applications. Touchpad gestures need read access to
/dev/input (membership of the "input" group).

%package -n moksha-epulse
Summary:        PulseAudio mixer for the Moksha desktop
Group:          Sound

%description -n moksha-epulse
Epulse, the PulseAudio mixer used by the Moksha desktop, with its library.

%package -n %{devname}
Summary:        Development files for Moksha modules
Group:          Development/C
Requires:       %{name} = %{EVRD}
Requires:       pkgconfig(efl)

%description -n %{devname}
Headers and pkg-config file needed to build Moksha modules.

%prep -a
# Upstream tarball is a bare git snapshot: no configure script.
# (Patches add modules and touch configure.ac / Makefile.am, so this
# must run after they are applied.)
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
%config(noreplace) %{_sysconfdir}/xdg/menus/e-applications.menu
%{_bindir}/enlightenment
%{_bindir}/enlightenment_*
%{_libdir}/enlightenment
%{_datadir}/enlightenment
%{_datadir}/xsessions/enlightenment.desktop

%files -n moksha-epulse
%{_bindir}/epulse
%{_libdir}/libepulse.so
%{_datadir}/epulse
%{_datadir}/applications/epulse.desktop
%{_datadir}/pixmaps/epulse.png

%files -n %{devname}
%{_includedir}/enlightenment
%{_libdir}/pkgconfig/enlightenment.pc
%{_libdir}/pkgconfig/everything.pc
