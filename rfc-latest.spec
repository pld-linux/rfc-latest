#
# Conditional build:
%bcond_with	ps			# build package with RFCs in PostScript format too
%bcond_without	pdf		# don't build package with RFCs in PDF format
%bcond_without	html_index	# don't build HTML index

%include	/usr/lib/rpm/macros.perl
%define		rfcindex_version	1.2
Summary:	Latest RFC documents
Summary(es.UTF-8):	Los últimos documentos RFC
Summary(pl.UTF-8):	Najnowsze dokumenty RFC
Name:		rfc-latest
Version:	5340
Release:	1
License:	distributable
Group:		Documentation
Source0:	ftp://ftp.rfc-editor.org/in-notes/tar/RFCs5001-latest.tar.gz
# Source0-md5:	555c9dd215bf68a4d606b5128877d850
Source1:	ftp://ftp.rfc-editor.org/in-notes/rfc-index.txt
Source2:	ftp://ftp.rfc-editor.org/in-notes/rfc5000.txt
Source10:	rfcindex-%{rfcindex_version}
# Source10-md5:	2b35cdd18096517e048fd455364dd77a
Patch0:		rfc-index-typo.patch
Patch1:		rfc-index-missing_rfcs.patch
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

%description -l es.UTF-8
Los documentos RFC (Request For Comments: petición de comentarios) son
los estándares actuales y sugeridos del Internet.

%description -l pl.UTF-8
Dokumenty RFC (Request For Comments) zawierają opis obowiązujących i
proponowanych standardów internetowych.

%package -n rfc-index
Summary:	Index for RFC documents
Summary(es.UTF-8):	Índice para los documentos RFC
Summary(pl.UTF-8):	Spis treści dokumentów RFC
Group:		Documentation

%description -n rfc-index
Index file for RFC (Request For Comments) documents containing
information about document title, authors, status, size, etc.

%description -n rfc-index -l es.UTF-8
Fichero índice para los documentos RFC (Request For Comments: petición
de comentarios) que contiene informaciones sobre el título de
documento, su autores, estado, tamaño, etc.

%description -n rfc-index -l pl.UTF-8
Plik spisu treści dokumentów RFC (Request For Comments) zawierający
informacje takie, jak: tytuł, autorzy, status, rozmiar itp. dla
poszczególnych dokumentów.

%package -n rfc-index-html
Summary:	HTML-ized index of RFC documents
Summary(es.UTF-8):	Índice de los documentos RFC en HTML
Summary(pl.UTF-8):	Spis treści dokumentów RFC w HTML-u
Group:		Documentation
Requires:	%{name}-text >= %{version}-%{release}

%description -n rfc-index-html
Index file for RFC (Request For Comments) documents containing
information about document title, authors, status, size, etc.

%description -n rfc-index -l es.UTF-8
Fichero índice para los documentos RFC (Request For Comments: petición
de comentarios) que contiene informaciones sobre el título de
documento, su autores, estado, tamaño, etc.

%description -n rfc-index-html -l pl.UTF-8
Plik spisu treści dokumentów RFC (Request For Comments) zawierający
informacje takie, jak: tytuł, autorzy, status, rozmiar itp. dla
poszczególnych dokumentów.

%package -n rfcindex
Summary:	Script to generate HTML-ized index of RFC documents
Summary(es.UTF-8):	Script para generar un índice HTML de documentos RFC
Summary(pl.UTF-8):	Skrypt do generowania HTML-owego spisu treści dokumentów RFC
Group:		Base/Utilities
Requires:	rfc-index

%description -n rfcindex
Perl script that reads the plain rfc-index.txt and outputs an HTML
index file with hyperlinks to appropriate RFCs.

%description -n rfcindex -l pl.UTF-8
Script de Perl que lee el plano rfc-index.txt y devuelve un fichero
índice en HTML con hiperenlaces a los RFC adecuados.

%description -n rfcindex -l pl.UTF-8
Skrypt w Perlu generujacy na podstawie tekstowego pliku rfc-index.txt
spis treści w HTML-u zawierający przekierowania do odpowiednich
dokumentów RFC.

%package text
Summary:	RFC documents - pure text version
Summary(es.UTF-8):	Documentos RFC - versión de texto puro
Summary(pl.UTF-8):	Wersja czysto tekstowa dokumentów RFC
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

%description text -l es.UTF-8
Ésta es la versión de texto puro de los documentos RFC (Request For
Comments: petición de comentarios). Este conjunto es incompleto, ya
que algunos documentos son disponibles sólo en los formatos PostScript
y PDF.

