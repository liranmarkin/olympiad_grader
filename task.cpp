#include <iostream>
#include <vector>

using namespace std;

int main(){
	ios::sync_with_stdio(0);
	int n; cin >> n;
	cout << n/2 << endl;
	for(int t = 0;t<n/2;t++){
		for(int i = 0;i<n;i++)
			cout << 1+(((i%2)? i/2+1 : n-i/2)+t)%n << " ";
		cout << "\n";
	}
	return 0;
}