%global optflags %{optflags} -O2

%ifarch %{armx}
%bcond_without opengles
%bcond_without sdl
%else
%bcond_without opengles
%bcond_without sdl
%endif

%bcond_without wayland


%define _disable_ld_no_undefined 1
%define gstapi 1.0
%define major 1

%define libname %mklibname %{name} %major
%define devname %mklibname %{name} -d

%define shortver 1.25

Summary:	Enlightenment Foundation Libraries
Name:		efl
Version:	1.28.1
Release:	7
License:	BSD
Group:		Graphical desktop/Enlightenment
Url:		https://www.enlightenment.org/
Source0:	http://download.enlightenment.org/rel/libs/efl/%{name}-%{version}.tar.xz
Source1:	%{name}.rpmlintrc
Patch0:		fix_edje_cc_compile_failure.patch
# From Fedora # Build ecore_sdl versioned so. So efl no longer requires efl-devel
Patch1:		efl-1.27.0-sdl-version-build.patch

BuildRequires: meson
BuildRequires: doxygen
BuildRequires: gstreamer%{gstapi}-tools
BuildRequires: gettext-devel
BuildRequires: giflib-devel
BuildRequires: jpeg-devel
BuildRequires: libraw-devel
BuildRequires: psiconv-devel
BuildRequires: egl-devel
BuildRequires: pkgconfig(libavif)
BuildRequires: pkgconfig(avahi-core)
BuildRequires: pkgconfig(avahi-client)
BuildRequires: pkgconfig(bullet)
BuildRequires: pkgconfig(cairo)
BuildRequires: pkgconfig(check)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(fribidi)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(glu)
BuildRequires: pkgconfig(gstreamer-%{gstapi})
BuildRequires: pkgconfig(gstreamer-plugins-base-%{gstapi})
BuildRequires: pkgconfig(gstreamer-video-%{gstapi})
BuildRequires: pkgconfig(ibus-1.0)
BuildRequires: pkgconfig(ice)
BuildRequires: pkgconfig(libcares)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(libtiff-4)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(libwebp)
BuildRequires: pkgconfig(libxine)
BuildRequires: pkgconfig(libjxl)
BuildRequires: pkgconfig(mount)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(libopenjp2)
BuildRequires: pkgconfig(liblz4)
BuildRequires: pkgconfig(scim)
%if %{with sdl}
BuildRequires: pkgconfig(sdl2)
%endif
BuildRequires: pkgconfig(sndfile)
BuildRequires: pkgconfig(systemd)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xcb)
BuildRequires: pkgconfig(xcb-util)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xdamage)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xfixes)
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(xinerama)
BuildRequires: pkgconfig(xp)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(xpm)
BuildRequires: pkgconfig(xscrnsaver)
BuildRequires: pkgconfig(xtst)
BuildRequires: pkgconfig(xkbcommon-x11)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(luajit)
# EFL require lua up to 5.2, while pkgconfig install currently 5.4.7, so lets use older one.
BuildRequires: lua5.2-devel
#BuildRequires: pkgconfig(lua)
BuildRequires: pkgconfig(rlottie)
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(harfbuzz)
BuildRequires: pkgconfig(poppler-cpp)
BuildRequires: pkgconfig(libspectre)
BuildRequires: pkgconfig(printproto)
BuildRequires: pkgconfig(librsvg-2.0)
BuildRequires: pkgconfig(libinput)
Buildrequires: pkgconfig(libudev)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: vlan-utils
%if %{with wayland}
BuildRequires: pkgconfig(wayland-server)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(wayland-scanner)
BuildRequires: wayland-protocols-devel
BuildRequires: pkgconfig(wayland-cursor)
BuildRequires: pkgconfig(wayland-egl)
BuildRequires: wayland-tools
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(glesv2)
BuildRequires: pkgconfig(libglvnd)
%endif

Requires:  %{libname} = %{EVRD}


%description
The Enlightenment Foundation Libraries are a collection of libraries
and tools upon which sophisticated graphical applications can be
built.  Included are a data structure library (Eina), a C-based object
engine (EO), a data storage library (EET), an object canvas (Evas),
and more.

#----------------------------------------------------------------------------

%files -f %{name}.lang
%doc AUTHORS COPYING
%{_bindir}/*
%{_datadir}/dbus-1
%{_datadir}/ecore
%{_datadir}/ecore_con/checkme
%{_datadir}/ecore_imf
%{_datadir}/ecore_x
%{_datadir}/edje
%{_datadir}/eeze
%{_datadir}/efreet
%{_datadir}/elua
%{_datadir}/embryo
%{_datadir}/emotion
%{_datadir}/eo
%{_datadir}/ethumb
%{_datadir}/ethumb_client
%{_datadir}/evas
%{_datadir}/gdb/auto-load/usr/lib/*
%{_datadir}/mime/packages/edje.xml
%{_datadir}/eolian
%{_datadir}/exactness
%dir %{_datadir}/elementary
%{_datadir}/elementary/config
%{_datadir}/elementary/edje_externals
%{_datadir}/elementary/images
%{_datadir}/elementary/objects
%{_datadir}/elementary/test*
%dir %{_datadir}/elementary/themes
%{_datadir}/elementary/themes/default.edj
%{_datadir}/elementary/colors*
%{_datadir}/applications
%{_datadir}/mime/packages/evas.xml
%{_iconsdir}/Enlightenment-X
%{_iconsdir}/hicolor/128x128/apps/elementary.png
%{_libdir}/ecore*
%{_libdir}/edje
%{_libdir}/eeze
%{_libdir}/efreet
%{_libdir}/emotion
%{_libdir}/ethumb
%{_libdir}/ethumb_client
%{_libdir}/evas
%{_libdir}/elementary
%{_userunitdir}/*.service

#----------------------------------------------------------------------------

%package -n %{libname}
Summary: Libraries for the %{name} package
Group: System/Libraries

%description -n %{libname}
Libraries for %{name}.

%files -n %{libname}
%doc AUTHORS
%{_libdir}/*.so.%{major}
%{_libdir}/*.so.%{major}.*

#----------------------------------------------------------------------------
%package -n %{devname}
Summary: Headers and development libraries from %{name}
Group: Development/Other
Requires:  %{libname} = %{EVRD}
Requires:  %{name} = %{EVRD}
Provides:  %{name}-devel = %{EVRD}

%description -n %{devname}
%{name} development headers and libraries.

%files -n %{devname}
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/cmake/*

#----------------------------------------------------------------------------

%prep
%autosetup -p1

%build
# FIXME using native-arch-optimization on aarch64 seems to generate
# broken intrinsics, causing an error at link time
%meson \
       -Dxinput22=true \
       -Dsystemd=true \
       -Dharfbuzz=true \
       -Dglib=true \
       -Dsdl=true \
       -Decore-imf-loaders-disabler='ibus,scim' \
       -Devas-loaders-disabler='json,heif' \
       -Dfb=true \
       -Dwl=true \
       -Ddrm=true \
       -Dopengl=es-egl \
       -Dinstall-eo-files=true \
       -Dx11=true \
       -Dbindings=cxx \
%ifarch %{aarch64}
	-Dnative-arch-optimization=false
%endif
#If we want wayland support then OpenGL full need to be disabled, we need to use gles.
#       -Dopengl=full

%meson_build

%install

%meson_install

%find_lang %{name}
