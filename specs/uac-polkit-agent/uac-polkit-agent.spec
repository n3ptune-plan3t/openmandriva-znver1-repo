Name:           uac-polkit-agent
Summary:        Windows 7 style UAC polkit authentication agent for KDE Plasma
Version:        6.7.0
Release:        1
License:        GPL-2.0-or-later
Group:          Graphical desktop/KDE
URL:            https://github.com/aeroshell-desktop/uac-polkit-agent
Source0:        https://github.com/aeroshell-desktop/uac-polkit-agent/archive/refs/heads/Plasma/6.7.tar.gz#/%{name}-%{version}.tar.gz

BuildSystem:    cmake

BuildRequires:  cmake(ECM)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6Qml)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KF6WindowSystem)
BuildRequires:  cmake(KF6Notifications)
BuildRequires:  cmake(KF6DBusAddons)
BuildRequires:  cmake(KF6CoreAddons)
BuildRequires:  cmake(KF6Crash)
BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(PolkitQt6-1)
BuildRequires:  pkgconfig(systemd)

Requires:       polkit
Requires:       polkit-kde-agent-1

%description
A polkit authentication agent for KDE Plasma that mimics the Windows 7 UAC
elevation prompt. Used by the AeroThemePlasma session (USE_UAC_AGENT=1).

%prep
%autosetup -p1 -n uac-polkit-agent-Plasma-6.7

%files
%license LICENSES/*
%doc README.md
%{_libdir}/libexec/uac-polkit-agent
%{_datadir}/applications/io.gitgud.wackyideas.uac-polkit-agent.desktop
%{_sysconfdir}/xdg/autostart/uac-polkit-agent.desktop
%{_sysconfdir}/systemd/user/plasma-polkit-agent.service.d
%{_userunitdir}/uac-polkit-agent.service
%{_datadir}/knotifications6/uac-polkit-agent.notifyrc
%{_datadir}/locale/*/LC_MESSAGES/*.mo
