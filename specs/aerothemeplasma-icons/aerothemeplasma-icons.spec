%global commit b8d5ce100251b74a3a3c5b4a474cb3ff8df11bba

Name:           aerothemeplasma-icons
Summary:        Icon theme designed for AeroThemePlasma
Version:        6.6.4
Release:        1
License:        AGPL-3.0-or-later
Group:          Graphical desktop/KDE
URL:            https://gitgud.io/aeroshell/atp/aerothemeplasma-icons
Source0:        https://gitgud.io/aeroshell/atp/%{name}/-/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildArch:      noarch
BuildSystem:    cmake
BuildRequires:  cmake(ECM)

%description
Icon theme designed for AeroThemePlasma.

%prep
%autosetup -p1 -n %{name}-%{commit}

%files
%license LICENSE
%{_datadir}/icons/*
