%global appname AyuGramDesktop

Name:           ayugram-desktop
Version:        7.2.9
Release:        1
Summary:        Telegram Desktop fork with Ghost mode and message history
License:        GPL-3.0-or-later WITH OpenSSL-exception
Group:          Networking/Instant messaging
URL:            https://github.com/AyuGram/AyuGramDesktop
Source0:        %{url}/releases/download/v%{version}/%{appname}-%{version}-full.tar.gz#/%{name}-%{version}-full.tar.gz

BuildSystem:    cmake
BuildOption:    -DTDESKTOP_API_ID=611335
BuildOption:    -DTDESKTOP_API_HASH=d524b414d21f4d37f08684c1df41ac9c
BuildOption:    -DDESKTOP_APP_DISABLE_AUTOUPDATE:BOOL=ON
BuildOption:    -DDESKTOP_APP_DISABLE_CRASH_REPORTS:BOOL=ON
BuildOption:    -DDESKTOP_APP_USE_PACKAGED:BOOL=ON
BuildOption:    -DDESKTOP_APP_USE_PACKAGED_FONTS:BOOL=ON
BuildOption:    -DDESKTOP_APP_DISABLE_WAYLAND_INTEGRATION:BOOL=OFF
BuildOption:    -DDESKTOP_APP_DISABLE_X11_INTEGRATION:BOOL=OFF

BuildRequires:  cmake
BuildRequires:  ninja
BuildRequires:  clang
BuildRequires:  gperf
BuildRequires:  python
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(appstream-glib)
BuildRequires:  cmake(Microsoft.GSL)
BuildRequires:  cmake(OpenAL)
BuildRequires:  cmake(Qt6Concurrent)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Core5Compat)
BuildRequires:  cmake(Qt6CorePrivate)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6GuiPrivate)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6OpenGL)
BuildRequires:  cmake(Qt6OpenGLWidgets)
BuildRequires:  cmake(Qt6ShaderTools)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  cmake(Qt6WaylandClient)
BuildRequires:  cmake(Qt6WaylandClientPrivate)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6WidgetsPrivate)
BuildRequires:  cmake(KF6CoreAddons)
BuildRequires:  cmake(absl)
BuildRequires:  cmake(ada)
BuildRequires:  cmake(fmt)
BuildRequires:  cmake(range-v3)
BuildRequires:  cmake(tg_owt)
BuildRequires:  cmake(tde2e)
BuildRequires:  cmake(tl-expected)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(glibmm-2.68)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(hunspell)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libcmark-gfm)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libsrtp2)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  pkgconfig(minizip)
BuildRequires:  pkgconfig(openh264)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  pkgconfig(protobuf-lite)
BuildRequires:  pkgconfig(rnnoise)
BuildRequires:  pkgconfig(tlottie)
BuildRequires:  pkgconfig(vpx)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-keysyms)
BuildRequires:  pkgconfig(xcb-record)
BuildRequires:  pkgconfig(xcb-screensaver)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  lib64qrcodegencpp-devel

Requires:       hicolor-icon-theme
Requires:       qt6-qtimageformats
Recommends:     qt6-qtwayland
Recommends:     xdg-desktop-portal
Recommends:     kf6-kimageformats
Recommends:     open-sans-fonts
Recommends:     lib64webkit2gtk6.0

%description
AyuGram is a Telegram Desktop fork with Ghost mode, local message history
(including deleted messages), message filters, translation and extra
interface customization. Use at your own risk: third-party clients may
violate Telegram's terms.

%prep
%autosetup -p1 -n %{appname}-%{version}-full

%files
%license LICENSE LEGAL
%doc README.md changelog.txt
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/*.service
%{_datadir}/icons/hicolor/*/apps/*
%{_metainfodir}/*.metainfo.xml
