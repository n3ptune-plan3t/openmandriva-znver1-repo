%define commit 1cc6eb18ba0d6c82dd66999646d7e554f76a85b6
%define snapdate 20261019

Name:           xdg-desktop-portal-umbriel
Summary:        xdg-desktop-portal backend for the Umbriel compositor
Version:        0.1.0
Release:        0.%{snapdate}.1
License:        MIT
Group:          Graphical desktop/Other
URL:            https://github.com/noctalia-dev/xdg-desktop-portal-umbriel
# No tagged releases upstream yet, so this tracks a git snapshot
Source0:        %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildSystem:    meson
BuildOption:    -Dtests=false
BuildOption:    -Dpicker=enabled

BuildRequires:  pkgconfig(sdbus-c++) >= 2.0
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.39
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(gtk4) >= 4.12
BuildRequires:  glib2.0-common
BuildRequires:  pkgconfig(gio-2.0)

Requires:       xdg-desktop-portal
Requires:       pipewire
Requires:       wireplumber
Supplements:    umbriel

%description
xdg-desktop-portal-umbriel is an xdg-desktop-portal backend for the Umbriel
Wayland compositor. It implements the Screenshot and ScreenCast portal
interfaces, using the ext-image-copy-capture protocol and PipeWire, and ships
a GTK4 share picker for choosing which output or window to share.

%prep
%autosetup -p1 -n %{name}-%{commit}

%files
%license LICENSE
%doc README.md
%{_libexecdir}/xdg-desktop-portal-umbriel
%{_libexecdir}/umbriel-share-picker
%{_datadir}/xdg-desktop-portal/portals/umbriel.portal
%{_datadir}/xdg-desktop-portal/umbriel-portals.conf
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.umbriel.service
%{_prefix}/lib/systemd/user/xdg-desktop-portal-umbriel.service
