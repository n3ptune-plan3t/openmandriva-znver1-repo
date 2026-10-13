Name:           lazyvim
Version:        16.0.1
Release:        1
Summary:        Neovim setup powered by lazy.nvim
License:        Apache-2.0
URL:            https://github.com/LazyVim/LazyVim
Source0:        %{url}/archive/refs/tags/v%{version}/LazyVim-%{version}.tar.gz
BuildArch:      noarch

Requires:       neovim >= 0.11.2
Requires:       git
Recommends:     ripgrep
Recommends:     fd
Recommends:     lazygit
Recommends:     nodejs
Recommends:     gcc
Recommends:     make

%description
LazyVim is a Neovim setup powered by lazy.nvim to make it easy to
customize and extend your configuration. This package ships the LazyVim
distribution files under %{_datadir}/lazyvim; use the LazyVim starter
template (https://github.com/LazyVim/starter) as your ~/.config/nvim to
load it.

%prep
%autosetup -n LazyVim-%{version}

%build
# Pure Lua configuration files, nothing to compile

%install
install -d -m 0755 %{buildroot}%{_datadir}/lazyvim
cp -a init.lua lua doc queries scripts LICENSE NEWS.md %{buildroot}%{_datadir}/lazyvim/

%files
%license LICENSE
%doc README.md
%{_datadir}/lazyvim/
