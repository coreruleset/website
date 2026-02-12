FROM mcr.microsoft.com/devcontainers/base:debian@sha256:a30da48cdf5f9144ff7f2156622e701e752fc258d77ca7bb00120624f1a95938 as build

# VARIANT can be either 'hugo' for the standard version or 'hugo_extended' for the extended version.
ARG VARIANT=hugo_extended
# VERSION can be either 'latest' or a specific version number
ARG HUGO_VERSION=latest
ARG SASS_VERSION=latest

RUN apt-get install ca-certificates jq

RUN URL=$(curl -s https://api.github.com/repos/gohugoio/hugo/releases/${HUGO_VERSION} | jq -r ".assets[] | select(.name | test(\"${VARIANT}.*Linux-64bit.tar.gz\")) | .browser_download_url") && \
    wget -O ${HUGO_VERSION}.tar.gz "${URL}" && \
    tar xf ${HUGO_VERSION}.tar.gz && \
    mv hugo* /usr/bin/hugo

RUN URL=$(curl -s https://api.github.com/repos/sass/dart-sass/releases/${SASS_VERSION} | jq -r ".assets[] | select(.name | test(\".*linux-x64-musl.tar.gz\")) | .browser_download_url") && \
    wget -O ${SASS_VERSION}.tar.gz "${URL}" && \
    tar xf ${SASS_VERSION}.tar.gz && \
    mv dart-sass/sass /usr/bin/sass

FROM mcr.microsoft.com/devcontainers/javascript-node@sha256:9b6ea344f7873aeea807726b1e8a59001389f83c3d47cf17f1d7218dca5eca35
COPY --from=build /usr/bin/hugo /usr/bin
COPY --from=build /usr/bin/sass /usr/bin
EXPOSE 1313
WORKDIR /src
CMD ["/usr/bin/hugo server"]
