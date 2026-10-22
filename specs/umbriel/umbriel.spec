%define commit 5d657581e27e1a3fe604693779ca1405610f4f21
%define shortcommit %(c=%{commit}; echo ${c:0:7})
%define snapdate 20261022

Name:           umbriel
Summary:        A Wayland compositor built on wlroots
Version:        0.1.0
Release:        0.%{snapdate}.1
License:        MIT
Group:          Graphical desktop/Other
URL:            https://github.com/noctalia-dev/umbriel
# No tagged releases upstream yet, so this tracks a git snapshot
Source0:        %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildSystem:    meson
BuildRequires:  meson
BuildOption:    -Dtests=disabled
BuildOption:    -Dtracy=disabled

BuildRequires:  pkgconfig(wayland-server) >= 1.24
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.47
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wlroots-0.20) >= 0.20.1
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libinput) >= 1.27
BuildRequires:  pkgconfig(pixman-1) >= 0.43.0
BuildRequires:  pkgconfig(libdrm) >= 2.4.129
BuildRequires:  pkgconfig(libdisplay-info) >= 0.3.0
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libsystemd) >= 243
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(jemalloc)

Requires:       xwayland
Recommends:     xdg-desktop-portal-umbriel
Recommends:     fonts-ttf-dejavu

%description
Umbriel is a Wayland compositor designed for daily use, with scrolling,
dwindle and master layouts, per-output workspaces, window rules, blur,
shadows and fluid animations. It is built on wlroots and umbrielfx, an
in-tree fork of SceneFX, and supports HDR, VRR, tearing, direct scanout,
Xwayland and virtual outputs.

It runs independently and can be paired with the Noctalia desktop shell.

%prep
%autosetup -p1 -n %{name}-%{commit}

%files
%license LICENSE
%doc README.md PACKAGING.md SCOPE.md
%{_bindir}/umbriel
%{_bindir}/start-umbriel
%{_datadir}/umbriel/
%{_datadir}/wayland-sessions/umbriel.desktop
%{_prefix}/lib/systemd/user/umbriel.service
%{_prefix}/lib/systemd/user/umbriel-session.target
%{_prefix}/lib/systemd/user/umbriel-shutdown.target
