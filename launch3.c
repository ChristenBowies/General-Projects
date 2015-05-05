#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <wait.h>

#include "shell.h"

void dochild(int argc, char *argv[], int inputfd, int outputfd);
int doparent(pid_t child, int pipeout);
int doopenread(char *name);
int doopenwrite(char *name);

/* Initialize Security
 *
 * If a program is setuid, it can run with two different sets of
 * permissions. The "user" is the person who started the program.
 * The "owner" is the person who owns the program. Initially,
 * a setuid program is running as the "owner." The first thing it
 * should do is drop its privileges down to the "user" until it
 * really needs to be the owner.
 * This function should do just that: it should change to being the
 * "user" instead of the "owner."
 *
 * Return:
 * 	0 if successful.
 *	1 if there is an error changing identity.
 */

//Global variables for permissions.
const int euid, ruid;
euid = geteuid ();
ruid = getuid ();

int initsecurity()
{ /* The effective userid is who you are currently running as. Get the
   * current value using geteuid. Currently, this is the "owner."
   */
  /* The real userid is who you are really. Get the current value
   * using getuid. Currently, this is the "user."
   */
  /* Switch the real and effective userids using setreuid. */
   int setreuid(euid, ruid);

  return 0;
}

/* Start a child process.
 *
 * Arguments:
 *   argc: The number of arguments, including the command.
 *   argv: An array containing the program to execute followed by the
 *         arguments.
 *   inputfd: If this child should read from a pipe, the file descriptor
 *            of the read end of the pipe. Otherwise 0.
 *   in: If the child is to read from a file, the name of the file.
 *       Otherwise, NULL.
 *   out: If the child is to write to a file, the name of the file.
 *        Otherwise, NULL.
 *   pipeout: 1 if the child should create a pipe to write to, 
 *            otherwise, 0.
 *
 * Return:
 *   If a pipe was created, immediately return the read end of the pipe.
 *   Otherwise, wait for the child to exit and return 0 if the child was
 *   successfully started and waited for and -1 if an error was
 *   encountered.
 */
int launch(int argc, char *argv[], int inputfd,
           char *in, char *out, int pipeout)
{ pid_t pid;
  int pipefd[2]={-1,-1};

  if((inputfd&&in)||(pipeout&&out))
  { errno=EINVAL;
    return -1;
  }

  /* If you need a pipe, you had better make it before the fork. */
  if(pipeout)
  { if(pipe(pipefd))
      return -1;
  }

  if((pid=fork())==0)
  { /* If the child won't use half the pipe, this is a good place to
       clean up. */
    if(pipefd[0]>0)
      if(close(pipefd[0]))
      { logerror(BAD,"shell","launch: error closing read end of new pipe");
        exit(BAD); /* If we cannot close the pipe, the program will
	              not function properly! */
      }
       
    if(in)
    { inputfd=doopenread(in);

      if(inputfd<0)
      { logerror(BAD,"shell","launch: error opening input file");
        exit(BAD);
      }
    }

    if(out)
    { pipefd[1]=doopenwrite(out);

      if(pipefd[1]<0)
      { logerror(BAD,"shell","launch: error opening output file");
        exit(BAD);
      }
    }

    dochild(argc,argv,inputfd,pipefd[1]);
    logerror(FATAL,"shell","launch: dochild returned unexpectedly");
    exit(FATAL);
  }

  if(pid<0)
  { logerror(FATAL,"shell","launch: error forking a new process");
    return -1;
  }

  /* If the parent won't use half the pipe, this is a good place to
     clean up. */

  if(pipeout)
  { if(close(pipefd[1]))
    { /* Ouch, if this doesn't work we become unstable, and have to
         exit!.
       */
       logerror(FATAL,"shell","launch: could not close unused write end of pipe.");
       exit(FATAL);
     }
  } else
    pipefd[0]=0;

  return doparent(pid,pipefd[0]);
} 

/* Do the processing required by the child. 
 *
 * Arguments:
 *   argc: The number of arguments.
 *   argv: The vector of arguments.
 *   inputfd: The file descriptor that should be used for input.
 *   outputfd: The file descriptor that should be used for output.
 *
 * Return: The function should never return. It should either execute
 *         the required program or exit with a non-zero value.
 */
