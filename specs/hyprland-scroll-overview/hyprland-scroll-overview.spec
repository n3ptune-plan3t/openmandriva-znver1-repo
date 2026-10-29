%define commit 07a944e4d16f11d2d9be6ce10bea74a6f1e5f2ae
%define shortcommit %(c=%{commit}; echo ${c:0:12})

Name:           hyprland-scroll-overview
Summary:        Niri-like scrollable workspace overview plugin for Hyprland
Version:        0.1
Release:        1
License:        BSD-3-Clause
Group:          Graphical desktop/Other
URL:            https://github.com/yayuuu/hyprland-scroll-overview
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{commit}.tar.gz

BuildSystem:    meson

BuildRequires:  pkgconfig(hyprland)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(lua5.4)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(xkbcommon)

%description
ScrollOverview is a niri-style overview plugin for Hyprland with scrollable
workspaces, per-workspace wallpapers, blur and shadows.

Hyprland plugins must match the exact Hyprland version they were built
against; rebuild this package whenever hyprland is updated.

%autosetup -n %{name}-%{commit} -p1

%build -p
export SCROLLOVERVIEW_BUILD_VERSION=%{shortcommit}

%install -a
# upstream installs scrolloverview.so straight into %{_libdir}
install -d %{buildroot}%{_libdir}/hyprland/plugins
mv %{buildroot}%{_libdir}/scrolloverview.so %{buildroot}%{_libdir}/hyprland/plugins/scrolloverview.so

%files
%license LICENSE
%doc README.md
%{_libdir}/hyprland/plugins/scrolloverview.so
