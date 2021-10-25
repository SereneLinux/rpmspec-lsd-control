Summary: lsd-control
Name: lsd-control
Version: 1.0.0
Release: 1%{?dist}
Group: System Environment/Shells
License: NONE
Packager: kahenteikou
Vendor: INDETAIL
Requires: lsd
BuildArch: noarch

%global debug_package %{nil}
%description
lsd-contorl
%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/local/lib/
mkdir -p %{buildroot}/usr/local/bin/
cat <<'EOF' > %{buildroot}/usr/local/lib/lsd-alias
#!/usr/bin/env bash

lsd_control=~/.lsd-control
if [[ -f "${lsd_control}" ]]; then
    source "${lsd_control}"
else
    touch ${lsd_control}
    echo -ne "lsd=true" > ${lsd_control}
    lsd=true
fi


if [[ ! ${TERM} = "linux" ]]; then
    set +e
    unalias ls > /dev/null 2>&1


    case ${lsd} in
        true) alias ls='lsd';;
        false) alias ls='ls';;
        *) :;;
    esac
fi
EOF
chmod 755 %{buildroot}/usr/local/lib/lsd-alias
cat <<'EOF' > %{buildroot}/usr/local/bin/lsd-control
#!/usr/bin/env bash


# Usage
# _usage <exit code>
_usage() {
    echo "usage ${0} <true or false>"
    echo
    echo "Set the default behavior when the ls command is executed."
    echo
    echo "If true is passed, the ls alias will be set to lsd."
    echo "If false is passed, no ls alias will be set."

    exit "${1}"
}


if [[ ! ${#} = 1 ]]; then
    _usage 1
fi

set +e
unalias ls > /dev/null 2>&1

case ${1} in
    true) lsd=true;;
    false) lsd=false;;
    *) _usage 1 ;;
esac


echo -ne "lsd=${lsd}" > ~/.lsd-control

echo "lsd was set ${lsd}"
echo "reload lsd-alias or restart shell"
EOF
chmod 755 %{buildroot}/usr/local/bin/lsd-control

%clean
rm -rf %{buildroot}

%post

%postun

%files
/usr/local/lib/lsd-alias
/usr/local/bin/lsd-control
%changelog
