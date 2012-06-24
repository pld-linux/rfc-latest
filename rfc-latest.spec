#
# Conditional build:
%bcond_with	ps			# build package with RFCs in PostScript format too
%bcond_without	pdf		# don't build package with RFCs in PDF format
%bcond_without	html_index	# don't build HTML index

%include	/usr/lib/rpm/macros.perl
Summary:	Latest RFC documents
Summary(es):	Los �ltimos documentos RFC
Summary(pl):	Najnowsze dokumenty RFC
Name:		rfc-latest
Version:	4671
%define		rfcindex_version	1.2
Release:	1
License:	distributable
Group:		Documentation
Source0:	ftp://ftp.isi.edu/in-notes/tar/RFCs4501-latest.tar.gz
# Source0-md5:	5de875e7f40833e3f526a7498159c9b8
Source1:	ftp://ftp.isi.edu/in-notes/rfc-index.txt
Source10:	http://www.kernighan.demon.co.uk/software/rfcindex-%{rfcindex_version}
# Source10-md5:	2b35cdd18096517e048fd455364dd77a
Patch0:		rfc-index-typo.patch
Patch10:	rfcindex-pld.patch
URL:		http://www.rfc.net/
%if %{with ps} || %{with pdf}
BuildRequires:	enscript
BuildRequires:	ghostscript
%endif
BuildRequires:	perl-devel
%if %{with html_index}
BuildRequires:	rpm-perlprov
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RFC (Request For Comments) documents are actual and suggested Internet
standards.

%description -l es
Los documentos RFC (Request For Comments: petici�n de comentarios) son
los est�ndares actuales y sugeridos del Internet.

%description -l pl
Dokumenty RFC (Request For Comments) zawieraj� opis obowi�zuj�cych i
proponowanych standard�w internetowych.

%package -n rfc-index
Summary:	Index for RFC documents
Summary(es):	�ndice para los documentos RFC
Summary(pl):	Spis tre�ci dokument�w RFC
Group:		Documentation

%description -n rfc-index
Index file for RFC (Request For Comments) documents containing
information about document title, authors, status, size, etc.

%description -n rfc-index -l es
Fichero �ndice para los documentos RFC (Request For Comments: petici�n
de comentarios) que contiene informaciones sobre el t�tulo de
documento, su autores, estado, tama�o, etc.

%description -n rfc-index -l pl
Plik spisu tre�ci dokument�w RFC (Request For Comments) zawieraj�cy
informacje takie, jak: tytu�, autorzy, status, rozmiar itp. dla
poszczeg�lnych dokument�w.

%package -n rfc-index-html
Summary:	HTML-ized index of RFC documents
Summary(es):	�ndice de los documentos RFC en HTML
Summary(pl):	Spis tre�ci dokument�w RFC w HTML-u
Group:		Documentation
Requires:	%{name}-text >= %{version}-%{release}

%description -n rfc-index-html
Index file for RFC (Request For Comments) documents containing
information about document title, authors, status, size, etc.

%description -n rfc-index -l es
Fichero �ndice para los documentos RFC (Request For Comments: petici�n
de comentarios) que contiene informaciones sobre el t�tulo de
documento, su autores, estado, tama�o, etc.

%description -n rfc-index-html -l pl
Plik spisu tre�ci dokument�w RFC (Request For Comments) zawieraj�cy
informacje takie, jak: tytu�, autorzy, status, rozmiar itp. dla
poszczeg�lnych dokument�w.

%package -n rfcindex
Summary:	Script to generate HTML-ized index of RFC documents
Summary(es):	Script para generar un �ndice HTML de documentos RFC
Summary(pl):	Skrypt do generowania HTML-owego spisu tre�ci dokument�w RFC
Group:		Base/Utilities
Requires:	rfc-index

%description -n rfcindex
Perl script that reads the plain rfc-index.txt and outputs an HTML
index file with hyperlinks to appropriate RFCs.

%description -n rfcindex -l pl
Script de Perl que lee el plano rfc-index.txt y devuelve un fichero
�ndice en HTML con hiperenlaces a los RFC adecuados.

%description -n rfcindex -l pl
Skrypt w Perlu generujacy na podstawie tekstowego pliku rfc-index.txt
spis tre�ci w HTML-u zawieraj�cy przekierowania do odpowiednich
dokument�w RFC.

%package text
Summary:	RFC documents - pure text version
Summary(es):	Documentos RFC - versi�n de texto puro
Summary(pl):	Wersja czysto tekstowa dokument�w RFC
Group:		Documentation
Requires:	rfc-index >= %{version}
# common dirs
Requires:	rfc-text
#Provides:	%{name}-text-basic
#Obsoletes:	%{name}-text-basic

%description text
This is pure text version of RFC (Request For Comments) documents. The
set is incomplete. Some documents are available in PostScript and PDF
formats only.

%description text -l es
�sta es la versi�n de texto puro de los documentos RFC (Request For
Comments: petici�n de comentarios). Este conjunto es incompleto, ya
que algunos documentos son disponibles s�lo en los formatos PostScript
y PDF.

