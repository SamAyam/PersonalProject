

/* #include "SDL_image.h"
#include <SDL.h> */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void run_game(), tick(int), check_input(),pick_up(int);
//int player_location(),player_stats(),check_flags(),pass_sec(),tick_log();


int main(){
    char weapons[20][10];   // no weapons list should exist in code, inventory list is built through pick_up function
    char *weapon[1][20];
    weapon=&weaparr[0];
    printf("%s",weapon);

    //strcpy(record[0].name,"Mike");

    //run_game();
    return 0;
}


run_game(){
    //run_game function holds all the variables and calls functions to play the game
    struct player{
    char name[10];
    int level,inventory[50],equipped[10],move,crouch,jump,action;
    float health, strength;
    }player1;
    int s=0, play=1;
    while(play!=0){
        tick(s);

        s=s+1; //last step before loop
    }
}


tick(int sec){
    check_input();      // checks to see what buttons the player is pressing
//    player_location();  // checks and syncs the location of the character
//    player_stats();  // checks and updates health and other stats
//    check_flags();  // like no health, no ground, or stuck on something. if flag: play=0
//    pass_sec(); // this is the part that tells other functions when time has passed
//    tick_log();     // keeps a log of passing seconds and what happened each sec

}



check_input(){
    //use pointers so changes don't have to be returned
    char input;
    int *m, *j, *c, *a;
    m=&move;
    j=&jump;
    c=&crouch;
    a=&action;

    scanf('%c', &input);
    switch(input){
    case 'a':
        move=-1;
    case 'd':
        move=1;
    case 's':
        crouch=1;
    case 'w':
        action=2;
    case ' ':
        jump=1;
    case 'f':
        action=1;
    }
}

pick_up(int item){
    switch(item){
    case 0:
        inventory
    }
}




/*
display(){

}
*/
