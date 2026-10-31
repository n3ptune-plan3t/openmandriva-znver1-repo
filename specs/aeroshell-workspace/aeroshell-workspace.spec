Name:           aeroshell-workspace
Summary:        Components required by AeroShell-based desktops
Version:        6.7.5
Release:        1
License:        AGPL-3.0-or-later
Group:          Graphical desktop/KDE
URL:            https://github.com/aeroshell-desktop/aeroshell-workspace
Source0:        https://github.com/aeroshell-desktop/aeroshell-workspace/archive/refs/heads/Plasma/6.7.tar.gz#/%{name}-%{version}.tar.gz

BuildSystem:    cmake

BuildRequires:  cmake(ECM)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Qml)
BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KF6KIO)
BuildRequires:  cmake(KF6Notifications)
BuildRequires:  cmake(KF6Service)
BuildRequires:  cmake(KF6WindowSystem)
BuildRequires:  cmake(KF6CoreAddons)
BuildRequires:  cmake(KF6KCMUtils)
BuildRequires:  cmake(KSysGuard)
BuildRequires:  cmake(LibNotificationManager)
BuildRequires:  cmake(LibTaskManager)
BuildRequires:  cmake(Plasma)
BuildRequires:  cmake(PlasmaActivities)
BuildRequires:  cmake(PlasmaActivitiesStats)
BuildRequires:  %{_lib}plasma-workspace-devel
BuildRequires:  aeroshell-libplasma

Requires:       plasma-workspace
Requires:       aeroshell-libplasma
Requires:       fontconfig

%description
Miscellaneous components required by AeroShell-based desktops: a KCM loader,
QML plugins (task manager, show desktop, utils), a Segoe UI hinting fontconfig
file and the MS-Windows mime types.

%prep
%autosetup -p1 -n aeroshell-workspace-Plasma-6.7

%files
%license LICENSE
%{_bindir}/aeroshell-kcmloader
%{_datadir}/mime/packages/*
%{_datadir}/fontconfig/*
%{_qtdir}/qml/aeroshell
%{_sysconfdir}/fonts/conf.d/95-segoeui-hinting.conf
