FROM php:7.4
RUN apt-get update -y
RUN apt-get upgrade -y
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# PHP-related things
ENV COMPOSER_ALLOW_SUPERUSER 1

# 1. development packages
RUN apt-get install -y \
    git \
    sudo \
    wget \
    zip \
    curl \
    sudo \
    unzip \
    libzip-dev \
    libicu-dev \
    libbz2-dev \
    libpng-dev \
    libjpeg-dev \
    libmcrypt-dev \
    libreadline-dev \
    libwebp-dev \
    libgmp-dev \
    libjpeg62-turbo-dev \
    libfreetype6-dev \
    libonig-dev \
    g++ \
    gnupg \
    gnupg2 \
    gnupg1

# PHP-related install
RUN docker-php-ext-install bcmath && \
    curl -s https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin/ --filename=composer

RUN docker-php-ext-configure gd --with-freetype=/usr/include/ --with-webp=/usr/include/  --with-jpeg=/usr/include/

RUN docker-php-ext-install \
    bz2 \
    intl \
    iconv \
    bcmath \
    opcache \
    calendar \
    pdo_mysql \
    zip \
    exif \
    gd \
    pdo \
    pdo_mysql

# Node install
ENV NODE_VERSION 10.13.0
ENV NVM_DIR /usr/local/nvm

RUN mkdir ${NVM_DIR} && \
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash && \
    . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

ENV NODE_PATH $NVM_DIR/versions/node/v$NODE_VERSION/lib/node_modules
ENV PATH      $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# Chrome install
RUN wget http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_80.0.3987.132-1_amd64.deb
RUN apt install -y ./google-chrome-stable_80.0.3987.132-1_amd64.deb

RUN cd /opt

RUN mkdir -p /laradock
WORKDIR /laradock

# RUN composer create-project laravel/laravel=7.6.2 laravel --prefer-dist

COPY composer.json .
COPY composer.lock .
COPY package.json .
COPY package-lock.json .

RUN npm install

RUN composer install \
    --ignore-platform-reqs \
    --no-interaction \
    --no-plugins \
    --no-scripts \
    --prefer-dist \
    --no-autoloader

RUN composer
RUN npm -v