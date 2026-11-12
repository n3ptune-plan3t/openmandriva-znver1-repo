Name:           python-inotify-simple
Version:        2.0.1
Release:        1
Summary:        Simple Python wrapper around inotify
License:        BSD-2-Clause
Group:          Development/Python
URL:            https://github.com/chrisjbillington/inotify_simple
Source0:        https://files.pythonhosted.org/packages/source/i/inotify_simple/inotify_simple-%{version}.tar.gz
BuildArch:      noarch
BuildSystem:    python

BuildRequires:  pkgconfig(python)
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(wheel)

%description
A simple ctypes wrapper around Linux inotify.

%files
%license LICENSE
%doc README.md
%{python_sitelib}/inotify_simple.py
%{python_sitelib}/__pycache__/inotify_simple*
%{python_sitelib}/inotify_simple-%{version}.dist-info/
