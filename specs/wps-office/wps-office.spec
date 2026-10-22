%global wpsver 12.1.2.29183
%global wpsrel %(echo %{wpsver} | awk -F. '{print $NF}')

# The WPS CDN only serves the personal Linux build through a time-limited signed URL:
# k = md5(secret + uri + unix-timestamp). Same scheme as the Arch/AUR wps-office-cn PKGBUILD
# (https://gitlab.com/cwittlut/wps-tsk/-/blob/main/tsk.sh by Ryan Tsien).
# Once the deb has been stored on file-store (abb store + .abf.yml) the URL is never refetched.
%global wpshost https://wps-linux-personal.wpscdn.cn
%global wpsuri /wps/download/ep/Linux2023/%{wpsrel}/wps-office_%{wpsver}.AK.preread.sw.Personal_806791_amd64.deb
%global wpsts  %(date +%%s)
%global wpskey 7f8faaaa468174dc1c9cd62e5f218a5b
%global wpssig %(echo -n "%{wpskey}%{wpsuri}%{wpsts}" | md5sum | cut -d' ' -f1)

Name:           wps-office
Version:        %{wpsver}
Release:        2
Summary:        Linux office suite with similar appearance to MS Office
Group:          Office

# The old Kingsoft WPS Community License has disappeared from the site.
# There is an EULA in the archive that we ship as the package license file, plus a non-downloadable EULA only reachable from inside the program.
License:        Custom (EULA)
URL:            https://www.wps.com/

# Upstream only distributes this as a prebuilt vendor package (a .deb as of 12.x), so we just repack it rather than compiling anything ourselves.
Source0:        %{wpshost}%{wpsuri}?t=%{wpsts}&k=%{wpssig}#/wps-office_%{version}_amd64.deb
Source1:        wps-office.rpmlintrc

ExclusiveArch:  %{x86_64}
BuildRequires:  binutils
BuildRequires:  tar
BuildRequires:  xz
BuildRequires:  hardlink

Requires:       libtiff.so.6()(64bit)
Requires:       ttf-wps-fonts
Recommends:     %{name}-mime = %{EVRD}

# Vendor package ships prebuilt, unusual/bundled sonames -- don't try to scan them for auto Requires/Provides
AutoReqProv:    no

# this is untouched vendor binary, skip find-debuginfo and stripping entirely.
%global debug_package %{nil}
%global __os_install_post %{nil}

Conflicts:      EternalTerminal

%description
WPS Office is an office suite whose interface closely mirrors Microsoft
Office, providing word processing, spreadsheet, and presentation
applications.

This package ships the English (en_US) user interface only.

%package mime
Summary:        MIME type definitions provided by WPS Office
Group:          Office
BuildArch:      noarch
Requires:       shared-mime-info

%description mime
MIME type definitions for WPS Office document formats, as shipped by Kingsoft.

%prep
# There's no tarball to unpack -- just create an empty build dir and extract the vendor deb's data payload into it ourselves.
%setup -q -c -T
echo "77ffbdc1be76c834e1853c27ff9063e49d5d3b1f30b206d785761b5bf560c83b  %{SOURCE0}" | sha256sum -c -
ar p %{SOURCE0} data.tar.xz | tar -xJ

%build
# Nothing to build; this is a prebuilt vendor binary package.

%check
# Prebuilt vendor binaries; there is no test suite to run.

%install
mkdir -p %{buildroot}
cp -a ./opt %{buildroot}/

# English UI only: drop the Simplified Chinese language pack (en_US and default stay)
rm -rf %{buildroot}/opt/kingsoft/wps-office/office6/mui/zh_CN

# Disable background services
chmod -x %{buildroot}/opt/kingsoft/wps-office/office6/wpsd || :
chmod -x %{buildroot}/opt/kingsoft/wps-office/office6/wpscloudsvr || :

# Vendor postinst/prerm scripts we don't want to ship
rm -rf %{buildroot}/opt/kingsoft/wps-office/INSTALL

# Qt4 rpc libs, bundled systemd/libdbus, bundled libstdc++ (breaks with icu>=71.1) and bundled libjpeg -- openmandriva already provides compatible versions of all of these.
rm -f %{buildroot}/opt/kingsoft/wps-office/office6/librpcetapi.so
rm -f %{buildroot}/opt/kingsoft/wps-office/office6/librpcwpsapi.so
rm -f %{buildroot}/opt/kingsoft/wps-office/office6/librpcwppapi.so
rm -f %{buildroot}/opt/kingsoft/wps-office/office6/libdbus-1.so*
rm -f %{buildroot}/opt/kingsoft/wps-office/office6/libstdc++.so*
rm -f %{buildroot}/opt/kingsoft/wps-office/office6/libjpeg.so*

# Plain config files that ship with a spurious executable bit, which makes rpmlint try (and fail) to parse them as shell scripts.
find %{buildroot}/opt/kingsoft/wps-office -type f \( -name '*.ini' -o -name '*.cfg' \) -exec chmod -x {} +

# The vendor ships dangling symlinks (office6/libbz2.so -> libbz2.so.1.0.4, which isn't in the payload); drop them.
find %{buildroot}/opt/kingsoft/wps-office -xtype l -delete

# The vendor payload ships many byte-identical files (per-locale strings, repeated icons, duplicated .so files) -- hardlink them to reclaim space.
hardlink -c %{buildroot} || :

# Launchers: the deb's /usr/bin wrappers already point at /opt/kingsoft/wps-office
mkdir -p %{buildroot}%{_bindir}
install -m755 usr/bin/* %{buildroot}%{_bindir}/

# Desktop entries, icons, fonts and MIME definitions from the deb
mkdir -p %{buildroot}%{_datadir}/applications
cp -a usr/share/applications/*.desktop %{buildroot}%{_datadir}/applications/

mkdir -p %{buildroot}%{_datadir}/icons
cp -a usr/share/icons/* %{buildroot}%{_datadir}/icons/

mkdir -p %{buildroot}%{_datadir}/fonts/wps-office
install -m644 usr/share/fonts/wps-office/* %{buildroot}%{_datadir}/fonts/wps-office/

mkdir -p %{buildroot}%{_datadir}/mime
cp -a usr/share/mime/* %{buildroot}%{_datadir}/mime/

# The vendor menu/desktop-directories (etc/xdg/menus, usr/share/desktop-directories) provide a non-working menu category -- not installed.

%post
update-desktop-database -q &> /dev/null || :

%postun
update-desktop-database -q &> /dev/null || :

%files
/opt/kingsoft/wps-office
%exclude /opt/kingsoft/wps-office/office6/mui/default/EULA_linux.html
%exclude /opt/kingsoft/wps-office/office6/mui/default/Privacy_Linux.html
%exclude /opt/kingsoft/wps-office/office6/thirdpartylegalnotices.txt
%license opt/kingsoft/wps-office/office6/mui/default/EULA_linux.html
%license opt/kingsoft/wps-office/office6/thirdpartylegalnotices.txt
%doc opt/kingsoft/wps-office/office6/mui/default/Privacy_Linux.html
%{_bindir}/et
%{_bindir}/misc
%{_bindir}/wpp
%{_bindir}/wps
%{_bindir}/wpspdf
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/fonts/wps-office

%files mime
%{_datadir}/mime/packages/*
