#include <iostream>
#include "Bfs_implementation.h"

using namespace std;
template <typename Tiles>

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
    
    if (closed.size()==0 || (closed.find(temp)==closed.end())){
    
        vector<Tiles> possible_path;
        possible_path = temp.expand();
        closed.insert(temp);
                
        for (int i = possible_path.size()-1;i>=0;i--){
            mod.push(possible_path.at(i));
        }    
    }
    return BFS(goal,mod,closed,sol);
}

int main()
{
    int initialT[3][3] = {
        {1,3,4},
        {8,0,2},
        {7,6,5}
    };
    
    State initial(initialT);
    
    cout<<"Given puzzle:"<<endl;
    cout<<initial.toString()<< endl;
    
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
    
    queue <State> mod;
    mod.push(initial);
        
    BFS(goal,mod,closed,sol);
    
    cout<<"The shortest path cost using BFS: "<< sol.getPath() << " " << endl;
    
    return 0;
}


