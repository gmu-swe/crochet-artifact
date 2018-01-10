#!/bin/bash

cat << EOF
FtpServer.user.user.UserId=1
FtpServer.user.user.userpassword=pass
FtpServer.user.user.homedirectory=$CROSSFTP_DIR/res/home
FtpServer.user.user.writepermission=false
FtpServer.user.user.enableflag=true
EOF
