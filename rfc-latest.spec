#
# Conditional build:
# _with_ps
# _without_pdf
# _without_html_index
#
%include	/usr/lib/rpm/macros.perl
Summary:	Latest RFC documents
Summary(pl):	Najnowsze dokumenty RFC
Name:		rfc-latest
Version:	3541
%define		rfcindex_version	1.2
Release:	1
License:	distributable
Group:		Documentation
Source0:	ftp://ftp.isi.edu/in-notes/tar/RFCs3501-latest.tar.gz
# Source0-md5:	db47a7ca02ace83dfb01ade5ade26d46
Source1:	ftp://ftp.isi.edu/in-notes/rfc-index.txt
# Source1-md5:	d339353ffc6fef7d9a8485a08028d0b3
Source10:	http://www.kernighan.demon.co.uk/software/rfcindex-%{rfcindex_version}
# Source10-md5:	2b35cdd18096517e048fd455364dd77a
Patch0:		rfc-index-typo.patch
Patch10:	rfcindex-pld.patch
URL:		http://www.rfc.net/
%if %{!?_with_ps:%{!?_without_pdf:1}0}%{?_with_ps:1}
BuildRequires:	enscript
BuildRequires:	ghostscript
%endif
BuildRequires:	perl-devel
%if %{!?_without_html_index:1}0
BuildRequires:	rpm-perlprov
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RFC (Request For Comments) documents are actual and suggested Internet
standards.

%description -l pl
Dokumenty RFC (Request For Comments) zawieraj± opis obowi±zuj±cych i
proponowanych standardów internetowych.

%package -n rfc-index
Summary:	Index for RFC documents
Summary(pl):	Indeks dokumentów RFC
Group:		Documentation

%description -n rfc-index
Index file for RFC (Request For Comments) documents containing info
about document title, authors, status, size, etc.

%description -n rfc-index -l pl
Plik indeksowy dokumentów RFC (Request For Comments) zawieraj±cy
informacje takie, jak: tytu³, autorzy, status, rozmiar itp. dla
poszczególnych dokumentów.

%if %{!?_without_html_index:1}%{?_without_html_index:0}
%package -n rfc-index-html
Summary:	HTML-ized index of RFC documents
Summary(pl):	Indeks dokumentów RFC w HTML-u
Group:		Documentation
Requires:	%{name}-text >= %{version}-%{release}

%description -n rfc-index-html
Index file for RFC (Request For Comments) documents containing info
about document title, authors, status, size, etc.

%description -n rfc-index-html -l pl
Plik indeksowy dokumentów RFC (Request For Comments) zawieraj±cy
informacje takie, jak: tytu³, autorzy, status, rozmiar itp. dla
poszczególnych dokumentów.

%package -n rfcindex
Summary:	Script to generate HTML-ized index of RFC documents
Summary(pl):	Indeks dokumentów RFC
Group:		Utilities
Requires:	rfc-index

%description -n rfcindex
Perl script that reads the plain rfc-index.txt and outputs an HTML
index file with hyperlinks to appropriate RFCs.

%description -n rfcindex -l pl
Skrypt w perlu generujacy na podstawie tekstowego pliku rfc-index.txt
indeks w HTML-u zawieraj±cy przekierowania do odpowiednich dokumentów
RFC.
%endif

%package	text
Summary:	RFC documents - pure text version
Summary(pl):	Wersja czysto tekstowa dokumentów RFC
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

%description text -l pl
Wersja tekstowa dokumentów RFC (Request For Comments). Zbiór jest
niepe³ny, gdy¿ niektóre dokumenty s± dostêpne wy³±cznie w postaci
postscriptowej i PDF.

%if %{!?_with_ps:0}%{?_with_ps:1}
%package	ps
Summary:	RFC documents - PostScript version
Summary(pl):	Wersja postscriptowa dokumentów RFC
Group:		Documentation
Requires:	rfc-index >= %{version}
# common dirs 
Requires:	rfc-ps

%description ps
PostScript version of RFC (Request For Comments) documents.

%description ps -l pl
Wersja postscriptowa dokumentów RFC (Request For Comments).
%endif

