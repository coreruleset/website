FROM mcr.microsoft.com/devcontainers/base:debian@sha256:f1ac6335fc8cdd253c673a76edf77d81b5aa4bf9746bc67ecce4337d6bbaeb20 as build

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

FROM mcr.microsoft.com/devcontainers/javascript-node@sha256:cad3951c5a6ff844e5b080541b5a0fee63fc18b21adc9f4854a7b50b9775f4fd
COPY --from=build /usr/bin/hugo /usr/bin
COPY --from=build /usr/bin/sass /usr/bin
EXPOSE 1313
WORKDIR /src
CMD ["/usr/bin/hugo server"]
