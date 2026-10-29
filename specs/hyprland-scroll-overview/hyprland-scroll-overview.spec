%global __provides_exclude_from ^(%{_libdir}/hyprland/.*\\.so)$
%global _disable_ld_no_undefined %nil

%define commit 07a944e4d16f11d2d9be6ce10bea74a6f1e5f2ae
%define shortcommit %(c=%{commit}; echo ${c:0:12})

Name:           hyprland-scroll-overview
Summary:        Niri-like scrollable workspace overview plugin for Hyprland
Version:        0.1
Release:        1
License:        BSD-3-Clause
Group:          System/Libraries
URL:            https://github.com/yayuuu/hyprland-scroll-overview
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{commit}.tar.gz

BuildSystem:    meson
BuildOption:    --libdir=%{_libdir}/hyprland

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(hyprland)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(lua) >= 5.4
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(xkbcommon)
Requires:       hyprland

%description
ScrollOverview is a niri-style overview plugin for Hyprland with scrollable
workspaces, per-workspace wallpapers, blur and shadows.

Hyprland plugins must match the exact Hyprland version they were built
against; rebuild this package whenever hyprland is updated.

%prep
%autosetup -n %{name}-%{commit} -p1
# meson.build globs *.cpp recursively and would pick up files from ./build
sed -i "s|'find', '.', '-name'|'find', '.', '-maxdepth', '1', '-name'|" meson.build
grep -q -- "-maxdepth" meson.build

%build -p
export SCROLLOVERVIEW_BUILD_VERSION=%{shortcommit}
export CXXFLAGS="%{optflags} -I%{_includedir}/hyprland/"

%files
%license LICENSE
%doc README.md
%{_libdir}/hyprland/libscrolloverview.so
