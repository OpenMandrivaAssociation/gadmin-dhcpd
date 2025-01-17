Summary:	A GTK+ administation tool for the ISC DHCPD server
Name:		gadmin-dhcpd
Version:	0.5.2
Release:	2
License:	GPLv3+
Group:		System/Configuration/Networking
URL:		https://www.gadmintools.org/
Source0:	http://mange.dynalias.org/linux/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}.pam
BuildRequires:	gtk+2-devel
BuildRequires:	imagemagick
BuildRequires:  desktop-file-utils
Requires:	dhcp-server >= 3.0.1
Requires:	usermode-consoleonly
Obsoletes:	gdhcpd
Provides:	gdhcpd
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Gadmin-Dhcpd is a fast and easy to use GTK+ administration tool for the
ISC DHCPD server.

%prep
%setup -q

%build
%configure2_5x

perl -pi -e 's|^#define DHCPD_BINARY .*|#define DHCPD_BINARY \"%{_sbindir}/dhcpd\"|g' config.h
perl -pi -e 's|^#define DHCPD_CONF .*|#define DHCPD_CONF \"%{_sysconfdir}/dhcpd.conf\"|g' config.h
perl -pi -e 's|^#define LEASE_FILE .*|#define LEASE_FILE \"%{_localstatedir}/lib/dhcp/dhcpd.leases\"|g' config.h

%make

%install
rm -rf %{buildroot}

%makeinstall_std INSTALL_USER=`id -un` INSTALL_GROUP=`id -gn`

# pam auth
install -d %{buildroot}%{_sysconfdir}/pam.d/
install -d %{buildroot}%{_sysconfdir}/security/console.apps

install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{name}
install -m 644 etc/security/console.apps/%{name} %{buildroot}%{_sysconfdir}/security/console.apps/%{name}

# locales
%find_lang %{name}

# Icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert -geometry 48x48 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -geometry 32x32 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -geometry 16x16 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications
sed -i -e 's,%{name}.png,%{name},g' desktop/%{name}.desktop
sed -i -e 's,GADMIN-DHCPD,Gadmin-Dhcpd,g' desktop/%{name}.desktop
mv desktop/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-install --vendor="" \
    --remove-category="Application" \
    --add-category="Settings;Network;GTK;" \
    --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# Prepare usermode entry
mkdir -p %{buildroot}%{_bindir}
mv %{buildroot}%{_sbindir}/gadmin-dhcpd %{buildroot}%{_sbindir}/gadmin-dhcpd.real
ln -s %{_bindir}/consolehelper %{buildroot}%{_bindir}/gadmin-dhcpd

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name} <<_EOF_
USER=root
PROGRAM=%{_sbindir}/%{name}.real
SESSION=true
FALLBACK=false
_EOF_

rm -rf %{buildroot}%{_datadir}/doc/%{name}

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc COPYING AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%{_bindir}/%{name}
%{_sbindir}/%{name}.real
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*.png
%{_datadir}/pixmaps/%{name}/%{name}.png
%{_iconsdir}/hicolor/*/apps/%{name}.png



%changelog
* Sat Jan 29 2011 Funda Wang <fwang@mandriva.org> 0.5.2-1mdv2011.0
+ Revision: 633941
- update to new version 0.5.2
- update to new version 0.5.1

* Sun Jan 09 2011 Funda Wang <fwang@mandriva.org> 0.5.0-1mdv2011.0
+ Revision: 630685
- update to new version 0.5.0

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4.9-2mdv2011.0
+ Revision: 610786
- rebuild

* Sun Mar 28 2010 Funda Wang <fwang@mandriva.org> 0.4.9-1mdv2010.1
+ Revision: 528508
- update to new version 0.4.9
- use install_std

* Wed Mar 17 2010 Funda Wang <fwang@mandriva.org> 0.4.8-1mdv2010.1
+ Revision: 522777
- update to new version 0.4.8

* Thu Jan 07 2010 Emmanuel Andry <eandry@mandriva.org> 0.4.7-1mdv2010.1
+ Revision: 487287
- New version 0.4.7

* Fri Sep 11 2009 Emmanuel Andry <eandry@mandriva.org> 0.4.5-1mdv2010.0
+ Revision: 438452
- New version 0.4.5

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0.4.4-4mdv2010.0
+ Revision: 437613
- rebuild

* Sun Jan 04 2009 Adam Williamson <awilliamson@mandriva.org> 0.4.4-3mdv2009.1
+ Revision: 324138
- install consolehelper link to /usr/bin not /usr/sbin, so it works right
- don't use ALL CAPS in menu entry
- fd.o icons
- clean description a bit
- new license policy
- disable Werror (if I try and fix it, it crashes on startup)

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Tue Sep 09 2008 Emmanuel Andry <eandry@mandriva.org> 0.4.4-2mdv2009.0
+ Revision: 283232
- fix source0

* Tue Sep 09 2008 Emmanuel Andry <eandry@mandriva.org> 0.4.4-1mdv2009.0
+ Revision: 283071
- import gadmin-dhcpd


