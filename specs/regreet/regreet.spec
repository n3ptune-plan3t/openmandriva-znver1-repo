%define _disable_ld_no_undefined 1
%global debug_package %{nil}

Name:           regreet
Version:        0.2.0
Release:        2
Summary:        Clean and customizable GTK4 greeter for greetd
License:        GPL-3.0-or-later AND MIT AND CC0-1.0
Group:          System/Base
URL:            https://github.com/rharish101/ReGreet
Source0:        %{url}/archive/%{version}/ReGreet-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.zst

BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(cairo)

Requires:       greetd
Requires:       accountsservice
Requires:       dbus
Requires:       /usr/bin/startx
Requires:       /usr/bin/Xorg
Requires:       /usr/bin/env
Recommends:     cage
Recommends:     adwaita-icon-theme

%description
A clean and customizable GTK4-based greeter for greetd, written in Rust
using Relm4. Includes an "Xinitrc" X11 session that logs in through startx
and runs the user's ~/.xinitrc.

%prep
%autosetup -p1 -n ReGreet-%{version} -a1
mkdir -p .cargo
cat > .cargo/config.toml <<'EOF'
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
export GREETD_CONFIG_DIR=%{_sysconfdir}/greetd
export STATE_DIR=%{_localstatedir}/lib/regreet
export LOG_DIR=%{_localstatedir}/log/regreet
export SESSION_DIRS=%{_datadir}/xsessions:%{_datadir}/wayland-sessions
export X11_CMD_PREFIX="startx /usr/bin/env"
export REBOOT_CMD="loginctl reboot"
export POWEROFF_CMD="loginctl poweroff"
cargo build --release --frozen --offline

%install
install -Dm0755 target/release/regreet %{buildroot}%{_bindir}/regreet
install -Dm0644 systemd-tmpfiles.conf %{buildroot}%{_tmpfilesdir}/regreet.conf
install -Dm0644 regreet.sample.toml %{buildroot}%{_sysconfdir}/greetd/regreet.toml
install -dm0755 %{buildroot}%{_localstatedir}/lib/regreet
install -dm0755 %{buildroot}%{_localstatedir}/log/regreet

# xinitrc session: startx runs this instead of xinitrc, which then execs ~/.xinitrc
install -dm0755 %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/regreet-xinitrc <<'EOF'
#!/bin/sh
if [ -f "$HOME/.xinitrc" ]; then
    exec sh "$HOME/.xinitrc"
elif [ -f /etc/X11/xinit/xinitrc ]; then
    exec sh /etc/X11/xinit/xinitrc
fi
echo "regreet-xinitrc: no ~/.xinitrc found" >&2
exit 1
EOF
chmod 0755 %{buildroot}%{_bindir}/regreet-xinitrc

install -dm0755 %{buildroot}%{_datadir}/xsessions
cat > %{buildroot}%{_datadir}/xsessions/xinitrc.desktop <<'EOF'
[Desktop Entry]
Name=Xinitrc
Comment=Start X11 using ~/.xinitrc
Exec=regreet-xinitrc
Type=Application
EOF

%files
%license LICENSE
%doc README.md
%{_bindir}/regreet
%{_bindir}/regreet-xinitrc
%{_datadir}/xsessions/xinitrc.desktop
%{_tmpfilesdir}/regreet.conf
%config(noreplace) %{_sysconfdir}/greetd/regreet.toml
%dir %attr(0755,greeter,greeter) %{_localstatedir}/lib/regreet
%dir %attr(0755,greeter,greeter) %{_localstatedir}/log/regreet
