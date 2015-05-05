#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include "shell.h"
#include <stdlib.h>

int childprocess(char *argv[]){
    execvp(argv[0], argv); //run command from argv
    perror("FAIL:");
    int k;
    logerror(k = 10, "Child", "Failed Exec"); //call log error
    _exit(EXIT_FAILURE);

}

void parentprocess(){
	int returnstat;
    	wait(&returnstat);
	
            if(WIFEXITED(returnstat)){ //Terminates normal
               printf("child process terminated normally: %d", WEXITSTATUS(returnstat));  
            }
            else if(WIFSIGNALED(returnstat)){ //Terminates from signal
                printf("terminated due to signal: %d", WTERMSIG(returnstat));
            }
            else if(WIFSTOPPED(returnstat)){ //Stopped on processor
		printf("terminated due to stop: %d", WSTOPSIG(returnstat)); 
            }
            else if(WIFCONTINUED(returnstat)){
		printf("child continued");

	    }
}

int launch(int argc, char *argv[])
     { printf("Parsed:]\n");

     for(int i=0; i<argc; i++)
        printf("\t%s\n",argv[i]);

        printf("DONE\n\n");

 

     pid_t child;
     child = fork();
     if (child == -1){          //Fail
          int k;
          logerror(k = 10, "Child", "Failed Fork");
          _exit(EXIT_FAILURE);
  	  return -1; 		//return -1 on fail: Child
     }

     else if (child == 0){      //Success
         childprocess(argv);	//call child execute
     }
       
 
     else{       		  //Parent process
          parentprocess();	  //call parent wait    
     }         

	
     return 0; //return on normal exit
}
