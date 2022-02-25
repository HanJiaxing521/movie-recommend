'''
description: generate recommendation list.

process: 1. predict scores of empty cell in user-movie matrix
         2. choose top n movies by predicted scores.

date: 2022-01-30 15:52

author: Hanjiaxing
'''

import numpy as np
from similarity import select_neighbor


def rating_predict(U, UE):
    # fill up user-movie matrix by predicted rating
    # U: user-movie matrix
    # UE: user-hidden_factor matrix
    for u in U:
        neighborList = select_neighbor(u, UE)
        Ru = np.mean(i for i in u if i != -1)  # 求该用户的平均值Ru
        for item_i in range(u):
            if u[item_i] == -1:
                sim_rvi_rv_list = [(U[neighbor[0]][item_i]-np.mean(U[neighbor[0]]))*neighbor[1]
                                   for neighbor in neighborList if U[neighbor[0]][item_i] != -1]
                if len(sim_rvi_rv_list) == 0:
                    # 如果所有的邻居都没有对这部电影评分，则跳过对该电影的分数预测
                    continue

                # 计算Σsim(u,v)(rvi-rv), v in K
                sum_sim_rvi_rv = sum(sim_rvi_rv_list)
                # 计算Σ|sim(u,v)|, v in K
                sum_abs_sim_u_v = sum(abs(neighbor[1])
                                      for neighbor in neighborList)

                P_ui = Ru+sum_sim_rvi_rv/sum_abs_sim_u_v  # 计算P(u,i)
                u[item_i] = P_ui
    return U


def recommend_n_movie(U_origin, U, n=10):
    # recommend top n movies for active user
    # U_origin: not predicted user-movie matrix
    # U: predicted user-movie matrix
    # n: top n movie (default=10)

    for u_id in range(len(U)):
        marked_movies = [i for i in range(len(U)) if U_origin[i] != 0]
        not_marked_ratings = [(i, U[i])
                              for i in range(len(U)) if i not in marked_movies]

        # reversed sort according for the second element
        not_marked_ratings.sort(key=lambda x: -x[1])

        if len(not_marked_ratings) < n:
            print([e[0] for e in not_marked_ratings])
        else:
            print([e[0] for e in not_marked_ratings][:n])

    return
