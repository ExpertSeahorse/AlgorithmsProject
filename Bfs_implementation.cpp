#include "Bfs_implementation.h"

State::State(){

}

State::State(int tiles2D[3][3]){
    for (int i = 0; i < 3; i++){
        for (int j = 0; j < 3; j++){
            setValue(i, j, tiles2D[i][j]);
        }
    }
}

void State::setValue(int i, int j, int value){
    tiles2D[i][j] = value;
}

int State::getValue(int i, int j){
    return tiles2D[i][j];
}

State State::operator=(State Tiles){
    for (int i = 0; i < 3; i++){
        for (int j = 0; j < 3; j++){
            setValue(i, j, Tiles.getValue(i, j));
        }
    }
    path = Tiles.path;
    return *this;
}

bool State::operator==(const State& Tiles) const {
    bool result = 1;
    for (int i = 0; i < 3; i++){
        for (int j = 0; j < 3; j++){
            if (tiles2D[i][j]!= Tiles.tiles2D[i][j]){
                result = 0;
            }
        }
    }
    return result;
}

bool operator< (const State& a,const State& o){
    return (a.toString() < o.toString());
}

string State::toString() const {
    stringstream stringToReturn;
    for (int i = 0; i < 3; i++){
        for (int j = 0; j < 3; j++){
            if (tiles2D[i][j] != 0){
                stringToReturn<<tiles2D[i][j]<<" ";
            }
            else{
                stringToReturn<<"  ";
            }
        }
        stringToReturn<<endl;
    }
    return stringToReturn.str();
}


int State::getPath(){
    int result=0;
    if (path.size() > 0)
    {
        for (unsigned i=0; i < path.size(); i++){
            result += path.at(i);
        }
        
    }
    return result;
}

int State::getBlankX(){
    for (int i=0;i<3;i++){
        for (int j=0;j<3;j++){
            if (tiles2D[i][j]==0){
                return j;
            }
        }
    }
    return 0;
}

int State::getBlankY(){
    for (int i=0;i<3;i++){
        for (int j=0;j<3;j++){
            if (tiles2D[i][j]==0){
                return i;
            }
        }
    }
    
    return 0;
}

bool State::moveLeft(State& Tiles){
    if (getBlankX() == 2 || getBlankX() == 1){
        Tiles = *this;
        int temp = tiles2D[getBlankY()][getBlankX()-1];
        int tempX = getBlankX();
        int tempY = getBlankY();
        Tiles.tiles2D[getBlankY()][getBlankX()-1] = 0;
        Tiles.tiles2D[tempY][tempX] = temp;
      
        Tiles.path.push_back(temp);
        return 1;
    }
    return 0;
}

bool State::moveRight(State& Tiles){
    if (getBlankX()== 0 || getBlankX()==1){
        Tiles=*this;
        int temp=tiles2D[getBlankY()][getBlankX()+1];
        int tempX=getBlankX();
        int tempY=getBlankY();
        Tiles.tiles2D[getBlankY()][getBlankX()+1]=0;
        Tiles.tiles2D[tempY][tempX]=temp;

        Tiles.path.push_back(temp);
        return 1;
    }
    return 0;
}

bool State::moveUp(State& Tiles){

    if (getBlankY()==2 || getBlankY()==1){
        Tiles=*this;
        int temp=tiles2D[getBlankY()-1][getBlankX()];
        int tempX=getBlankX();
        int tempY=getBlankY();
        Tiles.tiles2D[getBlankY()-1][getBlankX()]=0;
        Tiles.tiles2D[tempY][tempX]=temp;
        
        Tiles.path.push_back(temp);
        return 1;
    }
    return 0;
}

bool State::moveDown(State& Tiles){

    if (getBlankY()==0 || getBlankY()==1){
        Tiles=*this;
        int temp=tiles2D[getBlankY()+1][getBlankX()];
        int tempX=getBlankX();
        int tempY=getBlankY();
        Tiles.tiles2D[getBlankY()+1][getBlankX()]=0;
        Tiles.tiles2D[tempY][tempX]=temp;
      
        Tiles.path.push_back(temp);
        return 1;
    }
    return 0;
}

vector <State> State::expand(){
    vector <State> possible_path;
    State temp;

    if (moveLeft(temp)){
        possible_path.push_back(temp);
    }
    if (moveRight(temp)){
        possible_path.push_back(temp);
    }
    if (moveUp(temp)){
        possible_path.push_back(temp);
    }
    if (moveDown(temp)){
        possible_path.push_back(temp);
    }
    
    return possible_path;
}


