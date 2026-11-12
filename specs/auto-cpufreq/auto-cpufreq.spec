Name:           auto-cpufreq
Version:        3.2.0
Release:        1
Summary:        Automatic CPU speed and power optimizer
License:        GPL-3.0-or-later
Group:          System/Configuration
URL:            https://github.com/AdnanHodzic/auto-cpufreq
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildSystem:    python

BuildRequires:  pkgconfig(python)
BuildRequires:  python%{pyver}dist(pip)
BuildRequires:  python%{pyver}dist(wheel)
BuildRequires:  python%{pyver}dist(poetry-core)

Requires:       systemd
Recommends:     dmidecode

%description
auto-cpufreq monitors CPU load, temperature and battery state and
automatically adjusts the governor, turbo boost and power settings.
Runs as a systemd daemon. Config: /etc/auto-cpufreq.conf
(example in the documentation directory).

%package gtk
Summary:        GTK GUI for auto-cpufreq
Group:          System/Configuration
Requires:       %{name} = %{EVRD}
Requires:       typelib(Gtk) = 3.0
Requires:       python%{pyver}dist(pygobject)
Requires:       polkit

%description gtk
GTK graphical interface for auto-cpufreq.

%prep -a
# poetry-dynamic-versioning needs git metadata: use the static version
sed -i -e 's|^build-backend = .*|build-backend = "poetry.core.masonry.api"|' \
       -e 's|, *"poetry-dynamic-versioning[^"]*"||' pyproject.toml
# upstream pins inotify-simple exactly
sed -i 's|^inotify-simple = "2.0.1"|inotify-simple = ">=2.0.1"|' pyproject.toml

# state files: /opt/auto-cpufreq -> /var/lib/auto-cpufreq
sed -i -e 's|/opt/auto-cpufreq/override.pickle|%{_sharedstatedir}/auto-cpufreq/override.pickle|' \
       -e 's|/opt/auto-cpufreq/turbo-override.pickle|%{_sharedstatedir}/auto-cpufreq/turbo-override.pickle|' \
       -e 's|SOURCE_INSTALL_ROOT / "current/share/scripts"|Path("%{_datadir}/auto-cpufreq/scripts")|' \
       auto_cpufreq/core.py
# shared data: /opt/.../current/share -> /usr/share/auto-cpufreq
sed -i 's|/opt/auto-cpufreq/current/share|%{_datadir}/auto-cpufreq|g' \
       auto_cpufreq/gui/app.py auto_cpufreq/gui/objects.py \
       scripts/auto-cpufreq-install.sh scripts/auto-cpufreq-remove.sh
# /usr/local -> /usr
sed -i 's|/usr/local|%{_prefix}|g' \
       auto_cpufreq/core.py auto_cpufreq/gui/app.py auto_cpufreq/gui/objects.py \
       scripts/auto-cpufreq-install.sh scripts/auto-cpufreq-remove.sh

# systemd unit and polkit policy: no venv
sed -i -e '/^WorkingDirectory=/d' -e '/^Environment=PYTHONPATH=/d' \
       -e 's|^ExecStart=.*|ExecStart=%{_bindir}/auto-cpufreq --daemon|' \
       scripts/auto-cpufreq.service
sed -i 's|/opt/auto-cpufreq/current/venv/bin/auto-cpufreq|%{_bindir}/auto-cpufreq|' \
       scripts/org.auto-cpufreq.pkexec.policy

%install -a
install -Dm644 scripts/auto-cpufreq.service %{buildroot}%{_unitdir}/auto-cpufreq.service
install -Dm755 scripts/cpufreqctl.sh %{buildroot}%{_bindir}/cpufreqctl.auto-cpufreq
install -dm755 %{buildroot}%{_sharedstatedir}/auto-cpufreq

# helper scripts used by "auto-cpufreq --install/--remove"
install -Dm644 scripts/auto-cpufreq.service %{buildroot}%{_datadir}/auto-cpufreq/scripts/auto-cpufreq.service
install -Dm755 scripts/auto-cpufreq-install.sh %{buildroot}%{_datadir}/auto-cpufreq/scripts/auto-cpufreq-install.sh
install -Dm755 scripts/auto-cpufreq-remove.sh %{buildroot}%{_datadir}/auto-cpufreq/scripts/auto-cpufreq-remove.sh

# GUI
install -Dm644 scripts/style.css %{buildroot}%{_datadir}/auto-cpufreq/scripts/style.css
install -Dm644 images/icon.png %{buildroot}%{_datadir}/auto-cpufreq/images/icon.png
install -Dm644 images/icon.png %{buildroot}%{_iconsdir}/hicolor/512x512/apps/auto-cpufreq.png
install -Dm644 scripts/auto-cpufreq-gtk.desktop %{buildroot}%{_datadir}/applications/auto-cpufreq-gtk.desktop
install -Dm644 scripts/org.auto-cpufreq.pkexec.policy %{buildroot}%{_datadir}/polkit-1/actions/org.auto-cpufreq.pkexec.policy

%post
%systemd_post auto-cpufreq.service

%preun
%systemd_preun auto-cpufreq.service

%postun
%systemd_postun_with_restart auto-cpufreq.service

%files
%license LICENSE
%doc README.md auto-cpufreq.conf-example
%{_bindir}/auto-cpufreq
%{_bindir}/cpufreqctl.auto-cpufreq
%{_unitdir}/auto-cpufreq.service
%dir %{_sharedstatedir}/auto-cpufreq
%dir %{_datadir}/auto-cpufreq
%{_datadir}/auto-cpufreq/scripts/
%exclude %{_datadir}/auto-cpufreq/scripts/style.css
%{python_sitelib}/auto_cpufreq/
%{python_sitelib}/auto_cpufreq-%{version}.dist-info/
%exclude %{python_sitelib}/auto_cpufreq/gui/
%exclude %{python_sitelib}/auto_cpufreq/bin/auto_cpufreq_gtk.py
%exclude %{python_sitelib}/auto_cpufreq/bin/__pycache__/auto_cpufreq_gtk*

%files gtk
%{_bindir}/auto-cpufreq-gtk
%{python_sitelib}/auto_cpufreq/gui/
%{python_sitelib}/auto_cpufreq/bin/auto_cpufreq_gtk.py
%{python_sitelib}/auto_cpufreq/bin/__pycache__/auto_cpufreq_gtk*
%{_datadir}/auto-cpufreq/scripts/style.css
%{_datadir}/auto-cpufreq/images/
%{_iconsdir}/hicolor/512x512/apps/auto-cpufreq.png
%{_datadir}/applications/auto-cpufreq-gtk.desktop
%{_datadir}/polkit-1/actions/org.auto-cpufreq.pkexec.policy
