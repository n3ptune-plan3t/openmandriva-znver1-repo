Name:           xwayland-satellite
Version:        0.8.3
Release:        1
Summary:        Rootless Xwayland integration for Wayland compositors
License:        MPL-2.0
Group:          System/X11
URL:            https://github.com/Supreeeme/xwayland-satellite
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# Generated fresh by the znver1 repo's build.sh (cargo vendor)
Source1:        %{name}-%{version}-vendor.tar.xz

BuildRequires:  cargo
BuildRequires:  rust >= 1.85
BuildRequires:  clang
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-cursor)
Requires:       x11-server-xwayland

%description
xwayland-satellite grants rootless Xwayland integration to any Wayland
compositor implementing xdg_wm_base and viewporter. It is useful for
compositors that do not implement rootless Xwayland themselves, such as niri.

%prep
%autosetup -a1 -p1
mkdir -p .cargo
cat > .cargo/config.toml <<EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF
sed -i 's|^ExecStart=.*|ExecStart=%{_bindir}/%{name}|' resources/%{name}.service

%build
export CC=clang
export CXX=clang++
cargo build --release --offline --frozen -F systemd

%install
install -Dm755 target/release/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm644 resources/%{name}.service %{buildroot}%{_userunitdir}/%{name}.service
install -Dm644 %{name}.man %{buildroot}%{_mandir}/man1/%{name}.1

%check
cargo test --release --offline --frozen --lib || :

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_userunitdir}/%{name}.service
%{_mandir}/man1/%{name}.1*
