%define _disable_ld_no_undefined 1
%define tag xlibre-xf86-input-synaptics-%{version}

Name:           xlibre-xf86-input-synaptics
Version:        25.0.0
Release:        1
Summary:        XLibre fork of the X.Org Synaptics touchpad driver
Group:          System/X11
License:        MIT
URL:            https://github.com/X11Libre/xf86-input-synaptics
Source0:        %{url}/archive/refs/tags/%{tag}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool-base
BuildRequires:  slibtool
BuildRequires:  make
BuildRequires:  x11-util-macros >= 1.19.2
BuildRequires:  x11-proto-devel
BuildRequires:  x11-server-devel >= 25.0.0
BuildRequires:  pkgconfig(libevdev) >= 0.4
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xi) >= 1.2
BuildRequires:  pkgconfig(xtst)

Requires:       x11-server-common %(xserver-sdk-abi-requires xinput)
Conflicts:      x11-driver-input-synaptics

%description
XLibre fork of the X.Org Synaptics input driver for notebook touchpads,
with the synclient and syndaemon tools.

%package devel
Summary:        Development files for the XLibre synaptics driver
Group:          Development/C
Requires:       %{name} = %{EVRD}
Conflicts:      x11-driver-input-synaptics-devel

%description devel
Header files for programming against the XLibre synaptics driver.

%prep
%autosetup -p1 -n xf86-input-synaptics-%{tag}
mkdir -p m4
autoreconf -fiv

%build
%configure
%make_build

%install
%make_install

%files
%license COPYING
%doc README.md
%{_bindir}/synclient
%{_bindir}/syndaemon
%{_libdir}/xorg/modules/input/synaptics_drv.so
%{_datadir}/X11/xorg.conf.d/70-synaptics.conf
%{_mandir}/man1/synclient.*
%{_mandir}/man1/syndaemon.*
%{_mandir}/man4/synaptics.*

%files devel
%{_includedir}/xorg/synaptics-properties.h
