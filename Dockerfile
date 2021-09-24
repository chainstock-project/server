FROM amazonlinux:2
RUN yum -y install git
RUN yum -y install python3
RUN yum -y install wget
RUN yum -y install tar
RUN yum -y install make
RUN wget https://golang.org/dl/go1.17.linux-amd64.tar.gz    
RUN tar -xzf go1.17.linux-amd64.tar.gz -C /usr/local
RUN rm -rf go1.17.linux-amd64.tar.
ENV GOPATH=$HOME/go
ENV PATH=$PATH:/usr/local/go/bin:$GOPATH/bin
ENV mkdir $GOPATH $GOPATH/bin $GOPATH/src $GOPATH/pkg
COPY script/ script/
RUN chmod a+x script/*
CMD [ "script/server.sh" ]