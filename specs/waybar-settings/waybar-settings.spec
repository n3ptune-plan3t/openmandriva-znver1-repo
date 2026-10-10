Name:           waybar-settings
Summary:        Qt6 GUI settings manager for Waybar
Version:        0.1
Release:        1
License:        GPL-3.0-or-later
Group:          Graphical desktop/Other
URL:            https://github.com/n3ptune-plan3t/waybar-settings
Source0:        https://github.com/n3ptune-plan3t/waybar-settings/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildSystem:    cmake

BuildRequires:  cmake
BuildRequires:  cmake(Qt6Widgets)

Requires:       waybar
Recommends:     procps-ng

%description
A small Qt6 Widgets application to edit Waybar (0.15) configuration:
bar options, module layout (drag and drop), per-module options and an
optional managed style.css block. Unknown config keys are preserved, a
backup is kept, and Waybar can be reloaded with SIGUSR2 from the GUI.

%files
%{_bindir}/waybar-settings
