# Pre-synced OpenMandriva Rolling builder image.
# Rebuilt weekly by .github/workflows/build-image.yml so package builds
# don't have to run `dnf distro-sync` + install the toolchain every time.
FROM --platform=linux/amd64 openmandriva/minimal:rolling

ARG BUILD_DATE=unknown

RUN dnf clean all \
 && dnf makecache \
 && dnf distro-sync -y \
 && dnf install -y \
        packaging-tools \
        rpmlint \
        git \
        sudo \
        curl \
        createrepo_c \
        github-cli \
        hostname \
        gnutar \
        rpm-openmandriva-setup \
 && (id builder >/dev/null 2>&1 || useradd -m builder) \
 && mkdir -p /etc/sudoers.d \
 && echo "builder ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/builder \
 && chmod 440 /etc/sudoers.d/builder \
 && dnf clean all \
 && rm -rf /var/cache/dnf /var/cache/libdnf5 /tmp/*

# build.sh looks for this file to know it can skip sync + tool install.
RUN echo "$BUILD_DATE" > /etc/oma-builder-image
