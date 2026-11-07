Name:           aeroqt
Version:        0.2.0
Release:        1
Summary:        Frutiger Aero Qt6 widget style (and QQC2 style) for KDE
License:        MIT
Group:          Graphical desktop/KDE
URL:            https://github.com/n3ptune-plan3t/aeroqt
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  ninja
BuildRequires:  pkgconfig(Qt6Widgets)
BuildRequires:  lib64Qt6Widgets-devel

Requires:       lib64Qt6Widgets
Requires:       lib64Qt6QmlCore
Requires:       lib64Qt6QuickControls2
Requires:       lib64Qt6QuickTemplates2

BuildSystem:    cmake
BuildOption:    -DCMAKE_BUILD_TYPE=Release

%description
...

%files
%{_libdir}/qt6/plugins/styles/libaeroqt.so
%{_bindir}/aeroqt-preview
%{_libdir}/qt6/qml/QtQuick/Controls/AeroQt/
%{_datadir}/aeroqt/aeroqt-env.sh

%doc HANDOFF.md
