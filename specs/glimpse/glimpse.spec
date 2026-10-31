%define _disable_lto 1
%define debug_package %{nil}

%bcond tests 0

%global bins glimpsectl glimpse-panel glimpse-lock glimpse-wallpaper glimpse-sunset glimpse-notifications glimpse-agents glimpse-weather glimpse-calendar glimpse-idle glimpse-lens glimpse-shot glimpse-settings-daemon glimpse-compositor-niri glimpse-compositor-hyprland

Name:           glimpse
Version:        0.17.0
Release:        1
Summary:        Desktop shell suite for Wayland compositors
License:        BSD-3-Clause
Group:          Graphical desktop/Other
URL:            https://github.com/alex-oleshkevich/glimpse
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.xz

BuildRequires:  rust >= 1.95
BuildRequires:  cargo
BuildRequires:  clang
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  gettext
BuildRequires:  blueprint-compiler-devel
BuildRequires:  desktop-file-utils
BuildRequires:  pam-devel
BuildRequires:  pkgconfig(gtk4) >= 4.22
BuildRequires:  pkgconfig(libadwaita-1) >= 1.9
BuildRequires:  pkgconfig(gtk4-layer-shell-0) >= 1.3
BuildRequires:  pkgconfig(glib-2.0) >= 2.80
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(graphene-gobject-1.0)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libpulse-mainloop-glib)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libspa-0.2)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(zlib)

Requires:       pam
Requires:       geoclue
# Optional applets
Recommends:     ddcutil
Recommends:     upower
Recommends:     power-profiles-daemon
Recommends:     networkmanager
Recommends:     bluez
Recommends:     udisks2
Recommends:     cups
Recommends:     kdeconnect
Recommends:     xdg-desktop-portal
Recommends:     wl-clipboard

%description
glimpse is a desktop shell for Wayland compositors (niri and Hyprland),
built with GTK4 and libadwaita. It provides a panel, wallpaper, lock screen,
night light, notifications, weather, calendar and screenshot/lens tools,
run as systemd user services under glimpse-session.target.

%prep
%autosetup -a1 -p1
mkdir -p .cargo
cat > .cargo/config.toml <<'EOF'
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"

[net]
offline = true
EOF

%build
# Same LTO problem as OM's niri (rustc/LLVM error with thin LTO)
export CARGO_PROFILE_RELEASE_LTO=off
# glibc already provides gettext/intl; don't build bundled gettext-sys
export GETTEXT_SYSTEM=1
# baked into the binaries as the default locale dir
export PREFIX=%{_prefix}

cargo build --release --frozen --offline $(for b in %{bins}; do printf -- '--bin %s ' "$b"; done)

export GLIMPSE_LANGUAGES="$(tr '\n' ' ' < po/LINGUAS)"
scripts/i18n-build.sh

%install
export PREFIX=%{_prefix}
export DESTDIR=%{buildroot}
export GLIMPSE_BINARIES="%{bins}"
scripts/install.sh

%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
%if %{with tests}
export GETTEXT_SYSTEM=1
cargo test --release --frozen --offline --workspace
%endif

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/glimpse*
%{_userunitdir}/glimpse-*.service
%{_userunitdir}/glimpse-session.target
%{_datadir}/dbus-1/services/*.service
%{_datadir}/xdg-desktop-portal/portals/glimpse*.portal
%config(noreplace) %{_sysconfdir}/xdg-desktop-portal/glimpse-portals.conf
%config(noreplace) %{_sysconfdir}/xdg-desktop-portal/niri-portals.conf
%config(noreplace) %{_sysconfdir}/xdg-desktop-portal/hyprland-portals.conf
%config(noreplace) %{_sysconfdir}/pam.d/glimpse-lock
%config(noreplace) %{_sysconfdir}/geoclue/conf.d/glimpse.conf
%{_datadir}/glimpse/
%{_datadir}/applications/me.aresa.Glimpse.*.desktop
%{_metainfodir}/me.aresa.Glimpse.Shot.metainfo.xml
%{_iconsdir}/hicolor/scalable/apps/me.aresa.Glimpse*.svg
%{_iconsdir}/hicolor/symbolic/apps/me.aresa.Glimpse*-symbolic.svg
