%bcond tests 1

Name:           xwob
Version:        0.2
Release:        1
Summary:        Overlay volume (or anything) bar for both X11 and Wayland
License:        GPL-3.0-only AND ISC
Group:          Graphical desktop/Other
URL:            https://github.com/n3ptune-plan3t/xwob
Source0:        https://github.com/n3ptune-plan3t/xwob/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  meson
BuildRequires:  scdoc
# X11 backend (xob fork)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(libconfig)
# Wayland backend (wob fork)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(inih)
BuildRequires:  pkgconfig(libseccomp)
%if %{with tests}
BuildRequires:  pkgconfig(cmocka)
%endif

# The launcher is useless without at least one backend. Both are recommended,
# so a default install works in either kind of session; a minimal install can
# drop one (e.g. dnf --setopt=install_weak_deps=False install xwob xwob-wayland).
Requires:       xwob-backend
Recommends:     xwob-x11
Recommends:     xwob-wayland

%description
xwob is one command that shows an overlay volume, brightness (or anything)
bar on both X11 and Wayland. It looks at the running session and starts the
right program: a fork of wob inside a Wayland session, a fork of xob inside
an X11 session. Values are read from standard input, one per line, and shown
with a percentage label whose text is black or white depending on what it
is drawn on.

This package contains the xwob launcher, its manual page and the systemd
user units (socket-activated FIFO at $XDG_RUNTIME_DIR/xwob.sock).

%package x11
Summary:        X11 backend for xwob (xob fork)
Group:          Graphical desktop/Other
License:        GPL-3.0-only
Provides:       xwob-backend = %{version}-%{release}

%description x11
The X11 backend of xwob, a fork of xob (X Overlay Bar) with a color-aware
percentage label. It is started by the xwob launcher inside an X11 session
(also usable on Wayland compositors without wlr-layer-shell, through
XWayland).

%package wayland
Summary:        Wayland backend for xwob (wob fork)
Group:          Graphical desktop/Other
License:        ISC
Provides:       xwob-backend = %{version}-%{release}

%description wayland
The Wayland backend of xwob, a fork of wob (Wayland Overlay Bar) with a
color-aware percentage label. It needs a compositor that supports the
wlr-layer-shell-unstable-v1 protocol and is started by the xwob launcher
inside a Wayland session.

%prep
%autosetup -p1

%build
export CC="%{__cc}"
export CFLAGS="%{optflags}"
export LDFLAGS="%{build_ldflags}"

# The Wayland backend is configured here (not by the top-level Makefile) so
# that the distribution's flags and a plain buildtype are used; the Makefile
# sees wob/build and skips its own meson setup.
meson setup wob/build wob \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--buildtype=plain \
	-Dseccomp=enabled \
	-Dman-pages=enabled \
	-Dsystemd-unit-files=disabled \
%if %{with tests}
	-Dtests=enabled
%else
	-Dtests=disabled
%endif

%make_build CC="%{__cc}" \
	prefix=%{_prefix} \
	bindir=%{_bindir} \
	libexecdir=%{_libexecdir} \
	sysconfdir=%{_sysconfdir} \
	unitdir=%{_userunitdir}

%check
%if %{with tests}
meson test -C wob/build --print-errorlogs
%endif

%install
# same variables as in %%build: they are baked into the launcher
%make_install \
	prefix=%{_prefix} \
	bindir=%{_bindir} \
	libexecdir=%{_libexecdir} \
	sysconfdir=%{_sysconfdir} \
	unitdir=%{_userunitdir}

%files
%license LICENSE.md
%doc README.md
%{_bindir}/xwob
%{_mandir}/man1/xwob.1*
%{_userunitdir}/xwob.service
%{_userunitdir}/xwob.socket
%dir %{_sysconfdir}/xwob
%dir %{_libexecdir}/xwob

%files x11
%license xob/LICENSE
%doc xob/README.md xob/CHANGELOG.md
%dir %{_sysconfdir}/xwob
%dir %{_libexecdir}/xwob
%{_libexecdir}/xwob/xwob-x11
%{_mandir}/man1/xwob-x11.1*
%config(noreplace) %{_sysconfdir}/xwob/xob.cfg

%files wayland
%license wob/LICENSE
%doc wob/README.md
%dir %{_sysconfdir}/xwob
%dir %{_libexecdir}/xwob
%{_libexecdir}/xwob/xwob-wayland
%{_mandir}/man1/xwob-wayland.1*
%{_mandir}/man5/xwob-wayland.ini.5*
%config(noreplace) %{_sysconfdir}/xwob/wob.ini
