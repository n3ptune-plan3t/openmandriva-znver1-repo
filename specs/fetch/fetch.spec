Name:           fetch
Summary:        Animated 3D system info fetch tool for the terminal
Version:        2.3.0
Release:        1
License:        ISC
Group:          Monitoring
URL:            https://github.com/areofyl/fetch
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  make

%description
A donut.c-inspired fetch tool that spins your distro logo in 3D with
live-updating system info. It turns each character of an ASCII/Unicode logo
into a point cloud and renders it as a rotating 3D relief with Blinn-Phong
shading. System info is gathered natively from /proc, /sys and GTK config,
with no dependencies beyond libm.

%prep
%autosetup -p1

%build
%set_build_flags
%make_build \
	CC="%{__cc}" \
	CFLAGS="%{optflags}" \
	LDFLAGS="%{build_ldflags}"

%install
%make_install PREFIX=%{_prefix}

%files
%license LICENSE
%doc README.md docs/*.md
%{_bindir}/fetch
