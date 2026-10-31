Name:           aeroshell-smod
Summary:        SMOD window decoration and glow effect for AeroShell-based desktops
Version:        6.7.4
Release:        1
License:        AGPL-3.0-or-later
Group:          Graphical desktop/KDE
URL:            https://github.com/aeroshell-desktop/smod
Source0:        https://github.com/aeroshell-desktop/smod/archive/refs/heads/Plasma/6.7.tar.gz#/%{name}-%{version}.tar.gz

BuildSystem:    cmake
BuildOption:    -DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON
BuildOption:    -DBUILD_DECORATION:BOOL=ON
BuildOption:    -DBUILD_EFFECT:BOOL=ON
BuildOption:    -DBUILD_EFFECTX11:BOOL=OFF
BuildOption:    -DBUILD_TESTING:BOOL=OFF

BuildRequires:  cmake(ECM)
BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(KF6CoreAddons)
BuildRequires:  cmake(KF6ColorScheme)
BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6ConfigWidgets)
BuildRequires:  cmake(KF6GuiAddons)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KF6IconThemes)
BuildRequires:  cmake(KF6WindowSystem)
BuildRequires:  cmake(KF6KCMUtils)
BuildRequires:  cmake(KDecoration3)
BuildRequires:  kwin-devel
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  cmake(VulkanHeaders)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libdrm)

Requires:       aeroshell-libplasma
Requires:       kwin
Requires:       kvantum

%description
SMOD is the Windows 7 style window decoration (with theme) and the caption glow
KWin effect used by AeroShell-based desktops (Wayland build).

%prep
%autosetup -p1 -n smod-Plasma-6.7

%files
%license LICENSE
%doc README.md AUTHORS
%{_datadir}/smod
%{_qtdir}/plugins/org.kde.kdecoration3/org.smod.smod.so
%{_qtdir}/plugins/org.kde.kdecoration3.kcm/kcm_smoddecoration.so
%{_qtdir}/plugins/kwin/effects/plugins/smodglow.so
%{_includedir}/SMOD
%{_libdir}/pkgconfig/smoddecoration.pc
%{_datadir}/applications/kcm_smoddecoration.desktop
