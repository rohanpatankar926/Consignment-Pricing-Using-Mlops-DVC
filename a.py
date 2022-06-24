# A large war is raging in Valhalla. One of the viking tribes, the Bersekers have abig wall that covers the city on all sides. The wall was built by the Bersekers toprotect against military incursions. For the purposes of this problem, the wall is asquare. Berserkers are awesome craftsmen and they can quickly repair walls. Whenever a side is attacked successfully, the Wall on that side would be raisedtothe height sufficient to stop an identical attack in the future. Valhalla was frequently attacked by nomadic tribes. For the purposes of this
# problem, we assume that each tribe attacks the wall with some weapon X, strength S (the strength defines the height at impact) and in a direction
# (N,S,E,W). The weapon has a magnitude of 1 and it is the strength that defines
# the attack. In order to repel the attack, the Wall must have height S all alongthedefended side of the wall. If the height on that side of the Wall is lower than
# needed, the attack will breach the Wall at this point and succeed. Note that evena successful attack does not damage the Wall. After the attack, every attackedfragment of the Wall that was lower than S is raised to height S —in other words, the Wall is increased in the minimal way that would have stopped the attack. Note that if two or more attacks happened on the exact same day, the Wall was
# raised only after they all resolved, and is raised in the minimumway that wouldstop all of them. Assuming that initially the Wall was nonexistent (i.e., of height zero everywhere), and given the full description of all the nomadic tribes that attacked the Wall, determine how many of the attacks were successful. Weaponry has not advancedacross the globe and thus all tribes have the same weapon X
#Input:
# The first line of the input contains a single integer T denoting the number of test cases. The description of T test cases follows.
# The first line of each test case contains a single integer N, the number of nomadic tribes.   
# The second line contains N integers, the strength of the weapon of each tribe.
# The third line contains N integers, the number of attacks of each tribe.
# The fourth line contains N integers, the number of attacks of each tribe.
# The fifth line contains N integers, the number of attacks of each tribe.
# The sixth line contains N integers, the number of attacks of each tribe.
# The seventh line contains N integers, the number of attacks of each tribe.


#Output:
# For each test case, output a single line containing the number of successful attacks. 
# Constraints:
# 1 ≤ T ≤ 100
# 1 ≤ N ≤ 100
# 1 ≤ S ≤ 100
# 1 ≤ X ≤ 100   
# 1 ≤ N ≤ 100


#Sample Input:
# 2
# 3
# 1 2 3


#Sample Output:
# 2
# 1

