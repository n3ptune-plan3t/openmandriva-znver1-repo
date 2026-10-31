%define _disable_ld_no_undefined 1
%global debug_package %{nil}

Name:           regreet
Version:        0.5.0
Release:        1
Summary:        Clean and customizable GTK4 greeter for greetd
License:        GPL-3.0-or-later AND MIT AND 0BSD
Group:          System/Base
URL:            https://github.com/rharish101/ReGreet
Source0:        %{url}/archive/%{version}/ReGreet-%{version}.tar.gz

# Rust 1.85+ (edition 2024)
BuildRequires:  cargo
BuildRequires:  rust >= 1.85
BuildRequires:  pkgconfig(gtk4) >= 4.16
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(graphene-gobject-1.0)
# glycin crate deps
BuildRequires:  pkgconfig(libseccomp)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(fontconfig)

Requires:       greetd
Requires:       accountsservice
Requires:       dbus
Requires:       glycin-loaders
Requires:       /usr/bin/startx
Requires:       /usr/bin/Xorg
Requires:       /usr/bin/env
Recommends:     cage
Recommends:     adwaita-icon-theme
# animated backgrounds / video
Recommends:     gstreamer1.0-plugins-good

%description
A clean and customizable GTK4-based greeter for greetd, written in Rust
using Relm4. Includes an "Xinitrc" X11 session that logs in through startx
and runs the user's ~/.xinitrc.

%prep
%autosetup -p1 -n ReGreet-%{version}

%build
export GREETD_CONFIG_DIR=%{_sysconfdir}/greetd
export STATE_DIR=%{_localstatedir}/lib/regreet
export LOG_DIR=%{_localstatedir}/log/regreet
export SESSION_DIRS=%{_datadir}/xsessions:%{_datadir}/wayland-sessions
export X11_CMD_PREFIX="startx /usr/bin/env"
export REBOOT_CMD="loginctl reboot"
export POWEROFF_CMD="loginctl poweroff"
cargo build --release --locked

%install
install -Dm0755 target/release/regreet %{buildroot}%{_bindir}/regreet
install -Dm0644 systemd-tmpfiles.conf %{buildroot}%{_tmpfilesdir}/regreet.conf
install -Dm0644 regreet.sample.toml %{buildroot}%{_sysconfdir}/greetd/regreet.toml
install -dm0755 %{buildroot}%{_localstatedir}/lib/regreet
install -dm0755 %{buildroot}%{_localstatedir}/log/regreet

# xinitrc session: startx runs this instead of xinitrc, which then execs ~/.xinitrc
install -dm0755 %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/regreet-xinitrc <<'EOS'
#!/bin/sh
if [ -f "$HOME/.xinitrc" ]; then
    exec sh "$HOME/.xinitrc"
elif [ -f /etc/X11/xinit/xinitrc ]; then
    exec sh /etc/X11/xinit/xinitrc
fi
echo "regreet-xinitrc: no ~/.xinitrc found" >&2
exit 1
EOS
chmod 0755 %{buildroot}%{_bindir}/regreet-xinitrc

install -dm0755 %{buildroot}%{_datadir}/xsessions
cat > %{buildroot}%{_datadir}/xsessions/xinitrc.desktop <<'EOS'
[Desktop Entry]
Name=Xinitrc
Comment=Start X11 using ~/.xinitrc
Exec=regreet-xinitrc
Type=Application
EOS

%files
%license LICENSE LICENSES/
%doc README.md
%{_bindir}/regreet
%{_bindir}/regreet-xinitrc
%{_datadir}/xsessions/xinitrc.desktop
%{_tmpfilesdir}/regreet.conf
%config(noreplace) %{_sysconfdir}/greetd/regreet.toml
%dir %attr(0755,greeter,greeter) %{_localstatedir}/lib/regreet
%dir %attr(0755,greeter,greeter) %{_localstatedir}/log/regreet
