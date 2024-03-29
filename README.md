# Full Stack Foundations

### Note that this is the free course offered by Udacity and NOT the Nanodegree program

<a href="https://www.udacity.com/">
  <img src="https://s3-us-west-1.amazonaws.com/udacity-content/rebrand/svg/logo.min.svg" width="300" alt="Udacity logo">
</a>

Virtual machine for the [Relational Databases](https://www.udacity.com/course/intro-to-relational-databases--ud197) and [Full Stack Foundations](https://www.udacity.com/course/full-stack-foundations--ud088) courses in the [Full Stack Web Developer Nanodegree program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Intro](#intro)
- [Installation](#installation)
- [Instructions](#instructions)
- [Troubleshooting](#troubleshooting)
- [Supporting Materials](#supporting-materials)

## Intro

### Python Version Notes
The VM as the course was written uses Python 2.7.12. Lesson 2 Making a Webserver makes use of BaseHTTPServer which is deprecated in favor of http.server in version 3 or greater. Reference this [doc](https://docs.python.org/2/library/basehttpserver.html) for additional information.

The python source files appended with '\_v2.py' should work with that version. Those without '\_v2.py' are written for Python version 3.6. These files use [http-server](https://docs.python.org/3.5/library/http.server.html).

#### NOTE - Anaconda
*Updated Anaconda to 4.7.10 which included Python 3.7.3. Code as written began throwing Content-Length errors when updating or adding new records. Created a Python 3.6 environment to run code and works as expected. Will investigate issue with 3.7 later.*

**Update on Python 3.7 vs. 3.6**
- Description of [problem](https://bugs.python.org/issue34226)
- Found solution at [StackOverflow](https://stackoverflow.com/questions/31486618/cgi-parse-multipart-function-throws-typeerror-in-python-3). Where else! 
- Example code needed in the do_POST(self):

```
if self.path.endswith("/edit"):
	ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
	# ERROR on content-length with python 3.7 NEED THIS!
	content_len = int(self.headers.get('Content-length'))
	pdict['boundary'] = bytes(p_dict['boundary'], "utf-8")
	pdict['CONTENT-LENGTH'] = content_len
	...
```

#### Additional Notes:

Assuming you have everything you need installed on your computer, it is not necessary to run the VM as presented in the course, but can be good practice to set one up and work on it.

The source code presented in the beginning of lesson 2 uses a response code of 301 in the do_POST(). This works, but in the version 3 code it does not. A response code of 200 is the proper code to use.

200 OK = Standard response for successful HTTP requests. The actual response will depend on the request method used. In a GET request, the response will contain an entity corresponding to the requested resource. In a POST request, the response will contain an entity describing or containing the result of the action.
    
301 Moved Permanently: This and all future requests should be directed to the given URI.

**Source Files:**  
Lesson 2 Concepts  

  - webserver_l2.py
  - webserver\_l2_v2.py

Lesson 2 Quiz Objectives  

  - webserver_v2.py
  - webserver.py

### Vagrant Notes
I made a modification to the Vagrantfile in order to access the working directory once the VM is running. You may not need to do this, but if you do your path will most certainly be different!

These lines were added:
_config.vm.synced_folder "/media/ssi112/Data/dev/udacity/fullstack", "/vagrant/fullstack",
id: "fullstack" # <--- this ID must be unique_
```
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-16.04"
  config.vm.box_version = "= 2.3.5"
  # config.vm.synced_folder ".", "/vagrant"
  config.vm.synced_folder ".", "/vagrant",
      id: "vagranthome" # <--- this ID must be unique
  config.vm.synced_folder "/media/ssi112/Data/dev/udacity/fullstack", "/vagrant/fullstack",
      id: "fullstack" # <--- this ID must be unique
  config.vm.network "forwarded_port", guest: 8000, host: 8000, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"

  # Work around disconnected virtual network cable.
  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--cableconnected1", "on"]
  end
```

Also, refer to Lesson 2: Making a Web Server, Concept 6. Port Forwarding

<hr /> 

In the next part of this course, you'll use a virtual machine (VM) to run an SQL database server and a web app that uses it. The VM is a Linux server system that runs on top of your own computer. You can share files easily between your computer and the VM; and you'll be running a web service inside the VM which you'll be able to access from your regular browser.

We're using tools called [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) to install and manage the VM. You'll need to install these to do some of the exercises. The instructions on this page will help you do this.

### Conceptual overview

[This video](https://www.youtube.com/watch?v=djnqoEO2rLc) offers a conceptual overview of virtual machines and Vagrant. You don't need to watch it to proceed, but you may find it informative.

### Use a terminal

You'll be doing these exercises using a Unix-style terminal on your computer. If you are using a **Mac or Linux** system, your regular terminal program will do just fine. On **Windows**, we recommend using the **Git Bash** terminal that comes with the Git software. If you don't already have Git installed, download Git from [git-scm.com](https://git-scm.com/downloads).

For a refresher on using the Unix shell, look back at [our Shell Workshop](https://www.udacity.com/course/ud206).

If you'd like to learn more about Git, take a look at [our course about Git](https://www.udacity.com/course/ud123).

## Installation

### Install VirtualBox

VirtualBox is the software that actually runs the virtual machine. [You can download it from virtualbox.org, here.](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) Install the _platform package_ for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

Currently (October 2017), the supported version of VirtualBox to install is version 5.1. Newer versions do not work with the current release of Vagrant.

**Ubuntu users:** If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.

### Install Vagrant

Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. [Download it from vagrantup.com.](https://www.vagrantup.com/downloads.html) Install the version for your operating system.

**Windows users:** The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

![vagrant --version](https://d17h27t6h515a5.cloudfront.net/topher/2016/December/584881ee_screen-shot-2016-12-07-at-13.40.43/screen-shot-2016-12-07-at-13.40.43.png)

_If Vagrant is successfully installed, you will be able to run_ `vagrant --version`
_in your terminal to see the version number._
_The shell prompt in your terminal may differ. Here, the_ `$` _sign is the shell prompt._

### Download the VM configuration

Use Github to fork and clone, or download, the repository [https://github.com/udacity/fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm).

You will end up with a new directory containing the VM files. Change to this directory in your terminal with `cd`. Inside, you will find another directory called **vagrant**. Change directory to the **vagrant** directory:

![vagrant-directory](https://d17h27t6h515a5.cloudfront.net/topher/2016/December/58487f12_screen-shot-2016-12-07-at-13.28.31/screen-shot-2016-12-07-at-13.28.31.png)

_Navigating to the FSND-Virtual-Machine directory and listing the files in it._
_This picture was taken on a Mac, but the commands will look the same on Git Bash on Windows._

## Instructions

### Start the virtual machine

From your terminal, inside the **vagrant** subdirectory, run the command `vagrant up`. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

![vagrant-up-start](https://d17h27t6h515a5.cloudfront.net/topher/2016/December/58488603_screen-shot-2016-12-07-at-13.57.50/screen-shot-2016-12-07-at-13.57.50.png)

_Starting the Ubuntu Linux installation with `vagrant up`._
_This screenshot shows just the beginning of many, many pages of output in a lot of colors._

When `vagrant up` is finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh` to log in to your newly installed Linux VM!

![linux-vm-login](https://d17h27t6h515a5.cloudfront.net/topher/2016/December/58488962_screen-shot-2016-12-07-at-14.12.29/screen-shot-2016-12-07-at-14.12.29.png)

_Logging into the Linux VM with `vagrant ssh`._

### Logged in

If you are now looking at a shell prompt that starts with the word `vagrant` (as in the above screenshot), congratulations — you've gotten logged into your Linux VM.

If not, take a look at the [Troubleshooting](#troubleshooting) section below.

### The files for this course

Inside the VM, change directory to `/vagrant` and look around with `ls`.

The files you see here are the same as the ones in the `vagrant` subdirectory on your computer (where you started Vagrant from). Any file you create in one will be automatically shared to the other. This means that you can edit code in your favorite text editor, and run it inside the VM.

Files in the VM's `/vagrant` directory are shared with the `vagrant` folder on your computer. But other data inside the VM is not. For instance, the PostgreSQL database itself lives only inside the VM.

### Running the database

The PostgreSQL database server will automatically be started inside the VM. You can use the `psql` command-line tool to access it and run SQL statements:

![linux-vm-PostgreSQL](https://d17h27t6h515a5.cloudfront.net/topher/2016/December/58489186_screen-shot-2016-12-07-at-14.46.25/screen-shot-2016-12-07-at-14.46.25.png)

_Running `psql`, the PostgreSQL command interface, inside the VM._

### Logging out and in

If you type `exit` (or `Ctrl-D`) at the shell prompt inside the VM, you will be logged out, and put back into your host computer's shell. To log back in, make sure you're in the same directory and type `vagrant ssh` again.

If you reboot your computer, you will need to run `vagrant up` to restart the VM.

## Troubleshooting

### I'm not sure if it worked

If you can type `vagrant ssh` and log into your VM, then it worked! It's normal for the `vagrant up` process to display a lot of text in many colors, including sometimes scary-looking messages in red, green, and purple. If you get your shell prompt back at the end, and you can log in, it should be OK.

### `vagrant up` is taking a long time

Because it's downloading a whole Linux operating system from the Internet.

### I'm on Windows, and when I run `vagrant ssh`, I don't get a shell prompt

Some versions of Windows and Vagrant have a problem communicating the right settings for the terminal. There is a workaround: Instead of `vagrant ssh`, run the command `winpty vagrant ssh` instead.

### I'm on Windows and getting an error about virtualization

Sometimes other virtualization programs such as Docker or Hyper-V can interfere with VirtualBox. Try shutting these other programs down first.

In addition, some Windows PCs have settings in the BIOS or UEFI (firmware) or in the operating system that disable the use of virtualization. To change this, you may need to reboot your computer and access the firmware settings. [A web search](https://www.google.com/search?q=enable%20virtualization%20windows%2010) can help you find the settings for your computer and operating system. Unfortunately there are so many different versions of Windows and PCs that we can't offer a simple guide to doing this.

### Why are we using a VM, it seems complicated

It is complicated. In this case, the point of it is to be able to offer the same software (Linux and PostgreSQL) regardless of what kind of computer you're running on.

### I got some other error message

If you're getting a specific textual error message, try looking it up on your favorite search engine. If that doesn't help, take a screenshot and post it to the discussion forums, along with as much detail as you can provide about the process you went through to get there.

### If all else fails, try an older version

Udacity mentors have noticed that some newer versions of Vagrant don't work on all operating systems. Version 1.9.2 is reported to be stabler on some systems, and version 1.9.1 is the supported version on Ubuntu 17.04. You can download older versions of Vagrant from [the Vagrant releases index](https://releases.hashicorp.com/vagrant/).

## Supporting Materials

[Virtual machine repository on GitHub](https://github.com/udacity/fullstack-nanodegree-vm)

[(Back to TOC)](#table-of-contents)
