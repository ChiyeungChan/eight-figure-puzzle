#pragma warning(disable:4786) 
#include <algorithm> 
#include <cstdio> 
#include <set> 
#include <utility> 
#include <ctime> 
#include <cassert> 
#include <cstring> 
#include <iostream>
using namespace std;

/*item记录搜索空间中一个结点         
state 记录用整数形式表示的8数码格局          
blank 记录当前空格位置，主要用于程序优化，
扩展时可不必在寻找空格位置         
g, h  对应g(n), h(n)          
pre   记录当前结点由哪个结点扩展而来 */
struct item  
{          
	int state;          
	int blank;         
	int g;         
	int h;           
	int pre; 
};

const int MAXSTEPS = 100000; 
const int MAXCHAR = 100; 
char buf[MAXCHAR][MAXCHAR]; //open表 
item open[MAXSTEPS]; 
//vector<item> open;
int steps = 0;

//closed表，已查询状态只要知道该状态以及它由哪个结点扩展而来即可，用于输出路径 
//每次只需得到对应f值最小的待扩展结点，用堆实现提高效率
pair<int, int> closed[MAXSTEPS];
//读入，将8数码矩阵格局转换为整数表示 

bool read(pair<int,int> &state) 
{          
	if (!gets(buf[0]))                 
		return false;         
	if (!gets(buf[1]))                 
		return false;         
	if (!gets(buf[2]))                 
		return false; 

	//cout << strlen(buf[0]) << ' ' << strlen(buf[1]) << ' ' << strlen(buf[2]) << endl;
	assert(strlen(buf[0]) == 5 && strlen(buf[1]) == 5 && strlen(buf[2]) == 5);
	// astar.in中的每行数据长度必须为5
	state.first = 0;
	for (int i = 0, p = 1; i < 3; ++i)         
	{                  
		for (int j = 0; j < 6; j += 2)                  
		{                          
			if (buf[i][j] == '0')                                  
				state.second = i * 3 + j / 2;     // state.second为0（空格）在节点中的位置                    
			else                                  
				state.first += p * (buf[i][j] - '0');                
			p *= 10;                 
		}         
	}

	/* 若初试节点为:   
	1 2 3
	8 0 4
	7 6 5
	则state.first为567408321，state.second为4
	*/
	return true;
}

//计算当前结点距目标的距离 
int calculate(int current, int target)  // return h=the sum of distances each block have to move to the right position,这里的each block不包括空格
{          
	int c[9], t[9];         
	int i, cnt = 0;          
	for (i = 0; i < 9; ++i)         
	{                  
		c[current % 10] = t[target % 10] = i;                 
		current /= 10;                
		target /= 10;         
	}  

	for (i = 1; i < 9; ++i)                  
		cnt += abs(c[i] / 3 - t[i] / 3) + abs(c[i] % 3 - t[i] % 3);         

	return cnt; 
}

//open表中结点间选择时的规则 f(n) = g(n) + h(n)

class cmp 
{ 
public: inline bool operator()(item a, item b)         
		{                  
			return a.g + a.h > b.g + b.h;         
		} 
}; 

//将整数形式表示转换为矩阵表示输出
void pr(int state) 
{          
	memset(buf, ' ', sizeof(buf));         
	for (int i = 0; i < 3; ++i)         
	{                  
		for (int j = 0; j < 6; j += 2)                 
		{                          
			if (state % 10)
				buf[i][j] = state % 10 + '0';                         
			state /= 10;                 
		}       

		buf[i][5] = '\0';                 
		puts(buf[i]);
	}
}

//用于判断当前空格是否可以向对应方向移动
inline bool suit(int a, int b)  //空格移动后的坐标为(a,b)
{          
	return (a >= 0 && a < 3 && b >= 0 && b < 3); 
} 


//递归输出搜索路径
void path(int index) 
{          
	if (index == 0)         
	{                  
		pr(closed[index].first);                 
		puts("");                 
		return;         
	}          
	path(closed[index].second);         
	pr(closed[index].first); //将整数形式表示转换为矩阵表示输出         
	puts("");         
	++steps; 
}

int getNixuNum( int state ) //求节点的逆序对数
{
	int sum = 0;
	int result[9];
	memset( result, 0, sizeof(result) );
	//cout << result[8] << result[7] << endl;

	char buf[10];
	itoa( state, buf, 10 );
	//cout << buf << endl;
	int k = 0;
	while( buf[k] != '\0' )
	{
		result[9-k-1] = buf[k] - '0';
		k++;
	}
	
	for( int i = 0; i < 9; i++ )
	{
		for( int j = i + 1; j < 9; j++ )
		{
			if( result[i] && result[j] && result[i] > result[j] )
			{
				sum++;
			}
		}
	}
	return sum; //返回3*3方格数组的逆序对数
}

