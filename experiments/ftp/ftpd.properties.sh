#!/bin/bash

cat << EOF
config.socket-factory.class=org.apache.ftpserver.socketfactory.FtpSocketFactory
config.socket-factory.address=localhost
config.socket-factory.port=5555

config.user-manager.class=org.apache.ftpserver.usermanager.PropertiesUserManager
config.user-manager.admin=user
config.user-manager.prop-file=$CROSSFTP_DIR/users.properties
config.user-manager.prop-password-encrypt=false
EOF
