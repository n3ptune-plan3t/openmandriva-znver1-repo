%define _disable_ld_no_undefined 1

Name:           aerothemeplasma-desktop
Summary:        Windows 7 (Aero) inspired desktop shell, plasmoids and themes for KDE Plasma 6
Version:        6.7.5
Release:        1
License:        GPL-2.0-or-later AND LGPL-2.1-or-later AND AGPL-3.0-only
Group:          Graphical desktop/KDE
URL:            https://gitgud.io/wackyideas/aerothemeplasma
Source0:        https://gitgud.io/wackyideas/aerothemeplasma/-/archive/Plasma/6.7/aerothemeplasma-Plasma-6.7.tar.gz

BuildRequires:  cmake
BuildRequires:  ninja
BuildRequires:  cmake(ECM)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Core5Compat)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6GuiPrivate)
BuildRequires:  cmake(Qt6Qml)
BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6QuickControls2)
BuildRequires:  cmake(Qt6QuickWidgets)
BuildRequires:  cmake(Qt6Sql)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6Concurrent)
BuildRequires:  cmake(Qt6WaylandClient)
BuildRequires:  cmake(Qt6WaylandCompositor)
BuildRequires:  cmake(KF6Auth)
BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6CoreAddons)
BuildRequires:  cmake(KF6Crash)
BuildRequires:  cmake(KF6GlobalAccel)
BuildRequires:  cmake(KF6GuiAddons)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KF6IconThemes)
BuildRequires:  cmake(KF6ItemModels)
BuildRequires:  cmake(KF6KCMUtils)
BuildRequires:  cmake(KF6KIO)
BuildRequires:  cmake(KF6Kirigami)
BuildRequires:  cmake(KF6NewStuff)
BuildRequires:  cmake(KF6Notifications)
BuildRequires:  cmake(KF6NotifyConfig)
BuildRequires:  cmake(KF6Package)
BuildRequires:  cmake(KF6QQC2DesktopStyle)
BuildRequires:  cmake(KF6StatusNotifierItem)
BuildRequires:  cmake(KF6Svg)
BuildRequires:  cmake(KF6WindowSystem)
BuildRequires:  cmake(KF6XmlGui)
BuildRequires:  cmake(KF6Runner)
BuildRequires:  cmake(KF6DBusAddons)
BuildRequires:  cmake(KF6Sonnet)
BuildRequires:  cmake(KF6Attica)
BuildRequires:  cmake(KF6Archive)
BuildRequires:  cmake(Plasma)
BuildRequires:  cmake(PlasmaQuick)
BuildRequires:  cmake(Plasma5Support)
BuildRequires:  cmake(PlasmaActivities)
BuildRequires:  cmake(PlasmaActivitiesStats)
BuildRequires:  cmake(PlasmaWaylandProtocols)
BuildRequires:  cmake(KWin)
BuildRequires:  cmake(KDecoration3)
BuildRequires:  cmake(LibNotificationManager)
BuildRequires:  cmake(LibTaskManager)
BuildRequires:  cmake(KirigamiAddons)
BuildRequires:  cmake(PolkitQt6-1)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-randr)
BuildRequires:  pkgconfig(xcb-shm)
BuildRequires:  pkgconfig(xcb-damage)
BuildRequires:  pkgconfig(gmp)
BuildRequires:  plasma-wayland-protocols
BuildRequires:  plasma-workspace-devel
BuildRequires:  desktop-file-utils

Requires:       plasma-desktop
Requires:       plasma-workspace
Requires:       kvantum
Requires:       sddm
Requires:       polkit-kde-agent-1
Requires:       qml(org.kde.kirigamiaddons.formcard)
Recommends:     aeroshell-libplasma
Recommends:     aeroshell-workspace
Recommends:     aeroshell-kwin-components
Recommends:     aeroshell-smod
Recommends:     uac-polkit-agent
Recommends:     aerothemeplasma-icons
Recommends:     aerothemeplasma-sounds

%description
AeroThemePlasma recreates the look and feel of Windows 7 (Aero) on KDE Plasma 6.

This package provides the Plasma shell, Seven Start menu, Seven Tasks, system
tray, volume, battery, clock, network, keyboard layout and show-desktop
plasmoids, the Seven-Black Plasma theme, Aero colour scheme, Windows7Aero
Kvantum theme, authui7 look-and-feel, SDDM theme, first-run wizard (atpootb)
and the AeroThemePlasma Wayland session.

%package x11
Summary:        AeroThemePlasma X11 session
Group:          Graphical desktop/KDE
Requires:       %{name} = %{EVRD}
Requires:       kwin-x11
Requires:       plasma-x11-session
Recommends:     aeroshell-kwin-components-x11
Recommends:     aeroshell-smodglow-x11

%description x11
X11 session entry (aerothemeplasmax11.desktop) and startatp launcher for
AeroThemePlasma.

%prep
%autosetup -p1 -n aerothemeplasma-Plasma-6.7

%build
# Pass 1: Wayland session + all shell components
cmake -S . -B build -G Ninja \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-DINSTALL_X11_COMPONENTS:BOOL=OFF \
	-DKAUTH_ACTIONS_QML:BOOL=ON
cmake --build build

# Pass 2: X11 session files only
cmake -S . -B build-x11 -G Ninja \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DINSTALL_X11_COMPONENTS:BOOL=ON
cmake --build build-x11

%install
DESTDIR=%{buildroot} cmake --install build
DESTDIR=%{buildroot} cmake --install build-x11

%files
%license LICENSE
%doc README.md INSTALL.md DOCUMENTATION.md
%{_bindir}/atpootb
%{_bindir}/startatp-wayland
%{_libdir}/qt6/plugins/plasma/applets/io.gitgud.wackyideas.*.so
%{_libdir}/qt6/plugins/kf6/kded/statusnotifierwatcher.so
%{_libdir}/qt6/qml/io/gitgud/wackyideas
%{_libexecdir}/kauth/ootbcursor_authhelper
%{_datadir}/dbus-1/system.d/io.gitgud.wackyideas.ootb.conf
%{_datadir}/dbus-1/system-services/io.gitgud.wackyideas.ootb.service
%{_datadir}/polkit-1/actions/io.gitgud.wackyideas.ootb.policy
%{_datadir}/plasma/plasmoids/io.gitgud.wackyideas.*
%{_datadir}/plasma/shells/io.gitgud.wackyideas.desktop
%{_datadir}/plasma/desktoptheme/Seven-Black
%{_datadir}/plasma/look-and-feel/authui7
%{_datadir}/plasma/layout-templates/io.gitgud.wackyideas.taskbar
%{_datadir}/color-schemes/Aero.colors
%{_datadir}/Kvantum/Windows7Aero
%{_datadir}/sddm/themes/sddm-theme-mod
%{_datadir}/wayland-sessions/aerothemeplasma.desktop
%{_datadir}/aerothemeplasma
%{_datadir}/locale/*/LC_MESSAGES/*atpootb*.mo
%{_sysconfdir}/xdg/aerothemeplasma
%{_sysconfdir}/xdg/autostart/x-atpootb.desktop

%files x11
%{_bindir}/startatp
%{_datadir}/xsessions/aerothemeplasmax11.desktop
