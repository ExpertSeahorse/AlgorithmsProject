#ifndef BFS_IMPLEMENTATION_H
#define BFS_IMPLEMENTATION_H
#include <iostream>
#include <queue>
#include <set>
#include <vector>
#include <string>
#include <sstream>
#include <stack>

using namespace std;

class State{

    public:
        State();
        State(int[3][3]);
        int getValue(int,int);
        void setValue(int,int,int);
        State operator= (State);
        bool operator== (const State&) const;
       friend bool operator< (const State& a,const State& o);
        string toString() const;
        
        int getPath();
        
        int getBlankX();
        int getBlankY();
        
        bool moveUp(State&);
        bool moveDown(State&);
        bool moveRight(State&);
        bool moveLeft(State&);
        vector <State> expand();
        int tiles2D[3][3];
       
       vector <int> path;
};

#endif


