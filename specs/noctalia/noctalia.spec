# LTO + -g3 OOM-kills the final link on the CI runner
%global optflags %(echo '%{optflags}' | sed -E 's/-flto[^ ]*//g; s/-g3//g; s/-gdwarf-[0-9]//g')
%global build_ldflags %(echo '%{build_ldflags}' | sed -E 's/-flto[^ ]*//g; s/-g3//g; s/-gdwarf-[0-9]//g')
%global _debuginfo_subpackages 0
%global debug_package %{nil}

Name:           noctalia
Version:        5.5.0
Release:        1
Summary:        A sleek, customizable desktop shell crafted for Wayland.
License:        MIT
URL:            https://github.com/noctalia-dev/noctalia
Source0:        https://github.com/noctalia-dev/noctalia/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        stb_image_resize2.h

BuildRequires:  meson
BuildRequires:  dbus-daemon
BuildRequires:  pam-devel
BuildRequires:  glibc-devel
BuildRequires:  egl-devel
BuildRequires:  pkgconfig(sdbus-c++)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
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
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(jemalloc)
BuildRequires:  pkgconfig(stb)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libwebpdemux)
BuildRequires:  pkgconfig(libjxl)
BuildRequires:  pkgconfig(libjxl_threads)
# As last resort fallback
BuildRequires:  pkgconfig(epoxy)

Requires:       hicolor-icon-theme
# segfault at startup if it cannot connect to the pipewire daemon
Requires:       pipewire
# The plugin system uses git at runtime
Requires:       git-core
Requires:       brightnessctl
Requires:       fonts-ttf-dejavu
# Optional functionality
Recommends:     upower
Recommends:     ddcutil
Recommends:     gnome-keyring
Recommends:     sound-theme-freedesktop
# dlopen'ed for HEIC/HEIF/AVIF decoding
Recommends:     libheif

# Upstream doesn't offer a mechanism for building against system copies
# of these libraries (-Dsystem_libraries needs non-packaged layouts).
Provides:       bundled(fzy)
Provides:       bundled(luau)
Provides:       bundled(material_color_utilities)
Provides:       bundled(wuffs)

%rename noctalia-shell

%description
Noctalia is a native Wayland desktop shell for people who want a polished, configurable Linux desktop without stitching together a separate bar, launcher, notification daemon, lock screen, wallpaper tool, and settings UI.

It provides the shell layer around your compositor: bars, widgets, dock, launcher, control center, notifications, wallpaper, lock screen, session actions, clipboard history, OSDs, tray integration, and desktop widgets. The project is built directly on Wayland and OpenGL ES with no Qt or GTK dependency, so the UI, rendering, configuration, and IPC model are designed as one cohesive shell instead of a collection of unrelated panels and scripts.

%prep
%autosetup -n noctalia-%{version} -p1

# Upstream uses git describe for part of --version output; use the
# version as fallback since we're not building from a git checkout.
sed -e '/fallback/ s/unknown/%{version}/' -i meson.build

# Remove shebangs and exec bits from template apply scripts (rpmlint).
find assets/templates -type f -name '*.sh' \
    -exec sed -e '1 {/^#!/d}' -i '{}' + \
    -exec chmod -x '{}' +

# Move bundled licenses to the top level for easy inclusion in %%files.
mv lib/assets/fonts/tabler-icons-license.txt    LICENSE.tabler
mv third_party/fzy/LICENSE                      LICENSE.fzy
mv third_party/luau/LICENSE.txt                 LICENSE.luau
mv third_party/material_color_utilities/LICENSE LICENSE.material_color_utilities
mv lib/third_party/wuffs/LICENSE-APACHE         LICENSE-Apache-2.0.wuffs
mv lib/third_party/wuffs/LICENSE-MIT            LICENSE-MIT.wuffs
[ -f third_party/luau/lua_LICENSE.txt ] && mv third_party/luau/lua_LICENSE.txt LICENSE.luau_lua || :

# TEMP: OpenMandriva's stb package lacks stb_image_resize2.h; remove once fixed
mkdir -p vendor/stb
cp %{SOURCE1} vendor/stb/

%build
# TEMP: make stb/stb_image_resize2.h findable (see %%prep)
export CPATH="$PWD/vendor${CPATH:+:$CPATH}"

%meson \
	-Dtests=disabled \
	-Dnative_optimizations=false \
	-Db_lto=false \
	--buildtype=release

%meson_build -j2

%install
%meson_install

# shell completions (generated from the built binary, per PACKAGING.md)
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
%{_datadir}/applications/dev.noctalia.Noctalia.Annotator.desktop
%{_datadir}/icons/hicolor/scalable/apps/noctalia.svg
%{_datadir}/noctalia
%{_datadir}/bash-completion/completions/noctalia
%{_datadir}/fish/vendor_completions.d/noctalia.fish
%{_datadir}/zsh/site-functions/_noctalia