%if %{!?_without_pdf:1}%{?_without_pdf:0}
%package	pdf
Summary:	RFC documents - pdf version
Summary(pl):	Wersja postscriptowa dokumentów RFC
Group:		Documentation
Requires:	rfc-index >= %{version}
# common dirs 
Requires:	rfc-pdf

%description pdf
RFC (Request For Comments) documents in Adobe PDF format.

%description pdf -l pl
Dokumenty RFC (Request For Comments) w formacie Adobe PDF.
%endif

%prep
%setup -q -c
install %{SOURCE1} .
%patch0 -p0

%if %{!?_without_html_index:1}%{?_without_html_index:0}
install %{SOURCE10} rfcindex
%patch10 -p0
%endif

%build
# Generate .ps and .pdf versions when they are not provided
%if %{!?_with_ps:%{!?_without_pdf:1}%{?_without_pdf:0}}%{?_with_ps:1}
for i in rfc[1-9]*.txt ; do
	BASE=`echo $i | sed "s/.txt$//"`
	PSFILE=$BASE.ps
	if [ ! -e $BASE.ps ] ; then
		# avoid stopping on errors ; .ps file may be correct
		# even after processing problems
		enscript --margin=54 -B  -fCourier11 -p $BASE.ps $i 2>/dev/null || :
	fi
%endif
%if %{!?_without_pdf:1}%{?_without_pdf:0}
	if [ ! -e $BASE.pdf ] ; then
		ps2pdf $BASE.ps $BASE.pdf 2>/dev/null
	fi
%endif
%if %{!?_with_ps:%{!?_without_pdf:1}%{?_without_pdf:0}}%{?_with_ps:1}
done
%endif

%if %{!?_without_html_index:1}%{?_without_html_index:0}
./rfcindex --gzip --by100 --nodate --nocredit \
	--base="file://%{_defaultdocdir}/RFC/" rfc-index.txt >rfc-index.html
pod2man rfcindex > rfcindex.1
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text/3{5,6}00
install -d $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/pdf/3{5,6}00
install -d $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/postscript/3{5,6}00

install rfc-index.txt $RPM_BUILD_ROOT%{_defaultdocdir}/RFC

%if %{!?_without_html_index:1}%{?_without_html_index:0}
install rfc-index.html      $RPM_BUILD_ROOT%{_defaultdocdir}/RFC
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}
install rfcindex $RPM_BUILD_ROOT%{_bindir}/rfcindex
install rfcindex.1 $RPM_BUILD_ROOT%{_mandir}/man1
%endif

find . -name 'rfc[1-9]*.txt' -print | xargs gzip -9
%if %{!?_with_ps:0}%{?_with_ps:1}
find . -name 'rfc[1-9]*.ps'  -print | xargs gzip -9
%endif

# install rfc[1-9]*.txt* $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text
for i in 35; do
	install rfc`echo $i|sed s/^0\*//g`[0-9][0-9][a.]*txt* \
		$RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text/${i}00
done

# install rfc*.pdf       $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/pdf
%if %{!?_without_pdf:1}%{?_without_pdf:0}
for i in 35; do
	install rfc`echo $i|sed s/^0\*//g`[0-9][0-9][a.-]*pdf \
		$RPM_BUILD_ROOT%{_defaultdocdir}/RFC/pdf/${i}00
done
%endif

%if %{!?_with_ps:0}%{?_with_ps:1}
# install rfc*.ps        $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/postscript
for i in 35; do
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

%if %{!?_with_ps:0}%{?_with_ps:1}
%files ps
%defattr(644,root,root,755)
%{_defaultdocdir}/RFC/postscript/*
%endif

%if %{!?_without_pdf:1}%{?_without_pdf:0}
%files pdf
%defattr(644,root,root,755)
%{_defaultdocdir}/RFC/pdf/*
%endif

%if %{!?_without_html_index:1}%{?_without_html_index:0}
%files -n rfc-index-html
%defattr(644,root,root,755)
%{_defaultdocdir}/RFC/rfc-index.html

%files -n rfcindex
%defattr(644,root,root,755)
%{_bindir}/rfcindex
%{_mandir}/man1/*
%endif
