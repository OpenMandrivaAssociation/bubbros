Name:           bubbros
Version:        1.6
Release:        3
Summary:        Bub and Brothers game inspired by the classic Bubble and Bobble
Group:          Games/Arcade
License:        MIT and Artistic 2.0
#               Code under MIT
#               Sound and Graphics under Artistic 2.0, as released by Sebastian Wegner, in an email on 28/09/2009.
URL:            http://bub-n-bros.sourceforge.net/
Source0:        http://downloads.sourceforge.net/bub-n-bros/%{name}-%{version}.tar.bz2
Source1:        bubbros.desktop
Source2:        bubbros-client.sh
Source3:        bubbros-server.sh
Source4:        bubbros.sh
Source5:        bubbros-license-Artistic2.0.txt
Patch0:         bubbros-1.5-fixes.patch
BuildRequires:  python-devel imagemagick desktop-file-utils  
BuildRequires:  java-sdk
BuildRequires:  x11-proto-devel
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
Requires:       pygame pygtk2 hicolor-icon-theme
# htmlview

%description
This is a direct clone of the MacOS game Bub & Bob of McSebi. Thanks Sebi for
all the cool graphics and sounds!

Features:

    * 1 to 10 players -- the best fun is with at least 3 players!
    * Same gameplay as the famous McSebi's Bub & Bob.
    * Over-the-network game and/or up to 3 players on the same computer.
    * Completely original crazy bonuses!
    * Capture other players in a bubble!
    * New levels, including a random level generator!


%prep
%setup -q
#no backups for this patch, otherwise they end up getting installed!
%patch0 -p1
sed -i 's:#! /usr/bin/env python:#!%{__python}:' BubBob.py bubbob/bb.py \
  display/Client.py
chmod +x display/Client.py
# for %doc
mv bubbob/levels/README.txt levels.txt
install -m 644 %{SOURCE5} artistic.txt

%build
make %{?_smp_mflags}
pushd bubbob/images
python buildcolors.py
popd
pushd java
rm *.class
make
popd
convert bubbob/images/dragon_0.ppm -transparent '#010101' -crop 32x32+0+0 \
  %{name}.png


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_libdir}/%{name}
mkdir -p %{buildroot}%{_mandir}/man6
# copying the complete dirs and then removing the unwanted bits is easier :)
cp -a BubBob.py bubbob common display http2 java metaserver \
  %{buildroot}%{_datadir}/%{name}
rm -fr %{buildroot}%{_datadir}/%{name}/bubbob/build
rm -fr %{buildroot}%{_datadir}/%{name}/bubbob/doc
rm -fr %{buildroot}%{_datadir}/%{name}/display/build
rm -fr %{buildroot}%{_datadir}/%{name}/display/windows
rm     %{buildroot}%{_datadir}/%{name}/display/*_windows.py
rm -fr %{buildroot}%{_datadir}/%{name}/http2/sf
rm     %{buildroot}%{_datadir}/%{name}/http2/header.png
rm     %{buildroot}%{_datadir}/%{name}/java/pclient.java
rm `find %{buildroot}%{_datadir}/%{name} -name '*.c'`
rm `find %{buildroot}%{_datadir}/%{name} -name 'Makefile'`
rm `find %{buildroot}%{_datadir}/%{name} -name 'setup.py'`
# put the .so files in %{libdir}
mv `find %{buildroot}%{_datadir}/%{name} -name '*.so'` \
  %{buildroot}%{_libdir}/%{name}
# create the symlinks in /usr/bin, these must be absolute links!
install -m 755 %{SOURCE2} %{buildroot}%{_bindir}/bubbros-client
install -m 755 %{SOURCE3} %{buildroot}%{_bindir}/bubbros-server
install -m 755 %{SOURCE4} %{buildroot}%{_bindir}/bubbros
# install the manpages
install -m 644 doc/BubBob.py.1 %{buildroot}%{_mandir}/man6/bubbros.6
install -m 644 doc/bb.py.1 %{buildroot}%{_mandir}/man6/bubbros-server.6
install -m 644 doc/Client.py.1 %{buildroot}%{_mandir}/man6/bubbros-client.6
# below is the desktop file and icon stuff.
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install --vendor dribble           \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE1}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
install -p -m 644 %{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/32x32/apps


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE.txt artistic.txt levels.txt
%{_bindir}/bubbros*
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/dribble-%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_mandir}/man6/bubbros*.6.*




%changelog
* Sat Nov 06 2010 Funda Wang <fwang@mandriva.org> 1.6-1mdv2011.0
+ Revision: 594207
- update fil elist

* Tue Sep 29 2009 Glen Ogilvie <nelg@mandriva.org> 1.6-1mdv2010.0
+ Revision: 450814
- New game, under MIT and Artistic 2.0 license


* Wed Jun 10 2009 Glen Ogilvie <nelg@mandriva.org> 1.6-1mdv2010.0
- Reworked spec file for inclusion in Mandriva.

* Thu Jul 24 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.6-2
- Release bump for rpmfusion

* Mon Sep 10 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.6-1
- New upstream release 1.6

* Mon Jan 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.5-3
- Rebuild (with compile and run fixes) for new python2.5

* Tue Aug  1 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.5-2
- Add missing BuildRequires: libX11-devel libXext-devel xorg-x11-proto-devel
- Add Requires: htmlview
- Recompile java code instead of using precompiled .class files
- Don't install java source code, only class files

* Fri Jul 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.5-1
- initial Dribble package
