## 이 문서의 원작자는 당근마켓의 김대권 님입니다.

## 컨테이너?
* 컨테이너 엔진 -> libcontainer / libvirt / lxc / systemd-nspawn -> 리눅스 커널
* **컨테이너**: 리눅스 커널의 기능을 사용해서 프로세스를 **특별한** 형태로 실행하는 기술

## Iteration1: chroot
* [컨테이너 기초 - chroot를 사용한 프로세스의 루트 디렉터리 격리 | 44bits.io](https://www.44bits.io/ko/post/change-root-directory-by-using-chroot)
* [컨테이너 기초 - 정적 링크 프로그램을 chroot와 도커(Docker) scratch 이미지로 실행하기 | 44bits.io](https://www.44bits.io/ko/post/static-compile-program-on-chroot-and-docker-scratch-image)

### chroot 설치 및 실행
```
## 보통 리눅스에 이미 설치되어있어요
$ chroot --version

## 만약 설치되어있지 않다면 apt-get으로 coreutils 패키지를 설치해줍니다.
$ sudo apt-get install coreutils
$ chroot --version
```

chroot 사용법 - 이것만 알면 chroot 마스터!
```
chroot <ROOT_DIR> 명령어
```

동작하지 않는 예제: 왜 실패하는지 생각해보세요.
```
# 1차 시도 - 무작정 도전!
$ chroot ~/chroot/root bash

# 2차 시도 - 루트로 사용할 디렉터리를 생성
$ mkdir ~/chroot/root
$ chroot ~/chroot/root bash

# 3차 시도 - sudo도 추가해보고...
$ sudo chroot ~/chroot/root bash

# 4차 시도 - bash 파일 복사!
$ cp -v /bin/bash ~/chroot/root
$ sudo chroot ~/chroot/root bash
```

* **추가 과제**: bash가 의존하는 파일들을 새로운 루트 아래에 같은 구조로 복사하고 chroot를 실행해보세요.(힌트: ldd)
```
$ ldd /bin/bash
	linux-vdso.so.1 (0x00007ffec5f70000)
	libtinfo.so.5 => /lib/x86_64-linux-gnu/libtinfo.so.5 (0x00007f66fd09a000)
	libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f66fce96000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f66fcaa5000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f66fd5de000)
```
* **추가 과제**: ls도 같은 방식으로 실행해보세요. 실행에 성공하면 루트 디렉터리를 탐색해보세요.

### chroot로 C 프로그램 실행하기
아래 내용을 `hello.c`로 저장하세요.
```
#include <stdio.h>
int main()
{
   printf("Hello, World!");
   return 0;
}
```

`hello.c` 파일을 gcc를 사용해 `hello`로 필드합니다.
```
$ sudo apt-get install gcc
$ gcc -o hello hello.c
```

* **추가 과제**: Hello, world를 출력하는 C프로그램을 빌드하고, 이 프로그램을 chroot로 실행 가능하게 해보세요. (힌트: ldd)
* **추가 과제**: 위 과제의 작업 디렉터리(chroot의 루트)의 내용을 scratch 이미지(비어있는 이미지)를 베이스로 Dockerfile로 작성하고 컨테이너에서 hello를 실행해보세요.
```
$ curl -s https://get.docker.com/ | sudo sh
$ sudo usermod -aG docker your-user
```

```
FROM scratch
...
```
* **추가 과제**: 새로운 빈 디렉터리에 hello.c를 스태틱 빌드를 하고 hello 단일 파일로 chroot로 실행해보세요. (힌트: gcc의 --static 옵션)

### chroot 실행 환경 준비하기
#### bind mount를 사용해 디렉터리 마운트(생략)
```
$ sudo mount -o bind /bin $(pwd)/bin
$ sudo mount -o bind /lib $(pwd)/lib
$ sudo mount -o bind /lib64 $(pwd)/lib64
$ sudo chroot $(pwd) bash
```

#### debootstrap
> debootstrap is a tool which will install a Debian base system into a subdirectory of another, already installed system.  (https://wiki.debian.org/Debootstrap 참고)
```
$ sudo apt-get install debootstrap

# 오래 걸림!
$ sudo debootstrap stable stable-chroot http://deb.debian.org/debian/

$ cd stable-chroot
$ sudo chroot $(pwd) bash
```

### Docker 이미지로 chroot 실행환경 준비하기
```
$ mkdir ubuntu-image
$ docker run --name ubuntu-image ubuntu:latest
$ docker export ubuntu-image > ./ubuntu-image/image.tar
$ cd ubuntu-image
$ tar xf image.tar
$ sudo chroot $(pwd) bash
```

* **추가 과제**: 같은 방법으로 nginx:latest 이미지를 nginx 디렉터리에 만들어보세요.
* **추가 과제**: chroot로 nginx를 실행해보세요. nginx:latest 이미지를 사용하는 것과 어떤 차이가 있는지 비교해보세요.

## chroot 컨테이너와 Docker 컨테이너의 차이
* **추가 과제**: 두 컨테이너에 어떤 차이가 있는지 비교해보세요.

## Iteration2: Namespace & Union File System
### Default Namespace
프로세스들의 디폴트 네임스페이스 확인해봅니다.
```
$ cd /proc/1/ns
$ ls -al

# <OTHER_PID>에는 다른 프로세스의 pid 입력.
$ cd /proc/<OTHER_PID>/ns
$ ls -al
```

* 추가 과제: 다양한 프로세스의 네임스페이스를 비교해보세요.

### UTS Namespace
`unshare` 명령어의 사용법(`chroot`와 유사합니다.)

```
$ unshare <OPTIONS> <COMMAND>
```

`unshare`로 UTS 네임스페이스 분리하기
```
# 호스트네임을 확인합니다.
$ hostname
$ unshare --uts /bin/bash

# ##### 여기서부터 unshare로 uts 네임스페이스가 분리된 bash 프로세스 #####
# 호스트네임을 확인합니다.
-$ hostname
# 호스트네임을 설정합니다.
-$ hostname demo
# 변경된 호스트네임을 확인합니다.
-$ hostname
# Default Namespace와 새롭게 만들어진 uts 네임스페이스를 비교해봅니다.
-$ ll -al /proc/1/ns/uts
-$ ll -al /proc/$$/ns/uts
-$ exit

# ##### 다시 원래 bash 프로세스로 돌아갑니다. #####
# 호스트네임을 다시 확인합니다.
$ hostname
```

### Namespace 영속화
* pid 아래의 Namespace는 프로세스가 종료되면 사라집니다.
* Namespace를 보존하려면 파일로 영속화해야합니다.
* 관습적으로 `/run/<NAMESPACE_NAME>ns/` 디렉터리를 이용합니다.

```
$ mkdir -p /run/utsns
$ touch /run/utsns/demo
# 영속화할 경로를 지정합니다.
$ unshare --uts=/run/utsns/demo /bin/bash
$ hostname utsns_demo
$ echo $$
$ hostanme
```	

Namespace 공유하기. 다른 셸을 하나 더 띄워서 `nsenter`로 영속화된 Namespace를 `attach`해봅니다.
```
$ nsenter --uts=/run/utsns/demo /bin/bash
$ echo $$
$ hostname
```

### Pid Namespace
```
$ unshare -p -f --mount-proc chroot image /bin/bash
$ mount -t proc proc /proc
```

* 추가 과제: 이 PID가 네임스페이스 밖에서 어떻게 보이는지 찾아보세요.

## Union File System
### unionfs-fuse
`apt-get`을 사용해 `unionfs-fuse` 패키지를 설치합니다.
```
$ sudo apt-get install unionfs-fuse
```

```
# 2개의 디렉터리를 하나의 디렉터리에 마운트
$ mkdir  dirone dirtwo dirmerge
$ touch dirone/a dirone/b dirone/c dirtwo/x dirtwo/y dirtwo/z
$ unionfs-fuse dirone=RW:dirtwo=RW dirmerge

# 마운트 정보 확인
$ mount | grep unionfs-fuse

# 디렉터리 내용 확인 (ls -R이나 tree 사용)
$ cd dirmerge
$ ls -R .
```

상위 레이어(dirone)에서 하위 레이어의 파일을 가리는 예제

```
$ echo "Hello, world" > dirone/x
$ cat dirmerge/x

$ echo "Hello, foobar" > dirmerge/x
$ cat dirmerge/x
$ cat dirone/x
$ cat dirtwo/x
```

파일 삭제 예제

```
$ ls dirtwo
$ rm dirmerge/y
$ ls dirtwo
```

cow 모드 테스트

```
$ mkdir  container image1 image2 merge
$ touch image1/a image1/b image2/c
$ unionfs-fuse -o cow container=RW:image1=RO:image2=RO merge
$ tree .

# 파일 추가 예제
$ touch merge/d
$ tree .

# 파일 삭제 예제
$ rm merge/a
$ tree .

# 파일 편집 예제
$ echo "Hello, world!" > ./merge/b
$ cat container/b
$ cat image1/b
```

## overlayfs
```
$ mkdir container image1 image2 merge work
$ touch image1/a image1/b image2/c
$ sudo mount -t overlay overlay -o lowerdir=image1:image2,upperdir=container,workdir=work merge
$ tree . -I work
```

* 추가 과제: overlayfs와 unionfs-fuse의 인터페이스를 비교해보세요. unionfs-fuse의 cow 모드에서 진행한 예제를 overlayfs에서 시도해보세요.
* 추가 과제: overlayfs - merge 디렉터리(최상위 RW 레이어)에서 하위 레이어의 파일을 삭제시 어떻게 기록하는지 확인해보세요.

## overlayfs2 드라이버
* 추가 과제: /var/lib/docker/ 아래에 이미지가 어떤 구조로 저장되는지 탐색해보세요.
* 추가 과제: docker image inspect를 통해 overlayfs의 마운트 구조를 살펴보세요.
* 추가 과제: 위에서 확인한 명령어를 기반으로 도커 이미지를 overlayfs로 마운트하는 명령어를 작성해보세요.

## 더 공부하기
* [haconiwa/haconiwa: MRuby on Container / A Linux container runtime using mruby DSL for configuration, control and hooks](https://github.com/haconiwa/haconiwa)