%description text -l pl.UTF-8
Wersja tekstowa dokumentów RFC (Request For Comments). Zbiór jest
niepełny, gdyż niektóre dokumenty są dostępne wyłącznie w postaci
postscriptowej i PDF.

%package ps
Summary:	RFC documents - PostScript version
Summary(es.UTF-8):	Documentos RFC - versión PostScript
Summary(pl.UTF-8):	Wersja postscriptowa dokumentów RFC
Group:		Documentation
Requires:	rfc-index >= %{version}
# common dirs
Requires:	rfc-ps

%description ps
PostScript version of RFC (Request For Comments) documents.

%description ps -l es.UTF-8
La versión PostScript de los documentos RFC (Request For Comments:
petición de comentarios).

%description ps -l pl.UTF-8
Wersja postscriptowa dokumentów RFC (Request For Comments).

%package pdf
Summary:	RFC documents - PDF version
Summary(es.UTF-8):	Documentos RFC - versión PDF
Summary(pl.UTF-8):	Wersja PDF dokumentów RFC
Group:		Documentation
Requires:	rfc-index >= %{version}
# common dirs
Requires:	rfc-pdf

%description pdf
RFC (Request For Comments) documents in Adobe PDF format.

%description pdf -l es.UTF-8
Documentos RFC (Request For Comments: petición de comentarios) en
formato Adobe PDF.

%description pdf -l pl.UTF-8
Dokumenty RFC (Request For Comments) w formacie Adobe PDF.

%prep
%setup -q -c
install %{SOURCE1} .
%patch0 -p0
%patch1 -p0
install %{SOURCE2} .

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
	--base="file://%{_docdir}/RFC/" rfc-index.txt >rfc-index.html
pod2man rfcindex > rfcindex.1
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_docdir}/RFC/text/5{0,1,2,3}00
install -d $RPM_BUILD_ROOT%{_docdir}/RFC/pdf/5{0,1,2,3}00
install -d $RPM_BUILD_ROOT%{_docdir}/RFC/postscript/5{0,1,2,3}00

install rfc-index.txt $RPM_BUILD_ROOT%{_docdir}/RFC

%if %{with html_index}
install rfc-index.html $RPM_BUILD_ROOT%{_docdir}/RFC
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}
install rfcindex $RPM_BUILD_ROOT%{_bindir}/rfcindex
install rfcindex.1 $RPM_BUILD_ROOT%{_mandir}/man1
%endif

find . -name 'rfc[1-9]*.txt' -print | xargs gzip -9
%if %{with ps}
find . -name 'rfc[1-9]*.ps' -print | xargs gzip -9
%endif

# install rfc[1-9]*.txt* $RPM_BUILD_ROOT%{_docdir}/RFC/text
for i in 5{0,1,2,3} ; do
	install rfc`echo $i|sed s/^0\*//g`[0-9][0-9][a.]*txt* \
		$RPM_BUILD_ROOT%{_docdir}/RFC/text/${i}00
done

%if %{with pdf}
# install rfc*.pdf $RPM_BUILD_ROOT%{_docdir}/RFC/pdf
for i in 5{0,1,2,3} ; do
	install rfc`echo $i|sed s/^0\*//g`[0-9][0-9][a.-]*pdf \
		$RPM_BUILD_ROOT%{_docdir}/RFC/pdf/${i}00
done
%endif

%if %{with ps}
# install rfc*.ps $RPM_BUILD_ROOT%{_docdir}/RFC/postscript
for i in 5{0,1,2,3} ; do
	install rfc`echo $i|sed s/^0\*//g`[0-9][0-9][a.-]*ps* \
		$RPM_BUILD_ROOT%{_docdir}/RFC/postscript/${i}00
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files text
%defattr(644,root,root,755)
%{_docdir}/RFC/text/[0-9]*

%files -n rfc-index
%defattr(644,root,root,755)
%dir %{_docdir}/RFC
%{_docdir}/RFC/rfc-index.txt

%if %{with ps}
%files ps
%defattr(644,root,root,755)
%{_docdir}/RFC/postscript/*
%endif

%if %{with pdf}
%files pdf
%defattr(644,root,root,755)
%{_docdir}/RFC/pdf/*
%endif

%if %{with html_index}
%files -n rfc-index-html
%defattr(644,root,root,755)
%{_docdir}/RFC/rfc-index.html

%files -n rfcindex
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rfcindex
%{_mandir}/man1/*
%endif
