%define commit 9b6f18badb8c4c88225a429c405e5194d8f5b56c

Name:           moksha-menu
Version:        1.0
Release:        1
Summary:        Freedesktop.org menu specification files for Moksha
License:        LGPL-2.1-only
Group:          Graphical desktop/Other
URL:            https://github.com/BodhiDev/Moksha-menu
Source0:        https://github.com/BodhiDev/Moksha-menu/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildSystem:    autotools
BuildArch:      noarch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  intltool
BuildRequires:  gettext-devel
BuildRequires:  pkgconfig(glib-2.0)

%description
Freedesktop.org menu specification files (moksha-applications.menu and
desktop directories) used by the Moksha desktop.

%prep -a
# Upstream ships no configure script; autogen.sh only regenerates it
./autogen.sh

%files
%license COPYING
%doc AUTHORS README
%config(noreplace) %{_sysconfdir}/xdg/menus/moksha-applications.menu
%{_datadir}/desktop-directories/moksha-*.directory
