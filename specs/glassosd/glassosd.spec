%bcond tests 0

Name:		glassosd
Version:	0.3.3
Release:	1
Summary:	Glass notification daemon, OSD and notification centre for Wayland
License:	GPL-2.0-or-later AND CC0-1.0
Group:		Graphical desktop/Other
URL:		https://github.com/SmallTardigrade/glassosd
Source0:	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildSystem:	cmake
BuildOption:	-DBUILD_TESTING:BOOL=%{?with_tests:ON}%{!?with_tests:OFF}

BuildRequires:	cmake(ECM)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Qml)
BuildRequires:	cmake(Qt6Quick)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(KF6WindowSystem)
BuildRequires:	cmake(KF6GuiAddons)
BuildRequires:	cmake(KF6Config)
BuildRequires:	cmake(KF6I18n)
BuildRequires:	cmake(KF6GlobalAccel)
BuildRequires:	cmake(KF6StatusNotifierItem)
BuildRequires:	cmake(KF6IdleTime)
BuildRequires:	cmake(LayerShellQt)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(systemd)
%if %{with tests}
BuildRequires:	cmake(Qt6Test)
BuildRequires:	%{_bindir}/dbus-run-session
%endif

# QML runtime is loaded dynamically, rpm cannot see it
Requires:	qt6-qtdeclarative
Requires:	qt6-qtwayland
# All icons are SVG; without this plugin they render blank
Requires:	qt6-qtsvg
# provides the wayland-shell-integration plugin, loaded at runtime
Requires:	layer-shell-qt
Requires:	kf6-breeze-icons
Recommends:	xdg-desktop-portal
Recommends:	plasma-integration
Suggests:	wireplumber
Suggests:	brightnessctl

%description
glassosd draws Wayland shell surfaces with one rounded, blurred glass look:
notification popups, the volume/brightness OSD, lock-key indicators and a
notification centre.

It implements the freedesktop Desktop Notifications specification plus KDE
extensions, the XDG desktop portal notification backend, history, Do Not
Disturb, snooze and per-app rules. It runs on any compositor implementing
wlr-layer-shell (KDE Plasma, Hyprland, sway, niri, river, Wayfire).

%files
%license LICENSE LICENSES/CC0-1.0.txt
%doc README.md
%{_bindir}/glassosd
%{_bindir}/glassosdctl
%{_bindir}/glassosd-setup
%{_mandir}/man1/glassosd.1*
%{_mandir}/man1/glassosdctl.1*
%{_mandir}/man5/glassosdrc.5*
%{_datadir}/glassosd/
%{_userunitdir}/glassosd.service
%{_datadir}/dbus-1/services/org.freedesktop.Notifications.service
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.glassosd.service
%dir %{_datadir}/xdg-desktop-portal
%dir %{_datadir}/xdg-desktop-portal/portals
%{_datadir}/xdg-desktop-portal/portals/glassosd.portal
