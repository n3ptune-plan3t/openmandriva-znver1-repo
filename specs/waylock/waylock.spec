Name:		waylock
Version:	1.6.0
Release:	1
Summary:	Small, secure Wayland screenlocker
License:	ISC AND MIT
Group:		Graphical desktop/Other
URL:		https://codeberg.org/ifreund/waylock
Source0:	https://codeberg.org/ifreund/waylock/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Zig package manager dependencies from build.zig.zon (no network on ABF).
# Keep these in sync with build.zig.zon on every version bump.
Source10:	https://codeberg.org/ifreund/zig-wayland/archive/v0.6.0.tar.gz#/zig-wayland-0.6.0.tar.gz
Source11:	https://codeberg.org/ifreund/zig-xkbcommon/archive/v0.3.0.tar.gz#/zig-xkbcommon-0.3.0.tar.gz

# waylock tracks the latest Zig minor release; 1.6.0 needs Zig 0.16
BuildRequires:	zig >= 0.16
BuildRequires:	scdoc
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-protocols)
BuildRequires:	pkgconfig(wayland-scanner)
BuildRequires:	pkgconfig(xkbcommon)

%description
Waylock is a small screenlocker for Wayland compositors implementing the
ext-session-lock-v1 protocol. That protocol is significantly more robust than
previous client-side Wayland screen locking approaches; in particular, the
screenlocker crashing does not cause the session to be unlocked.

Use it together with swayidle (or a similar tool) to lock automatically after
a period of inactivity or before sleep.

%prep
%autosetup -p1
%zig_prep
# Populate ./zig-pkg/<hash> from the local tarballs so that
# "zig build --system zig-pkg" (part of %%_zig_build_options) can find them.
# The hashes are verified against build.zig.zon by zig itself.
%{__zig} fetch %{_zig_fetch_options} %{SOURCE10}
%{__zig} fetch %{_zig_fetch_options} %{SOURCE11}

%build
# -Dtarget/-Dcpu=baseline/--release=safe come from the zig macros.
# Symbols are intentionally kept (no -Dstrip) so debuginfo can be extracted.
%zig_build -Dpie

%install
%zig_install -Dpie

# PAM only reads /etc/pam.d, so install the config there ourselves and drop
# anything the install step may have put under /usr/etc.
install -D -m 0644 pam.d/waylock %{buildroot}%{_sysconfdir}/pam.d/waylock
rm -rf %{buildroot}%{_prefix}/etc

%files
%license LICENSE
%doc README.md
%{_bindir}/waylock
%{_mandir}/man1/waylock.1*
%config(noreplace) %{_sysconfdir}/pam.d/waylock
