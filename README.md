# grmx_poker
DP solution for optimal policy on Poker event

# セットアップ
``common/grmx_poker.py``内の``update_title``関数を書き換える.

``master``では以下の2つが実装されている
- (A) "TOWA(0)" & "IBUKI(1)" 称号
- (B) "IBUKI(1)" & "NOA(2)" & "SAKI(3)" 称号


# メインの計算
``python3 ch04/value_iter.py``


# 結果の見方
``grmx_policy.txt``では状態(n, y, x)について最適方策{"DRAW", "RESET"}を列挙する.

手札の枚数がn.

- TOWA  ... 1枚  1点
- IBUKI ... 1枚  4点
- NOA   ... 1枚 16点
- SAKI  ... 1枚 64点
として手札を得点化したものがx.

Aの称号を持っている時1点, Bの称号を持っている時2点として得点化したものがy.
