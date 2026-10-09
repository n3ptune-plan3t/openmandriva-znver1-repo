%global debug_package %{nil}
%global __strip /bin/true
%global _build_id_links none
%global __os_install_post %{nil}
%global _binary_payload w19.zstdio

Name:           cloudflare-warp
Summary:        Cloudflare WARP client (binary repack of the upstream rpm)
Version:        2026.6.836.0
Release:        1
License:        Proprietary
Group:          Networking/Other
URL:            https://pkg.cloudflareclient.com/
# Fetch with: dnf download cloudflare-warp  (Fedora, after adding the Cloudflare repo)
# then: abb store cloudflare-warp-%{version}-1.x86_64.rpm
Source0:        https://pkg.cloudflareclient.com/rpm/cloudflare-warp-%{version}-1.x86_64.rpm

ExclusiveArch:  x86_64

BuildRequires:  rpm
BuildRequires:  cpio
BuildRequires:  systemd-rpm-macros

Requires:       dbus
Requires:       nftables
Requires:       nss
Requires:       ca-certificates

# Bundled/private binaries, don't leak provides
%global __provides_exclude_from ^%{_bindir}/.*$

%description
Cloudflare WARP client for Linux: warp-svc daemon and warp-cli command line
client, plus warp-taskbar tray app and warp-diag diagnostics.

This is a repack of Cloudflare's closed-source binary rpm; nothing is
compiled from source.

%prep
%setup -q -c -T
rpm2cpio %{SOURCE0} | cpio -idmu --quiet

%build
# nothing, binary package

%install
mkdir -p %{buildroot}%{_bindir}
install -m0755 bin/* %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_unitdir} %{buildroot}%{_userunitdir}
install -m0644 lib/systemd/system/*.service %{buildroot}%{_unitdir}/
install -m0644 lib/systemd/user/*.service   %{buildroot}%{_userunitdir}/

[ -d etc ]  && cp -a etc  %{buildroot}/
[ -d usr ]  && cp -a usr  %{buildroot}/

%post
%systemd_post warp-svc.service

%preun
%systemd_preun warp-svc.service

%postun
%systemd_postun_with_restart warp-svc.service

%files
%{_bindir}/warp-*
%{_unitdir}/warp-svc.service
%{_userunitdir}/warp-taskbar.service
%{_datadir}/applications/*arp*.desktop
%{_datadir}/icons/hicolor/*/apps/*arp*
%{_datadir}/doc/cloudflare-warp
%config(noreplace) %{_sysconfdir}/xdg/autostart/*arp*.desktop
