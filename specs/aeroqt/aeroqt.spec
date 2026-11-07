Name:           aeroqt
Version:        0.2.0
Release:        1
Summary:        Modular Qt6 widget style with a Frutiger Aero look
# UNRESOLVED: upstream has no LICENSE file; set this once the author adds one
License:        UNKNOWN
Group:          Graphical desktop/Other
URL:            https://github.com/n3ptune-plan3t/aeroqt
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildSystem:    cmake
BuildOption:    -DCMAKE_BUILD_TYPE=Release
BuildRequires:  cmake
BuildRequires:  ninja
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6WidgetsTools)
BuildRequires:  cmake(Qt6CoreTools)

%description
AeroQt is a from-scratch, modular Qt6 widget style plugin (QStyle) with a
Frutiger Aero default look and JSON themes (frutiger-aero, aero-lite,
flat-dark, win7-classic). It includes a widget gallery preview tool and an
environment script to make KDE apps use it.

%package qml
Summary:        AeroQt Qt Quick Controls 2 style for Kirigami/QML apps
Group:          Graphical desktop/Other
Requires:       %{name} = %{EVRD}
Requires:       qt6-qtdeclarative
BuildArch:      noarch

%description qml
QQC2 style module "AeroQt" so QML/Kirigami apps match the widget style.
Select it with QT_QUICK_CONTROLS_STYLE=AeroQt.

%check
export QT_QPA_PLATFORM=offscreen
%ctest

%files
%doc HANDOFF.md
%{_bindir}/aeroqt-preview
%{_qtdir}/plugins/styles/libaeroqt.so
%{_datadir}/aeroqt/aeroqt-env.sh

%files qml
%{_qtdir}/qml/AeroQt/
