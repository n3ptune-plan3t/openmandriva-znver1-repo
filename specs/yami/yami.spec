%define debug_package %{nil}

Name:           yami
Version:        2.4.1
Release:        1
Summary:        Lightweight pixel-art Wayland shell for niri
License:        MIT
Group:          Graphical desktop/Other
URL:            https://github.com/Trendorin/yami
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.xz

BuildRequires:  cargo
BuildRequires:  rust >= 1.85
BuildRequires:  clang
BuildRequires:  pam-devel
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(wayland-client)

Requires:       niri
Requires:       /usr/bin/setsid
Recommends:     %{name}-fonts = %{EVRD}
Recommends:     grim
Recommends:     wl-clipboard
Recommends:     cliphist
Recommends:     /usr/bin/pactl
Recommends:     playerctl
Recommends:     networkmanager
Recommends:     brightnessctl
Recommends:     python
Recommends:     python%{pyver}dist(pillow)
Suggests:       curl
Suggests:       polkit
Suggests:       /usr/bin/parec
Suggests:       xdg-utils

%description
yami is a pixel-art Wayland shell for the niri compositor: bar, dock,
launcher, notifications, lock screen, polkit agent and settings.

%package fonts
Summary:        Pixel fonts and fontconfig rules for yami
Group:          System/Fonts
BuildArch:      noarch
Requires:       fontconfig

%description fonts
Tiny5, DotGothic16 and Terminess Nerd Font Mono, plus the fontconfig rules
yami uses for crisp pixel text (affects font rendering system-wide).

%prep
%autosetup -p1
tar xf %{SOURCE1} -C shell
mkdir -p shell/.cargo
cat > shell/.cargo/config.toml <<'EOF'
[source.crates-io]
replace-with = "vendored-sources"
[source.vendored-sources]
directory = "vendor"
EOF
# packaged install: no self-update by default (git clone + install.sh)
sed -i 's/update_check: true,/update_check: false,/' shell/src/config.rs

%build
cd shell
cargo build --release --frozen --offline -p yami-shell

%install
install -Dm755 shell/target/release/yami-shell %{buildroot}%{_bindir}/yami-shell
ln -s yami-shell %{buildroot}%{_bindir}/yami

install -d %{buildroot}%{_datadir}/fonts/%{name}
install -m644 fonts/*.ttf fonts/OFL-*.txt %{buildroot}%{_datadir}/fonts/%{name}/
install -Dm644 config/fontconfig/50-yami-pixel.conf \
  %{buildroot}%{_datadir}/fontconfig/conf.avail/50-yami-pixel.conf
install -d %{buildroot}%{_sysconfdir}/fonts/conf.d
ln -s %{_datadir}/fontconfig/conf.avail/50-yami-pixel.conf \
  %{buildroot}%{_sysconfdir}/fonts/conf.d/50-yami-pixel.conf

%files
%license LICENSE
%doc README.md CHANGELOG.md docs/CONFIG.md docs/SECURITY.md
%{_bindir}/yami
%{_bindir}/yami-shell

%files fonts
%{_datadir}/fonts/%{name}/
%{_datadir}/fontconfig/conf.avail/50-yami-pixel.conf
%{_sysconfdir}/fonts/conf.d/50-yami-pixel.conf