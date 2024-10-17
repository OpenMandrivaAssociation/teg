Summary:	Clone of a Risk clone
Name:		teg
Version:	0.11.2
Release:	%mkrel 7
URL:		https://teg.sourceforge.net/
License:	GPL
Group:		Games/Strategy
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source0:	%{name}-%{version}.tar.bz2
Patch0:		teg-0.11.2-remove-de-comment.patch
Obsoletes:	teg-gnome1
# 0.11.0-4mdk (Abel) I don't think providing teg-gnome1 is reasonable,
# but ... rpmlint
Provides:	teg-gnome1
BuildRequires:	GConf2
BuildRequires:	libgnomeui2-devel
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
Requires(post): GConf2
Requires(preun): GConf2

%description
Tenes Emapandas Graciela (TEG) is a clone of 'Plan Táctico y Estratégico
de la Guerra' (Tactical and Strategic plan of the War), which is a
pseudo-clone of Risk, a turn-based strategy game. Some rules are
different.

%prep
%setup -q
%patch0 -p0

%build
%configure2_5x --bindir=%{_gamesbindir}
%make

%install
rm -rf $RPM_BUILD_ROOT
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std bindir=%{_gamesbindir}

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/gnome/apps/Games/*

mkdir -p $RPM_BUILD_ROOT%{_iconsdir} \
	 $RPM_BUILD_ROOT%{_miconsdir} \
	 $RPM_BUILD_ROOT%{_liconsdir}
convert -geometry 48x48 client/teg_pix/teg_icono.png $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
convert -geometry 32x32 client/teg_pix/teg_icono.png $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert -geometry 16x16 client/teg_pix/teg_icono.png $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

%find_lang %{name} --with-gnome

%if %mdkversion < 200900
%post
%update_menus
%post_install_gconf_schemas %{name}
%endif

%preun
%preun_uninstall_gconf_schemas %{name}

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS ChangeLog PEOPLE README* ReleaseNotes.txt TODO
%{_gamesbindir}/*
%{_datadir}/pixmaps/*
%{_datadir}/applications/*.desktop
%{_datadir}/gnome/apps/Games/*.desktop
%{_sysconfdir}/gconf/schemas/*.schemas
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png


