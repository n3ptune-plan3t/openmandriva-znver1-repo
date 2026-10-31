%global commit 55d2f5fd15f53cccbbb13388941b930442db1159

Name:           aerothemeplasma-sounds
Summary:        Collection of sound themes designed for AeroThemePlasma
Version:        6.6.4
Release:        1
License:        AGPL-3.0-or-later
Group:          Graphical desktop/KDE
URL:            https://gitgud.io/aeroshell/atp/aerothemeplasma-sounds
Source0:        https://gitgud.io/aeroshell/atp/%{name}/-/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildArch:      noarch
BuildSystem:    cmake
BuildRequires:  cmake(ECM)

%description
Collection of sound themes designed for AeroThemePlasma.

%prep
%autosetup -p1 -n %{name}-%{commit}

%files
%license LICENSE
%{_datadir}/sounds/*
