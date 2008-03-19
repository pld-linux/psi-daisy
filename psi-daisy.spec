%define _rev 20080223
Summary:	Psi-Daisy - Jabber client
Summary(pl.UTF-8):	Psi-Daisy - klient Jabbera
Name:		psi-daisy
Version:	0.12
Release:	0.6.%{_rev}.0
License:	GPL v2
Group:		Applications/Communications
Source0:	http://uaznia.net/psi-daisy/Psi-%{version}/psi-%{version}-daisy-%{_rev}-src.zip
# Source0-md5:	fec5db067396d1bc1781b1b0149e559b
Patch0:		%{name}-configure_fix.patch
URL:		http://psi-daisy.uaznia.net/
BuildRequires:	Qt3Support-devel
BuildRequires:	QtCore-devel
BuildRequires:	QtDBus-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtXml-devel
BuildRequires:	aspell-devel
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel >= 0.9.7c
BuildRequires:	qca-devel >= 2.0.0
BuildRequires:	qt4-build
BuildRequires:	qt4-qmake
#BuildRequires:	unrar
BuildRequires:	unzip
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-proto-scrnsaverproto-devel
BuildRequires:	zlib-devel
Requires:	qt4-plugin-qca-ossl
Provides:	psi
Obsoletes:	psi
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Psi is a communicator for the Jabber open messaging system. It is
based on the Qt library. It supports SSL and TLS encrypted connections. 
The default behaviour for SSL was changed so that it looks for SSL
certificates in $DATADIR/certs or in ~/.psi/certs.
This is a private build made by Michał Jazłowiecki.

%description -l pl.UTF-8
Psi jest komunikatorem dla otwartego systemu wiadomoĹci Jabber.
ZostaĹ stworzony w oparciu o bibliotekÄ Qt. Psi wspiera poĹÄczenia
szyfrowane SSL i TLS. W stosunku do domyĹlnego zachowania komunikatora
zostaĹa wprowadzona zmiana, ktĂłra powoduje Ĺźe certyfikaty SSL sÄ
poszukiwane w katalogu $DATADIR/certs lub ~/.psi/certs.
To prywatna modyfikacja Michała Jazłowieckiego.

%prep
%setup -q -c
%patch0 -p1
rm -rf third-party

%build
chmod +x ./configure
./configure \
	--prefix=%{_prefix} \
	--datadir=%{_datadir}

qmake-qt4
%{__make}

cd src/plugins/generic
for pl in chess echo noughtsandcrosses python null; do
        cd $pl
        qmake-qt4 ${pl}plugin.pro
        make || die "make plugin ${pl} failed"
	cd ..
done
cd ../../..

cd lang

lrelease *.ts

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/psi/plugins

export QTDIR=%{_libdir}/qt4

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

cp -f lang/*.qm $RPM_BUILD_ROOT%{_datadir}/psi/
for pl in chess echo noughtsandcrosses python null; do
    cp src/plugins/generic/${pl}/lib${pl}plugin.so $RPM_BUILD_ROOT%{_datadir}/psi/plugins
done;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc INSTALL README
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/psi
%{_datadir}/psi/*.qm
%{_datadir}/psi/certs
%{_datadir}/psi/iconsets
%{_datadir}/psi/sound
%{_datadir}/psi/plugins
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/*.png