int main() 
{    
	//cout << getNixuNum(87654321);
	//open.resize(MAXSTEPS);
	unsigned int t1 = clock();    
	//cout << open.size() << endl;
	if( freopen("astar.in", "r", stdin) == NULL ) 
	{
		cout << "file not find\n";
		exit(0);
	};    

	freopen("astar2.out", "w", stdout);         
	set<int>states;         
	char tmp[100];          
	int i, x, y, a, b, nx, ny, end, next, index, kase = 0;         
	pair<int,int> start, target;         
	item head;          //4个方向移动时的偏移量          
	const int xtran[4] = {-1, 0, 1, 0};         
	const int ytran[4] = {0, 1, 0, -1};          
	const int p[] = {1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000};

	while (read(start))  // 读取初试状态节点       
	{                  
		unsigned int t2 = clock();                  
		printf("Case %d:\n\n", ++kase);                 
		gets(tmp);                 
		read(target);  // 读取目标状态节点          
		gets(tmp); 

		int targetNixuNum = getNixuNum(target.first);
		//若两者的逆序对数不是同为奇数或同为偶数，则无解
		if( !(getNixuNum(start.first)&1 && targetNixuNum&1 || !(getNixuNum(start.first)&1) && !(targetNixuNum&1)) )
		{
			cout << "无法从初始节点到终态节点\n";
			exit(0);
		}
		//初始化open表，将初始状态加入
		open[0].state = start.first;                  
		open[0].h = calculate(start.first, target.first); // 计算当前节点到目标节点的估计距离                
		open[0].blank = start.second;                 
		open[0].pre = -1;    // 初始节点无父节点             
		open[0].g = 0;  // 初始节点的g为0               
		index = 0;                  
		states.insert(start.first); // 扩展过节点保存在states中，即出现过的状态保存在states中，states为set<int>类型，其中的states中的元素唯一

		//提取open表中f值最小元素放入closed表，并对该结点进行扩展
		for (end = 1; end > 0; ++index)   // end为open表中的元素个数，一直循环到open表为空              
		{                          
			assert(index < MAXSTEPS);       
			//临时存储                         
			head = open[0]; // 由于使用pop_heap函数和push_heap函数，所以open[0]为g+h最小的元素

			//放入closed表记录当前格局和由哪个结点扩展而来（该结点肯定已在closed表中）
			closed[index].first = open[0].state; //放入close表中，表示已经扩展完的节点，下面的for循环会扩展其节点                         
			closed[index].second = open[0].pre; // index表示当前close表中当前扩展节点的下标
			//从open表中删除该结点                          
			pop_heap(open, open + end, cmp());//为algorithm文件中的函数，第一个参数指定开始位置，第二个指定结束，第三个指定比较函数                         
			--end;      

			//得到结果，递归输出路径
			if (head.state == target.first)                         
			{                                  
				path(index);                                 
				break;                         
			}

			x = head.blank / 3;                         
			y = head.blank % 3; //空格在3*3方格中的x,y坐标
			/*
			    |2 0 3|
			A = |1 8 4|
			    |7 6 5| // 看成3*3的数组
			则head.blank=1
			x=0,y=1,即空格的在3*3的数组中下标为(0,1)
			*/
			for (i = 0; i < 4; ++i)                         
			{                                  
				nx = x + xtran[i];                                 
				ny = y + ytran[i];   
				/*
				i=0时：(nx,ny）为当前空格向上移动一格后的坐标
				i=1时：(nx,ny）为当前空格向右移动一格后的坐标
				i=2时：(nx,ny）为当前空格向下移动一格后的坐标
				i=3时：(nx,ny）为当前空格向左移动一格后的坐标
				*/
				if (suit(nx, ny)) // 判断是否能够移动
				{                                          
					a = head.blank; // 空格当前位置,以上面矩阵A为例，a=1                                       
					b = nx * 3 + ny; // 空格移动后的新位置,开始是能够向右边移动，故b=0*3+2=2                                        
					//调换十进制表示整数对应两个数字位                                          
					next = head.state + ((head.state % p[a + 1]) / p[a] - (head.state % p[b + 1]) / p[b]) * p[b]  + ((head.state % p[b + 1]) / p[b] - (head.state % p[a + 1]) / p[a]) * p[a];   
					// 如head.state=567481302,空格向右移动一次后，next=567481032,即为移动后的节点
					
					// 判断能否由当前节点到达目标节点
					if( ( getNixuNum(next)&1 && targetNixuNum&1 ) || ( !(getNixuNum(next)&1) && !(targetNixuNum&1) ) )
					{
						//判断是否已经扩展过，即已经出现过
						if (states.find(next) == states.end()) //没出现就保存一下，也存入open表                                        
						{                                                  
							states.insert(next);                                                     
							open[end].pre = index; //扩展后的子节点，其父节点为当前扩展节点                                                
							open[end].blank = b;                                                 
							open[end].state = next;                                                  
							open[end].h = calculate(next,target.first); 
							open[end].g  = head.g + 1;  
							++end;  //open表中元素加1                                                
							push_heap(open, open + end, cmp());    //压入堆中                                     
						}           
					}
					                      
				}                         
			}                 
		} 

		if (end <= 0)                          
			puts("No solution");
		else                 
		{                          
			printf("Num of steps: %d\n", steps);                          
			printf("Num of expanded: %d\n", index);                         
			printf("Num of generated: %d\n", index + end);                         
			printf("Time consumed: %d\n\n", clock() - t2);                 
		} 

		states.clear();                 
		steps = 0;         
	}          
	printf("Total time consumed: %d\n", clock() - t1);         
	return 0;
}