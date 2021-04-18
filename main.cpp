#include <iostream>
#include <string.h>
#include <chrono>
#include "Bfs_implementation.h"

using namespace std;

template <typename Tiles>

//recursive function for BFS
bool BFS(const Tiles &goal, queue<Tiles> &mod, set<Tiles> &closed, Tiles &sol)
{
    if (mod.empty()){
        return 0;
    }
       
    Tiles temp;
    
    temp = mod.front();
    mod.pop();

    if (temp == goal){
        sol = temp;
        return 1;
    }
    
    if (closed.size()==0 || (closed.find(temp)==closed.end()) ){
    
        vector<Tiles> possible_path;
        possible_path = temp.expand();
        closed.insert(temp);
                
        for (int i = possible_path.size()-1;i>=0;i--){
            mod.push(possible_path.at(i));
        }    
    }
    return BFS(goal,mod,closed,sol);
}

int main(int argc, char * const argv[])
{
     int initialT1[3][3] = {
        {1,3,4},
        {8,0,2},
        {7,6,5}
    };
     int initialT2[3][3] = {
        {1,3,4},
        {8,0,6},
        {7,5,2}
    };  
    
    //2 graphs available     
    if(strcmp(argv[1],"1") == 0){
       State initial(initialT1);
              
    cout<<"Given puzzle:"<<endl;
    cout<<initial.toString()<< endl;
    
    queue <State> mod;
    mod.push(initial);
    
     int goalT[3][3] = {
        {1,2,3},
        {8,0,4},
        {7,6,5}
    };
    
    State goal(goalT);
    cout<<"Goal puzzle:"<<endl;
    cout<<goal.toString()<< endl;
        
    set <State> closed;
    State sol;
    
    auto start = chrono::high_resolution_clock::now();        
    BFS(goal,mod,closed,sol);
    auto end = chrono::high_resolution_clock::now();
    
    
    cout<<"The shortest path cost using BFS: "<< sol.getPath() << " " << endl;
    
    
      cout<< "Performance is " << chrono::duration<int64_t,nano>(end-start).count() << " in nano seconds and " <<
        chrono::duration<double,milli>(end-start).count() << " in milliseconds " << endl;
        
    }else if(strcmp(argv[1],"2") == 0){
       State initial(initialT2); 
             
    cout<<"Given puzzle:"<<endl;
    cout<<initial.toString()<< endl;  
    
    queue <State> mod;
    mod.push(initial);
    
     int goalT[3][3] = {
        {1,2,3},
        {8,0,4},
        {7,6,5}
    };
    
    State goal(goalT);
    cout<<"Goal puzzle:"<<endl;
    cout<<goal.toString()<< endl;
        
    set <State> closed;
    State sol;
    
    auto start = chrono::high_resolution_clock::now();        
    BFS(goal,mod,closed,sol);
    auto end = chrono::high_resolution_clock::now();

    cout<<"The shortest path cost using BFS: "<< sol.getPath() << " " << endl;
    
    
    cout<< "Performance is " << chrono::duration<int64_t,nano>(end-start).count() << " in nano seconds and " <<
        chrono::duration<double,milli>(end-start).count() << " in milliseconds "<< endl;
            
    }else{
       cout << "Please choose either 1 or 2" << endl; 
       return 0;
    }
    
    
    return 0;
}


