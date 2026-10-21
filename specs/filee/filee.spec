%global _enable_debug_packages %{nil}
%global debug_package %{nil}
# Everything under %{_libdir}/filee is a private .NET app directory (managed
# assemblies + bundled native libs from NuGet: SkiaSharp, HarfBuzz, libuiohook).
# Don't let rpm advertise or auto-require those private .so files.
%global __provides_exclude_from ^%{_libdir}/%{name}/.*$
%global __requires_exclude ^lib(SkiaSharp|HarfBuzzSharp|uiohook|coreclr|clrjit|hostfxr|hostpolicy|System\\..*|mscordaccore|mscordbi).*\\.so.*$
%global __strip /bin/true
%ifarch aarch64
%global dotnet_rid linux-arm64
%else
%global dotnet_rid linux-x64
%endif

Name:		filee
Version:	2.0.0
Release:	1
Summary:	Drag-and-drop file converter with a donut menu at the cursor
License:	MIT
Group:		File tools
URL:		https://filee.sh
Source0:	https://github.com/KnifeLemon/Filee/archive/v%{version}/Filee-%{version}.tar.gz
# Offline NuGet package cache (see make-nuget-cache.sh); ABF builders have no
# network access, so `dotnet restore` has to be fed from this tarball.
Source1:	%{name}-%{version}-nuget-packages.tar.zst
Source2:	%{name}.desktop

ExclusiveArch:	%{x86_64} aarch64

BuildRequires:	dotnet-sdk >= 10.0
BuildRequires:	dotnet-targeting-pack >= 10.0
BuildRequires:	dotnet-apphost-pack >= 10.0
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(icu-uc)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)

Requires:	dotnet-runtime >= 10.0
Requires:	icu
Requires:	fontconfig
Requires:	freetype
Requires:	libx11
Requires:	libxtst
Requires:	libxt
Requires:	libice
Requires:	libsm
Requires:	libxrandr
Requires:	xkbcommon
# TODO: add a CJK font Recommends once the OM package name is confirmed
# (dnf search noto cjk) - upstream lists fonts-noto-cjk for Ubuntu.
# Optional conversion engines. Filee discovers them on PATH and can also
# download its own copies from Settings > Engines.
Recommends:	ffmpeg
Recommends:	pandoc
Recommends:	ghostscript
Recommends:	libreoffice
Recommends:	calibre
Recommends:	p7zip

%description
Filee is a free, open-source file converter driven by dragging: hold a key,
drag files and drop them on a format in the donut menu that opens at the
cursor. It converts images, PDF, Office documents, HWP, e-books, archives,
fonts, CAD, 3D models, geospatial data, audio, video and subtitles, entirely
offline, and writes the result next to the original.

It also ships a command line, `filee`, which converts files and watches
folders without the tray app.

Drag gestures need X11 (or XWayland). On a Wayland session use the drop zone
or the file manager's right-click menu.

This package is built without upstream's FileeRelease flag, so it never
registers Explorer/startup entries or replaces itself: updates come from the
distribution.

%prep
%autosetup -n Filee-%{version} -p1
# Offline NuGet cache
mkdir -p "%{_builddir}/nuget-packages"
tar -C "%{_builddir}/nuget-packages" --zstd -xf %{SOURCE1}

%build
export DOTNET_CLI_TELEMETRY_OPTOUT=1
export DOTNET_NOLOGO=1
export DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1
export DOTNET_CLI_HOME="%{_builddir}/dotnet-home"
export NUGET_PACKAGES="%{_builddir}/nuget-packages"
export HOME="%{_builddir}/dotnet-home"
# Don't try to reach nuget.org: only the vendored cache is allowed.
cat > nuget.config <<NUGETEOF
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <clear />
    <add key="local" value="%{_builddir}/nuget-packages" />
  </packageSources>
</configuration>
NUGETEOF

# Framework-dependent publish: the system dotnet runtime is used, only the
# RID-specific native assets of the NuGet packages are bundled.
# FileeRelease is intentionally NOT set (see description).
for p in Filee.App Filee.Cli; do
  dotnet publish src/$p/$p.csproj \
	-c Release \
	-r %{dotnet_rid} \
	--self-contained false \
	-p:Version=%{version} \
	-p:PublishReadyToRun=false \
	-p:DebugType=none \
	-p:DebugSymbols=false \
	--source "%{_builddir}/nuget-packages" \
	-o publish
done

%install
install -d %{buildroot}%{_libdir}/%{name}
cp -a publish/. %{buildroot}%{_libdir}/%{name}/
chmod 0755 %{buildroot}%{_libdir}/%{name}/Filee %{buildroot}%{_libdir}/%{name}/filee-cli
# No bundled debug symbols / pdb leftovers
find %{buildroot}%{_libdir}/%{name} -name '*.pdb' -delete

install -d %{buildroot}%{_bindir}
ln -s %{_libdir}/%{name}/filee-cli %{buildroot}%{_bindir}/filee
ln -s %{_libdir}/%{name}/Filee %{buildroot}%{_bindir}/filee-gui

# Icons
install -Dm0644 src/Filee.App/Assets/Icons/filee.svg \
	%{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
for s in 16 32 48 64 128 256 512; do
  install -d %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps
  magick src/Filee.App/Assets/Icons/filee.png -resize ${s}x${s} \
	%{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/%{name}.png
done

# Desktop entry
install -Dm0644 %{SOURCE2} %{buildroot}%{_datadir}/applications/%{name}.desktop

# KWin script for the experimental Wayland gesture support (Plasma 6 only)
install -d %{buildroot}%{_datadir}/%{name}
cp -a installer/linux/kwin %{buildroot}%{_datadir}/%{name}/

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license LICENSE THIRD-PARTY-NOTICES.md
%doc README.md CHANGELOG.md installer/linux/INSTALL.txt
%{_bindir}/filee
%{_bindir}/filee-gui
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/%{name}
