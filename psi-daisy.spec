# TODO: %lang() for *.qm files
%define _rev 20080417
Summary:	Psi-Daisy - Jabber client
Summary(pl.UTF-8):	Psi-Daisy - klient Jabbera
Name:		psi-daisy
Version:	0.12
Release:	0.6.%{_rev}.0
License:	GPL v2
Group:		Applications/Communications
Source0:	http://uaznia.net/psi-daisy/Psi-%{version}/psi-%{version}-daisy-%{_rev}-src.rar
# Source0-md5:	4c03f9ba109d1771e254305c9416d707
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
BuildRequires:	python-devel >= 2.3.0
BuildRequires:	qca-devel >= 2.0.0
BuildRequires:	qt4-build
BuildRequires:	qt4-linguist
BuildRequires:	qt4-qmake
BuildRequires:	unrar
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

psi-daisy is a private build made by Michał Jazłowiecki.

%description -l pl.UTF-8
Psi jest komunikatorem dla otwartego systemu wiadomości Jabber.
Został stworzony w oparciu o bibliotekę Qt. Psi obsługuje połączenia
szyfrowane SSL i TLS. W stosunku do domyślnego zachowania komunikatora
została wprowadzona zmiana, która powoduje że certyfikaty SSL są
poszukiwane w katalogu $DATADIR/certs lub ~/.psi/certs.

psi-daisy to prywatna modyfikacja Michała Jazłowieckiego.

%prep
%setup -q -T -c
unrar x %{SOURCE0}
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
        %{__make} || die "make plugin ${pl} failed"
	cd ..
done
cd ../../..

cd lang
lrelease-qt4 *.ts

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
