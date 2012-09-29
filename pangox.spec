# $Revision: 1.236 $, $Date: 2012/06/11 14:39:51 $
# NOTE: this package provides libpangox (relying on newer libpango) for old applications
#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	System for layout and rendering of internationalized text - X11 backend
Summary(pl.UTF-8):	System renderowania międzynarodowego tekstu - backend X11
Name:		pangox
Version:	1.30.1
Release:	1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/pango/1.30/pango-%{version}.tar.xz
# Source0-md5:	ec3c1f236ee9bd4a982a5f46fcaff7b9
Patch0:		pango-xfonts.patch
Patch1:		pango-arch_confdir.patch
Patch2:		pango-xonly.patch
URL:		http://www.pango.org/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake >= 1:1.9
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	gobject-introspection-devel >= 0.9.5
BuildRequires:	gtk-doc-automake >= 1.8
BuildRequires:	libtool >= 2:1.5
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	python-modules
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires:	glib2 >= 1:2.32.0
Requires:	pango >= 1:%{version}
Obsoletes:	libpango24
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if "%{_lib}" != "lib"
%define		libext		%(lib="%{_lib}"; echo ${lib#lib})
%define		_sysconfdir	/etc/pango%{libext}
%define		pqext		-%{libext}
%else
%define		_sysconfdir	/etc/pango
%define		pqext		%{nil}
%endif

%description
System for layout and rendering of internationalized text - X11
backend.

%description -l pl.UTF-8
System obsługi i renderowania międzynarodowego tekstu - backend X11.

%package devel
Summary:	Development files for Pango X11 backend library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki backendu Pango X11
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.32.0
Requires:	pango >= 1:%{version}
Requires:	xorg-lib-libX11-devel
Obsoletes:	libpango24-devel

%description devel
Development files for Pango X11 backend library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki backendu Pango X11.

%package static
Summary:	Static Pango X11 backend library
Summary(pl.UTF-8):	Statyczna biblioteka backendu Pango X11
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Conflicts:	pango-static < 1:1.32

%description static
Static Pango X11 backend library.

%description static -l pl.UTF-8
Statyczna biblioteka backendu Pango X11.

%prep
%setup -q -n pango-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-debug=%{?debug:yes}%{!?debug:minimum} \
	--disable-gtk-doc \
	--enable-man \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--with-html-dir=%{_gtkdocdir} \
	--with-included-modules=basic-x

# some generator script requires access to newely created .pc files
export PKG_CONFIG_PATH="$PWD"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# provided by main pango
%{__rm} $RPM_BUILD_ROOT%{_bindir}/pango-{querymodules,view} \
	$RPM_BUILD_ROOT%{_mandir}/man1/pango-{querymodules,view}.1
%{__rm}	$RPM_BUILD_ROOT%{_libdir}/libpango-1.0.* \
	$RPM_BUILD_ROOT%{_libdir}/girepository-1.0/Pango-1.0.typelib \
	$RPM_BUILD_ROOT%{_includedir}/pango-1.0/pango/{pango,pango-*}.h \
	$RPM_BUILD_ROOT%{_datadir}/gir-1.0/Pango-1.0.gir \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/pango.pc
%{__rm}	$RPM_BUILD_ROOT%{_libdir}/pango/1.6.0/modules/pango-{arabic,indic}-lang.*
%{__rm} -rf $RPM_BUILD_ROOT%{_gtkdocdir}/pango

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README THANKS
%attr(755,root,root) %{_libdir}/libpangox-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpangox-1.0.so.0
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pangox.aliases

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpangox-1.0.so
%{_libdir}/libpangox-1.0.la
%{_pkgconfigdir}/pangox.pc
%{_includedir}/pango-1.0/pango/pangox.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libpangox-1.0.a
%endif
