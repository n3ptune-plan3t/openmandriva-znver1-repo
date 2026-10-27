#define basever     5.0.0
#define prerel      beta
#define prerelnum   10
#define tag         v%{basever}-%{prerel}.%{prerelnum}

Name:           noctalia
Version:        5.4.0
Release:        1
Summary:        A sleek, customizable desktop shell crafted for Wayland.
License:        MIT
URL:            https://github.com/noctalia-dev/noctalia
Source0:        https://github.com/noctalia-dev/noctalia/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	meson
BuildRequires:	dbus-daemon
BuildRequires:  pkgconfig(sdbus-c++)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-ft)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pangoft2)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libsodium)
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  pkgconfig(polkit-gobject-1)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(wireplumber-0.5)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libqalculate)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(md4c)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(libical)
BuildRequires:	pkgconfig(glesv2)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	egl-devel
BuildRequires:  pam-devel
BuildRequires:  glibc-devel
BuildRequires:  pkgconfig(jemalloc)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(stb)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libjxl)
BuildRequires:  pkgconfig(libjxl_threads)
BuildRequires:  pkgconfig(sndfile)

# As last resort fallback
BuildRequires:	pkgconfig(epoxy)

# Needed by plugin_git_export_test
BuildRequires:  git-core

Requires:       hicolor-icon-theme	
# segfault at startup if it cannot connect to the pipewire daemon
Requires:       pipewire
	
# The plugin system uses git at runtime as well
Requires:       git-core
# Optional requirements for various functionality
Recommends:     upower
Recommends:     ddcutil
Recommends:     gnome-keyring
	
# From fedora
# Upstream doesn't currently offer a mechanism for building against system
# copies of these libraries.
Provides:       bundled(fzy)
Provides:       bundled(luau)
Provides:       bundled(material_color_utilities)
Provides:       bundled(wuffs)

Requires: brightnessctl
Requires: fonts-ttf-dejavu
#Recommends: gpu-screen-recorder-gtk
#Recommends: xdg-desktop-portal-gtk

# for now
#Recommends: cava
#Recommends: cliphist
Recommends: ddcutil
#Recommends: matugen
#Recommends: power-profiles-daemon
#Recommends: wlsunset

%rename noctalia-shell

%description
Noctalia is a native Wayland desktop shell for people who want a polished, configurable Linux desktop without stitching together a separate bar, launcher, notification daemon, lock screen, wallpaper tool, and settings UI.

It provides the shell layer around your compositor: bars, widgets, dock, launcher, control center, notifications, wallpaper, lock screen, session actions, clipboard history, OSDs, tray integration, and desktop widgets. The project is built directly on Wayland and OpenGL ES with no Qt or GTK dependency, so the UI, rendering, configuration, and IPC model are designed as one cohesive shell instead of a collection of unrelated panels and scripts.

%prep
%autosetup -n noctalia-%{version} -p1

# Upstream uses a git describe command to determine part of the --version
# output.  Since we're not building from a git checkout, we can change the
# fallback value to set this instead.
sed -e '/fallback/ s/unknown/%{version}/' -i meson.build

# Remove shebangs and execute permissions from template apply scripts to avoid
# rpmlint errors/warnings.
find assets/templates -type f -name '*.sh' \
    -exec sed -e '1 {/^#!/d}' -i '{}' + \
    -exec chmod -x '{}' +
    
# Move bundled licenses to the top level to make inclusion in %%files easier.
mv assets/fonts/tabler-icons-license.txt        LICENSE.tabler
mv third_party/fzy/LICENSE                      LICENSE.fzy
mv third_party/luau/LICENSE.txt                 LICENSE.luau
mv third_party/luau/lua_LICENSE.txt             LICENSE.luau_lua
mv third_party/material_color_utilities/LICENSE LICENSE.material_color_utilities
mv third_party/wuffs/LICENSE-APACHE             LICENSE-Apache-2.0.wuffs
mv third_party/wuffs/LICENSE-MIT                LICENSE-MIT.wuffs

%build
%meson	\
	-Dtests=enabled \
	-Dnative_optimizations=false \
	--buildtype=release

%meson_build	

%install
%meson_install

# shell completions
install -d -m 0755 %{buildroot}%{_datadir}/bash-completion/completions/
%{buildroot}%{_bindir}/noctalia completions bash > %{buildroot}%{_datadir}/bash-completion/completions/noctalia
install -d -m 0755 %{buildroot}%{_datadir}/fish/vendor_completions.d/
%{buildroot}%{_bindir}/noctalia completions fish > %{buildroot}%{_datadir}/fish/vendor_completions.d/noctalia.fish
install -d -m 0755 %{buildroot}%{_datadir}/zsh/site-functions/
%{buildroot}%{_bindir}/noctalia completions zsh > %{buildroot}%{_datadir}/zsh/site-functions/_noctalia

%files
%license LICENSE*
%{_bindir}/noctalia
%{_datadir}/applications/dev.noctalia.Noctalia.desktop
%{_datadir}/icons/hicolor/scalable/apps/noctalia.svg
%{_datadir}/noctalia
%{_datadir}/bash-completion/completions/noctalia
%{_datadir}/fish/vendor_completions.d/noctalia.fish
%{_datadir}/zsh/site-functions/_noctalia
