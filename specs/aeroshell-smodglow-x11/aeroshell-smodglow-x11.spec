Name:           aeroshell-smodglow-x11
Summary:        SMOD caption glow KWin effect for the X11 session
Version:        6.7.4
Release:        1
License:        AGPL-3.0-or-later
Group:          Graphical desktop/KDE
URL:            https://github.com/aeroshell-desktop/smod
Source0:        https://github.com/aeroshell-desktop/smod/archive/refs/heads/Plasma/6.7.tar.gz#/aeroshell-smod-%{version}.tar.gz

BuildSystem:    cmake
BuildOption:    -DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON
BuildOption:    -DBUILD_DECORATION:BOOL=OFF
BuildOption:    -DBUILD_EFFECT:BOOL=OFF
BuildOption:    -DBUILD_EFFECTX11:BOOL=ON
BuildOption:    -DBUILD_TESTING:BOOL=OFF

BuildRequires:  cmake(ECM)
BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(KF6ConfigWidgets)
BuildRequires:  cmake(KF6CoreAddons)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KDecoration3)
BuildRequires:  kwin-x11-devel
BuildRequires:  aeroshell-smod
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(xkbcommon)

Requires:       aeroshell-smod = %{version}
Requires:       kwin-x11

%description
SMOD caption glow KWin effect for the X11 session.

%prep
%autosetup -p1 -n smod-Plasma-6.7

%files
%license LICENSE
%{_qtdir}/plugins/kwin-x11