%description text -l pl
Wersja tekstowa dokument�w RFC (Request For Comments). Zbi�r jest
niepe�ny, gdy� niekt�re dokumenty s� dost�pne wy��cznie w postaci
postscriptowej i PDF.

%package ps
Summary:	RFC documents - PostScript version
Summary(es):	Documentos RFC - versi�n PostScript
Summary(pl):	Wersja postscriptowa dokument�w RFC
Group:		Documentation
Requires:	rfc-index >= %{version}
# common dirs
Requires:	rfc-ps

%description ps
PostScript version of RFC (Request For Comments) documents.

%description ps -l es
La versi�n PostScript de los documentos RFC (Request For Comments:
petici�n de comentarios).

%description ps -l pl
Wersja postscriptowa dokument�w RFC (Request For Comments).

%package pdf
Summary:	RFC documents - PDF version
Summary(es):	Documentos RFC - versi�n PDF
Summary(pl):	Wersja PDF dokument�w RFC
Group:		Documentation
Requires:	rfc-index >= %{version}
# common dirs
Requires:	rfc-pdf

%description pdf
RFC (Request For Comments) documents in Adobe PDF format.

%description pdf -l es
Documentos RFC (Request For Comments: petici�n de comentarios) en
formato Adobe PDF.

%description pdf -l pl
Dokumenty RFC (Request For Comments) w formacie Adobe PDF.

%prep
%setup -q -c
install %{SOURCE1} .
%patch0 -p0

%if %{with html_index}
install %{SOURCE10} rfcindex
%patch10 -p0
%endif

%build
# Generate .ps and .pdf versions when they are not provided
%if %{with ps} || %{with pdf}
for i in rfc[1-9]*.txt ; do
	BASE=`echo $i | sed "s/.txt$//"`
	PSFILE=$BASE.ps
	if [ ! -e $BASE.ps ] ; then
		# avoid stopping on errors ; .ps file may be correct
		# even after processing problems
		enscript --margin=54 -B -fCourier11 -p $BASE.ps $i 2>/dev/null || :
	fi
%endif
%if %{with pdf}
	if [ ! -e $BASE.pdf ] ; then
		ps2pdf $BASE.ps $BASE.pdf 2>/dev/null
	fi
%endif
%if %{with ps} || %{with pdf}
done
%endif

%if %{with html_index}
./rfcindex --gzip --by100 --nodate --nocredit \
	--base="file://%{_defaultdocdir}/RFC/" rfc-index.txt >rfc-index.html
pod2man rfcindex > rfcindex.1
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text/4{5,6}00
install -d $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/pdf/4{5,6}00
install -d $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/postscript/4{5,6}00

install rfc-index.txt $RPM_BUILD_ROOT%{_defaultdocdir}/RFC

%if %{with html_index}
install rfc-index.html $RPM_BUILD_ROOT%{_defaultdocdir}/RFC
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}
install rfcindex $RPM_BUILD_ROOT%{_bindir}/rfcindex
install rfcindex.1 $RPM_BUILD_ROOT%{_mandir}/man1
%endif

find . -name 'rfc[1-9]*.txt' -print | xargs gzip -9
%if %{with ps}
find . -name 'rfc[1-9]*.ps' -print | xargs gzip -9
%endif

# install rfc[1-9]*.txt* $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text
for i in 4{5,6}; do
	install rfc`echo $i|sed s/^0\*//g`[0-9][0-9][a.]*txt* \
		$RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text/${i}00
done

%if %{with pdf}
# install rfc*.pdf $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/pdf
for i in 4{5,6}; do
	install rfc`echo $i|sed s/^0\*//g`[0-9][0-9][a.-]*pdf \
		$RPM_BUILD_ROOT%{_defaultdocdir}/RFC/pdf/${i}00
done
%endif

%if %{with ps}
# install rfc*.ps $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/postscript
for i in 4{5,6}; do
	install rfc`echo $i|sed s/^0\*//g`[0-9][0-9][a.-]*ps* \
		$RPM_BUILD_ROOT%{_defaultdocdir}/RFC/postscript/${i}00
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files text
%defattr(644,root,root,755)
%{_defaultdocdir}/RFC/text/[0-9]*

%files -n rfc-index
%defattr(644,root,root,755)
%dir %{_defaultdocdir}/RFC
%{_defaultdocdir}/RFC/rfc-index.txt

%if %{with ps}
%files ps
%defattr(644,root,root,755)
%{_defaultdocdir}/RFC/postscript/*
%endif

%if %{with pdf}
%files pdf
%defattr(644,root,root,755)
%{_defaultdocdir}/RFC/pdf/*
%endif

%if %{with html_index}
%files -n rfc-index-html
%defattr(644,root,root,755)
%{_defaultdocdir}/RFC/rfc-index.html

%files -n rfcindex
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rfcindex
%{_mandir}/man1/*
%endif
