%define libname %mklibname Plasma
%define devname %mklibname Plasma -d

Name:           aeroshell-libplasma
Summary:        Plasma library and runtime components, with AeroShell patches
Version:        6.7.5
Release:        1
License:        LGPL-2.0-or-later
Group:          System/Libraries
URL:            https://github.com/aeroshell-desktop/libplasma
Source0:        https://github.com/aeroshell-desktop/libplasma/archive/refs/heads/Plasma/6.7.tar.gz#/%{name}-%{version}.tar.gz

BuildSystem:    cmake
BuildOption:    -DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON
BuildOption:    -DBUILD_EXAMPLES:BOOL=OFF
BuildOption:    -DBUILD_TESTING:BOOL=OFF

BuildRequires:  cmake(ECM)
BuildRequires:  python
BuildRequires:  gettext
BuildRequires:  cmake(Qt6)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6DBusTools)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6GuiPrivate)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6Qml)
BuildRequires:  cmake(Qt6QmlTools)
BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6QuickControls2)
BuildRequires:  cmake(Qt6QuickTest)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  cmake(Qt6Test)
BuildRequires:  cmake(Qt6WaylandClient)
BuildRequires:  cmake(KF6Archive)
BuildRequires:  cmake(KF6ColorScheme)
BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6ConfigWidgets)
BuildRequires:  cmake(KF6CoreAddons)
BuildRequires:  cmake(KF6GlobalAccel)
BuildRequires:  cmake(KF6GuiAddons)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KF6IconThemes)
BuildRequires:  cmake(KF6KCMUtils)
BuildRequires:  cmake(KF6KIO)
BuildRequires:  cmake(KF6Kirigami2)
BuildRequires:  cmake(KF6Notifications)
BuildRequires:  cmake(KF6Package)
BuildRequires:  cmake(KF6Svg)
BuildRequires:  cmake(KF6WindowSystem)
BuildRequires:  cmake(KF6XmlGui)
BuildRequires:  cmake(KWayland)
BuildRequires:  cmake(PlasmaActivities)
BuildRequires:  cmake(PlasmaWaylandProtocols)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-damage)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gl)

# Drop-in replacement for the stock libplasma packages
Provides:       libplasma = %{EVRD}
Provides:       %{libname} = %{EVRD}
Provides:       %{devname} = %{EVRD}
Provides:       plasma-framework-common = %{EVRD}
Conflicts:      libplasma
Conflicts:      %{libname}
Conflicts:      %{devname}
Conflicts:      plasma-framework-common

%description
libplasma with the AeroShell patches used by AeroThemePlasma. It replaces the
stock libplasma packages and provides the same sonames.

%prep
%autosetup -p1 -n libplasma-Plasma-6.7

%install -a
%find_lang %{name} --all-name --with-man

%files -f %{name}.lang
%license LICENSES/*
%doc README.md
%{_datadir}/plasma
%{_datadir}/qlogging-categories6/*plasma*
%{_datadir}/kdevappwizard/templates
%{_includedir}/Plasma
%{_includedir}/PlasmaQuick
%{_libdir}/cmake/Plasma
%{_libdir}/cmake/PlasmaQuick
%{_libdir}/libPlasma.so*
%{_libdir}/libPlasmaQuick.so*
%dir %{_qtdir}/qml/org
%{_qtdir}/qml/org/kde
%{_qtdir}/plugins/kf6/kirigami
%{_qtdir}/plugins/kf6/packagestructure
%{_qtdir}/metatypes/qt6plasma*_metatypes.json
