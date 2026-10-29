Name:           hyprmod
Summary:        Native GTK4/libadwaita settings app for Hyprland
Version:        0.5.0
Release:        1
License:        GPL-3.0-or-later
Group:          Graphical desktop/Other
URL:            https://github.com/BlueManCZ/hyprmod
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildSystem:    python
BuildArch:      noarch

BuildRequires:  python%{pyver}dist(hatchling)
BuildRequires:  python%{pyver}dist(pip)
BuildRequires:  python%{pyver}dist(wheel)
# build hook runs glib-compile-schemas
BuildRequires:  glib2.0-common
BuildRequires:  desktop-file-utils

Requires:       python%{pyver}dist(pygobject) >= 3.56.2
Requires:       python%{pyver}dist(pycairo) >= 1.16
Requires:       python%{pyver}dist(hyprland-config) >= 0.9.19
Requires:       python%{pyver}dist(hyprland-schema) >= 0.7.1
Requires:       python%{pyver}dist(hyprland-state) >= 0.4.7
Requires:       python%{pyver}dist(hyprland-monitors) >= 0.9.0
Requires:       python%{pyver}dist(hyprland-socket) >= 0.12.2
Requires:       typelib(Gtk) = 4.0
Requires:       typelib(Gdk) = 4.0
Requires:       typelib(Adw) = 1
Requires:       glib2.0-common
Suggests:       typelib(GnomeDesktop) = 4.0

%description
HyprMod is a native GTK4/libadwaita settings app for Hyprland. Tweak any
option and see it change live. It writes only to its own hyprland-gui.conf
and includes a bezier curve editor, monitor layout editor, keybind, window,
layer and workspace rule editors, profiles, and Lua config support.

%install -a
install -Dm0644 data/applications/io.github.bluemancz.hyprmod.desktop \
	%{buildroot}%{_datadir}/applications/io.github.bluemancz.hyprmod.desktop
install -Dm0644 data/metainfo/io.github.bluemancz.hyprmod.metainfo.xml \
	%{buildroot}%{_datadir}/metainfo/io.github.bluemancz.hyprmod.metainfo.xml
install -Dm0644 data/icons/hicolor/scalable/apps/io.github.bluemancz.hyprmod.svg \
	%{buildroot}%{_datadir}/icons/hicolor/scalable/apps/io.github.bluemancz.hyprmod.svg

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/io.github.bluemancz.hyprmod.desktop

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/hyprmod
%{python_sitelib}/hyprmod
%{python_sitelib}/hyprmod-%{version}.dist-info
%{_datadir}/applications/io.github.bluemancz.hyprmod.desktop
%{_datadir}/metainfo/io.github.bluemancz.hyprmod.metainfo.xml
%{_datadir}/icons/hicolor/scalable/apps/io.github.bluemancz.hyprmod.svg
