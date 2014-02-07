Name:           gstreamer1-vaapi
Version:        0.5.8
Release:        2%{?dist}
Summary:        GStreamer plugins to use VA API video acceleration

License:        LGPLv2+
URL:            https://gitorious.org/vaapi/gstreamer-vaapi/
Source0:        http://www.freedesktop.org/software/vaapi/releases/gstreamer-vaapi/gstreamer-vaapi-%{version}.tar.bz2
# Fix for https://bugzilla.gnome.org/show_bug.cgi?id=723834
Patch1:         0001-vaapipostproc-Create-filter-surface-pool-if-it-does-.patch

BuildRequires:  glib2-devel >= 2.28
BuildRequires:  gstreamer1-devel >= 1.0.0
BuildRequires:  gstreamer1-plugins-base-devel >= 1.0.0
BuildRequires:  gstreamer1-plugins-bad-free-devel >= 1.0.0
BuildRequires:  libva-devel >= 1.1.0
BuildRequires:  libdrm-devel
BuildRequires:  libudev-devel
BuildRequires:  libGL-devel

%description

A collection of GStreamer plugins to let you make use of VA API video
acceleration from GStreamer applications.

Includes elements for video decoding, display, encoding and post-processing
using VA API (subject to hardware limitations).

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?isa} = %{version}-%{release}
Requires:       pkgconfig

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n gstreamer-vaapi-%{version}
%patch0 -p1

%build

# Fix for https://bugzilla.gnome.org/show_bug.cgi?id=723748
chmod -x ./tests/test-filter.c ./gst-libs/gst/vaapi/gstvaapifilter.c ./gst-libs/gst/vaapi/gstvaapifilter.h

# Wayland support in libva isn't present - gstreamer-vaapi can't support Wayland without it
# https://bugzilla.redhat.com/show_bug.cgi?id=1051862
%configure --enable-static=no --disable-wayland
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%make_install

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LIB NEWS README
%{_libdir}/*.so.*
%{_libdir}/gstreamer-1.0/*.so

%files devel
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LIB NEWS README
%{_includedir}/gstreamer-1.2/gst/vaapi
%{_libdir}/*.so
%{_libdir}/pkgconfig/gstreamer-vaapi*.pc

%changelog
* Fri Feb  7 2014 Simon Farnsworth <simon@farnz.org.uk> - 0.5.8-2
- Fix vaapipostproc crash in live pipelines

* Wed Feb  5 2014 Simon Farnsworth <simon@farnz.org.uk> - 0.5.8-1
- initial release
