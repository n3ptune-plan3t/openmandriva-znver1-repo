%define debug_package %{nil}

Name:           niri-screenshare
Version:        0.2.5
Release:        1
Summary:        XDG Desktop Portal ScreenCast backend for niri
License:        GPL-3.0-or-later
Group:          Graphical desktop/Other
URL:            https://github.com/pantarune/niri-screenshare
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Vendored crates, create with:
#   tar xf niri-screenshare-%{version}.tar.gz && cd niri-screenshare-%{version}
#   cargo vendor --locked vendor && tar cJf ../niri-screenshare-%{version}-vendor.tar.xz vendor
Source1:        %{name}-%{version}-vendor.tar.xz

BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)

Requires:       xdg-desktop-portal
Requires:       pipewire
Requires:       niri

%description
niri-screenshare is an XDG Desktop Portal ScreenCast backend for niri with a
GTK4/libadwaita display and window picker and PipeWire integration. It can
replace xdg-desktop-portal-gnome for screen sharing while other portal
interfaces stay on the existing backends.

%prep
%autosetup -p1
tar xf %{SOURCE1}
mkdir -p .cargo
cat > .cargo/config.toml <<'EOF'
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
export CARGO_HOME="$PWD/.cargo-home"
cargo build --release --frozen --offline

%install
# upstream unit and D-Bus files hardcode /usr/lib/niri-screenshare
install -Dm755 target/release/%{name} %{buildroot}%{_prefix}/lib/%{name}
install -Dm644 data/niri.portal %{buildroot}%{_datadir}/xdg-desktop-portal/portals/niri.portal
install -Dm644 data/org.freedesktop.impl.portal.desktop.niri.service \
    %{buildroot}%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.niri.service
install -Dm644 data/%{name}.service %{buildroot}%{_userunitdir}/%{name}.service

%files
%license LICENSE
%doc README.md
%{_prefix}/lib/%{name}
%{_datadir}/xdg-desktop-portal/portals/niri.portal
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.niri.service
%{_userunitdir}/%{name}.service