void dochild(int argc, char *argv[], int inputfd, int outputfd)
{ /* For setuid programs, it is critical to carefully
     specify a safe environment. */
  char *envp[]={"PATH="PATH, NULL};

  /* Step 1: Set up the file descriptors. */

  /*   Step A: If inputfd is different from STDIN_FILENO, move the
               file from inputfd to STDIN_FILENO. Don't forget to clean up.
   */
  if(inputfd>0 && (dup2(inputfd,STDIN_FILENO)<0 || close(inputfd)))
  { logerror(BAD,"shell","dochild: error on STDIN");
    exit(BAD);
  }


  /*   Step B: If outputfd is different from STDOUT_FILENO, move the
               file from outputfd to STDOUT_FILENO. Don't forget to clean up.
   */
  if(outputfd>1 && (dup2(outputfd,STDOUT_FILENO)<0 || close(outputfd)))
  { logerror(BAD,"shell","dochild: error on STDOUT");
    exit(BAD);
  }

  /* If the program does not start with '/' or "../" or contain "/../"
     and it is found in SECURITYEXEC, then: A) Switch both real and
     effective userids to your userid (should be the real UID). Then
     use execve to run it.

     Otherwise, switch both userids to the user's uid (effective UID)
   */

  execvp(argv[0],argv);
  logerror(BAD,"shell","Error executing the command");
  exit(BAD);
}

/* Do the processing required by the parent.
 *
 * Arguments:
 *   child: The PID of the child process.
 *   pipeout: The file descriptor of the read end of the pipe, or
 *            0 if no pipe was created.
 *
 * Return:
 *     If a pipe was created, the file descriptor of the read end of
 *     the pipe.
 *     If an error was encountered, -1.
 *     Otherwise, 0.
 */
int doparent(pid_t child, int pipeout)
{ int status, ret;

  if(pipeout)
    return pipeout;

  for(;;) /* Wait as long as their are children to wait for. */
  { while((ret=waitpid(-1,&status,0))==-1 && errno==EINTR);

    if(ret==-1)
      return (errno==ECHILD)?0:-1;

    if(WIFEXITED(status))
    { status=WEXITSTATUS(status);

      fprintf( stderr, "Child %lld exited with code %d\n",
               (long long)ret, status);
    } else
    { status=WTERMSIG(status);

      fprintf( stderr, "Child %lld terminated with signal %d\n",
               (long long)ret, status);
    }
  }

  return 0;
}

/* Open a file for reading. If the file is found in the SECURITYREAD
 * directory, it is opened under the privileges of the setuid owner.
 * Otherwise, it is opened under the privileges of the user running
 * this program.
 *
 * Input: name, the name of the file to open.
 * Return: the file descriptor for the file or -1 if error.
 */
int doopenread(char *name)
{ /* If name does not start with '/' or "../" or contain "/../",
     switch to the setuid privileges and try to open the file relative
     to SECURITYREAD directory. Then switch back to the user
     privileges.
   
     Otherwise or if that open fails, try to open the name directly.
   */
  int fd;
  int length = sizeof(name) / sizeof(name[0]);
  if (name[0] != '/' || name[length] != '/' || name[0] != '/' && name[length] != '/'){
     //swich to owner
     initsecurity();
     //Open file
     char *dir = (char*) malloc(1+strlen(SECURITYREAD) + strlen(name));
     strcpy(dir, SECURITYREAD);
     strcat(dir, name);
     if (open(dir,O_RDONLY) == -1){
            initsecurity();
            //error
            //switch back security
            return 0;
     }
     else{
        initsecurity();
        return 0;

     }
   }
   else{
      if (open(name,O_RDONLY == -1)){
           return 0; //error
        }     

     } 


/* Open a file for writing. If the file is found in the SECURITYWRITE
 * directory, it is opened under the privileges of the setuid owner.
 * Otherwise, it is opened under the privileges of the user running
 * this program.
 *
 * Input: name, the name of the file to open.
 * Return: the file descriptor for the file or -1 if error.
 */
int doopenwrite(char *name)
{ /* If name does not start with '/' or "../" or contain "/../",
     switch to the setuid privileges and try to open the file relative
     to SECURITYWRITE directory, without using O_CREAT. Then switch
     back to the user privileges.
   
     Otherwise or if that open fails, try to open the name directly.
   */
  return 0;
  //return open(name, O_WRONLY|O_CREAT|O_TRUNC,
      //        S_IRUSR|S_IWUSR|S_IRGRP|S_IWGRP|S_IROTH|S_IWOTH);
}
