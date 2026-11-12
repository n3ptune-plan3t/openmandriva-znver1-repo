%global appname AyuGramDesktop
%global _disable_lto 1
%global shimdir %{_builddir}/%{name}-%{version}-shim
%global optflags %{optflags} -I%{shimdir}
%global optflags %(echo %{optflags} | sed -e 's/-flto[^ ]*//g')
%global _debuginfo_subpackages 0
%global debug_package %{nil}.

Name:           ayugram-desktop
Version:        7.2.9
Release:        2
Summary:        Telegram Desktop fork with Ghost mode and message history
License:        GPL-3.0-or-later WITH openvpn-openssl-exception
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
BuildOption:    -DCMAKE_INTERPROCEDURAL_OPTIMIZATION:BOOL=OFF
BuildOption:    -DDESKTOP_APP_LTO:BOOL=OFF
BuildOption:    -DDESKTOP_APP_DISABLE_WAYLAND_INTEGRATION:BOOL=OFF
BuildOption:    -DDESKTOP_APP_DISABLE_X11_INTEGRATION:BOOL=OFF

# Build tools
BuildRequires:  cmake
BuildRequires:  ninja
BuildRequires:  clang
BuildRequires:  gperf
BuildRequires:  python
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(appstream-glib)
BuildRequires:  glib2.0-common
BuildRequires:  gobject-introspection

# Qt6
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
BuildRequires:  cmake(Qt6Sql)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  cmake(Qt6WaylandClient)
BuildRequires:  cmake(Qt6WaylandClientPrivate)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6WidgetsPrivate)
BuildRequires:  cmake(Qt6Xml)
BuildRequires:  cmake(KF6CoreAddons)

# C++ libraries (cmake config packages)
BuildRequires:  cmake(Microsoft.GSL)
BuildRequires:  cmake(absl)
BuildRequires:  cmake(ada)
BuildRequires:  cmake(fmt)
BuildRequires:  cmake(range-v3)
BuildRequires:  cmake(tg_owt)
BuildRequires:  cmake(tde2e)
BuildRequires:  cmake(tl-expected)
BuildRequires:  cmake(VulkanHeaders)

# Packages that must be named explicitly (virtual names resolve wrongly)
BuildRequires:  lib64boost-devel
BuildRequires:  lib64dispatch-devel
BuildRequires:  lib64openal-devel
BuildRequires:  lib64z-ng-static-devel
BuildRequires:  lib64qrcodegencpp-devel
BuildRequires:  lib64gio-gir2.0
BuildRequires:  lib64glib-gir2.0
BuildRequires:  lib64lz4-static-devel
BuildRequires:  qt6-qtbase-theme-gtk3
BuildRequires:  tdlib-static

# pkgconfig
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(fribidi)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(glibmm-2.68)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(hunspell)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavfilter)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libcmark-gfm)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libfido2)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libsrtp2)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  pkgconfig(libyuv)
BuildRequires:  pkgconfig(minizip)
BuildRequires:  pkgconfig(openh264)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  pkgconfig(protobuf-lite)
BuildRequires:  pkgconfig(rnnoise)
BuildRequires:  pkgconfig(tlottie)
BuildRequires:  pkgconfig(vpx)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-keysyms)
BuildRequires:  pkgconfig(xcb-record)
BuildRequires:  pkgconfig(xcb-screensaver)
BuildRequires:  pkgconfig(zlib)

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
mkdir -p %{shimdir}/third_party/libyuv/include
echo '#include <libyuv.h>' > %{shimdir}/third_party/libyuv/include/libyuv.h

%files
%license LICENSE LEGAL
%doc README.md changelog.txt
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/*.service
%{_datadir}/icons/hicolor/*/apps/*
%{_metainfodir}/*.metainfo.xml
