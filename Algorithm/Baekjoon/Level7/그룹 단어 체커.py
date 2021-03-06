# 1316번
"""
문제
그룹 단어란 단어에 존재하는 모든 문자에 대해서, 각 문자가 연속해서 나타나는 경우만을 말한다.
예를 들면, ccazzzzbb는 c, a, z, b가 모두 연속해서 나타나고, kin도 k, i, n이 연속해서 나타나기 때문에 그룹 단어이지만,
aabbbccb는 b가 떨어져서 나타나기 때문에 그룹 단어가 아니다.
단어 N개를 입력으로 받아 그룹 단어의 개수를 출력하는 프로그램을 작성하시오.

입력
첫째 줄에 단어의 개수 N이 들어온다. N은 100보다 작거나 같은 자연수이다. 둘째 줄부터 N개의 줄에 단어가 들어온다.
단어는 알파벳 소문자로만 되어있고 중복되지 않으며, 길이는 최대 100이다.

출력
첫째 줄에 그룹 단어의 개수를 출력한다.
"""
# count 변수를 만들어서 그룹 단어일 경우에 증가시키는 것이 아니라 전체 갯수에서 그룹단어가 아닐 경우를 빼는 방식으로 구현

N = int(input())  # 단어의 개수

for i in range(N):  # 입력받은 개수만큼 반복
    words = input()  # 단어 입력
    for j in range(len(words) - 1):  # 단어의 길이 -1까지 반복 , -1을 하는 이유는 j와 j+1을 비교해줘야하므로 -1을 안하면 out of range 발생
        if words[j] != words[j+1]:  # 선택된 한 글자와 그 다음 글자가 같지 않으면  ==  같은 글자가 연속되지 않으면
            if words[j] in words[j+1:]:  # 선택된 글자를 다음 글자 이후의 모든 글자 안에 있다면 그룹 단어가 아니므로
                N -= 1  # N을 1 감소 시켜줌. N을 쓰는 이유는 만약 입력받은 모든 글자가 그룹 단어라면 그룹단어의 개수 == 입력 받은 단어의 개수
                break
print(N)
