Name:           aeroshell-kwin-components
Summary:        KWin effects, scripts and other plugins for AeroShell-based desktops
Version:        6.7.5
Release:        1
License:        AGPL-3.0-or-later
Group:          Graphical desktop/KDE
URL:            https://github.com/aeroshell-desktop/aeroshell-kwin-components
Source0:        https://github.com/aeroshell-desktop/aeroshell-kwin-components/archive/refs/heads/Plasma/6.7.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  ninja
BuildRequires:  cmake(ECM)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6UiTools)
BuildRequires:  cmake(Qt6OpenGL)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6Xml)
BuildRequires:  cmake(Qt6WaylandClient)
BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6ConfigWidgets)
BuildRequires:  cmake(KF6CoreAddons)
BuildRequires:  cmake(KF6Crash)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KF6KIO)
BuildRequires:  cmake(KF6Service)
BuildRequires:  cmake(KF6Notifications)
BuildRequires:  cmake(KF6WidgetsAddons)
BuildRequires:  cmake(KF6WindowSystem)
BuildRequires:  cmake(KF6GuiAddons)
BuildRequires:  cmake(KF6KCMUtils)
BuildRequires:  cmake(KF6Svg)
BuildRequires:  cmake(KDecoration3)
BuildRequires:  cmake(PlasmaWaylandProtocols)
BuildRequires:  kwin-devel
BuildRequires:  kwin-x11-devel
BuildRequires:  aeroshell-libplasma
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  cmake(VulkanHeaders)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(libpipewire-0.3)

Requires:       aeroshell-libplasma
Requires:       kwin

%description
KWin effects, scripts, outlines and window rules for AeroShell-based desktops
(Aero Glass blur, Aero Glide, SMOD Peek, thumbnail task switcher and others).
This is the Wayland build.

%package x11
Summary:        AeroShell KWin effects for the X11 session
Group:          Graphical desktop/KDE
Requires:       %{name} = %{EVRD}
Requires:       kwin-x11

%description x11
X11 builds of the AeroShell KWin effects.

%prep
%autosetup -p1 -n aeroshell-kwin-components-Plasma-6.7

%build
# Wayland build (scripts, effects data, rules, translations)
cmake -S . -B build -G Ninja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
    -DKWIN_BUILD_WAYLAND:BOOL=ON
cmake --build build

# X11 build (effect plugins only)
cmake -S . -B build-x11 -G Ninja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
    -DKWIN_BUILD_WAYLAND:BOOL=OFF \
    -DKWIN_INSTALL_MISC:BOOL=OFF
cmake --build build-x11

%install
DESTDIR=%{buildroot} cmake --install build
DESTDIR=%{buildroot} cmake --install build-x11

%files
%license LICENSE
%doc README.md
%dir %{_datadir}/kwin/effects
%dir %{_datadir}/kwin/effects/*
%{_datadir}/kwin/effects/*/*
%{_datadir}/kwin/scripts
%{_datadir}/kwin/tabbox
%{_bindir}/aeroshell_update_default_rules
%{_datadir}/smod
%{_datadir}/aeroshell
%{_qtdir}/plugins/kwin/effects/configs/*.so
%{_qtdir}/plugins/kwin/effects/plugins/*.so
%{_datadir}/locale/*/LC_MESSAGES/aeroshell-kwin-components.mo

%files x11
%{_qtdir}/plugins/kwin-x11
